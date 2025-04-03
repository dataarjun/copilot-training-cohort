import time
import json
import logging
import queue
import threading
import random
from datetime import datetime
from enum import Enum
import sqlite3
import can  # requires python-can package

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tractor_monitoring.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("tractor_monitor")

# ==========================================
# 1. CAN Bus Data Ingestion Module
# ==========================================

class CANBusReader:
    """Module to read and parse CAN bus signals from tractor systems"""
    
    def __init__(self, interface='socketcan', channel='can0', bitrate=250000):
        self.interface = interface
        self.channel = channel
        self.bitrate = bitrate
        self.bus = None
        self.running = False
        self.data_queue = queue.Queue(maxsize=1000)
        self.local_buffer = []
        self.buffer_lock = threading.Lock()
        
    def connect(self):
        """Connect to the CAN bus interface"""
        try:
            self.bus = can.interface.Bus(
                bustype=self.interface,
                channel=self.channel,
                bitrate=self.bitrate
            )
            logger.info(f"Successfully connected to CAN bus on {self.channel}")
            return True
        except can.CanError as e:
            logger.error(f"Failed to connect to CAN bus: {e}")
            # Simulate CAN bus for testing when hardware not available
            self.bus = None
            return False
    
    def parse_can_message(self, msg):
        """Parse CAN message into tractor telemetry data"""
        # In real implementation, this would map CAN IDs to specific tractor parameters
        # This is a simplified example
        if not msg:
            # For simulation
            msg_id = random.choice([0x100, 0x200, 0x300, 0x400])
            data = [random.randint(0, 255) for _ in range(8)]
            timestamp = time.time()
        else:
            msg_id = msg.arbitration_id
            data = list(msg.data)
            timestamp = msg.timestamp
        
        # Example mapping of CAN IDs to tractor parameters
        if msg_id == 0x100:
            # Engine data
            rpm = (data[0] * 256 + data[1]) / 4.0
            temp = data[2] - 40  # Celsius
            return {
                "type": "engine",
                "timestamp": timestamp,
                "rpm": rpm,
                "temperature": temp,
                "load_percent": data[3]
            }
        elif msg_id == 0x200:
            # Hydraulic system
            pressure = (data[0] * 256 + data[1]) / 10.0  # Bar
            return {
                "type": "hydraulic",
                "timestamp": timestamp,
                "pressure": pressure,
                "oil_temp": data[2] - 40,  # Celsius
                "flow_rate": data[3] * 0.5  # L/min
            }
        elif msg_id == 0x300:
            # GPS/position data
            return {
                "type": "position",
                "timestamp": timestamp,
                "speed": (data[0] * 256 + data[1]) / 10.0,  # km/h
                "heading": (data[2] * 256 + data[3]) / 10.0  # degrees
            }
        elif msg_id == 0x400:
            # Implement data
            return {
                "type": "implement",
                "timestamp": timestamp,
                "position": data[0],  # %
                "working_width": data[1] * 0.1,  # meters
                "depth": data[2] * 0.5  # cm
            }
        else:
            return {
                "type": "unknown",
                "timestamp": timestamp,
                "can_id": msg_id,
                "data": data
            }
    
    def start_reading(self):
        """Start reading from CAN bus in a separate thread"""
        if self.running:
            return
        
        self.running = True
        self.read_thread = threading.Thread(target=self._read_loop)
        self.read_thread.daemon = True
        self.read_thread.start()
        
        # Start the buffer flushing thread for offline storage
        self.buffer_thread = threading.Thread(target=self._buffer_flush_loop)
        self.buffer_thread.daemon = True
        self.buffer_thread.start()
        
        logger.info("CAN bus reading started")
    
    def _read_loop(self):
        """Main loop reading CAN messages"""
        if not self.bus and not self.connect():
            # If can't connect to real hardware, simulate data for testing
            logger.warning("Using simulated CAN data")
            self._simulate_can_data()
            return
            
        while self.running:
            try:
                msg = self.bus.recv(timeout=0.5)
                if msg:
                    telemetry_data = self.parse_can_message(msg)
                    
                    # Add to processing queue
                    try:
                        self.data_queue.put(telemetry_data, block=False)
                    except queue.Full:
                        logger.warning("Queue full, dropping CAN message")
                    
                    # Also store in local buffer for offline storage
                    with self.buffer_lock:
                        self.local_buffer.append(telemetry_data)
                        if len(self.local_buffer) > 5000:  # Limit buffer size
                            self.local_buffer = self.local_buffer[-5000:]
            except can.CanError as e:
                logger.error(f"Error reading from CAN bus: {e}")
                time.sleep(1)  # Avoid tight looping on error
    
    def _simulate_can_data(self):
        """Simulate CAN data for testing without hardware"""
        while self.running:
            # Create simulated telemetry data
            telemetry_data = self.parse_can_message(None)  # None triggers simulation
            
            # Add to processing queue
            try:
                self.data_queue.put(telemetry_data, block=False)
            except queue.Full:
                logger.warning("Queue full, dropping simulated CAN message")
            
            # Also store in local buffer for offline storage
            with self.buffer_lock:
                self.local_buffer.append(telemetry_data)
                if len(self.local_buffer) > 5000:  # Limit buffer size
                    self.local_buffer = self.local_buffer[-5000:]
            
            time.sleep(0.1)  # 10Hz simulation rate
    
    def _buffer_flush_loop(self):
        """Periodically flush buffer to local storage"""
        db_conn = sqlite3.connect('tractor_telemetry.db')
        cursor = db_conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            timestamp REAL,
            data_type TEXT,
            data_json TEXT
        )
        ''')
        db_conn.commit()
        
        while self.running:
            time.sleep(5)  # Flush every 5 seconds
            
            with self.buffer_lock:
                if not self.local_buffer:
                    continue
                
                # Copy buffer and clear it
                to_flush = self.local_buffer.copy()
                self.local_buffer.clear()
            
            # Store in SQLite database
            try:
                for data in to_flush:
                    data_type = data.get('type', 'unknown')
                    timestamp = data.get('timestamp', time.time())
                    data_json = json.dumps(data)
                    
                    cursor.execute(
                        "INSERT INTO telemetry VALUES (?, ?, ?)",
                        (timestamp, data_type, data_json)
                    )
                
                db_conn.commit()
                logger.debug(f"Flushed {len(to_flush)} records to local storage")
            except sqlite3.Error as e:
                logger.error(f"Database error: {e}")
                # Put data back in buffer
                with self.buffer_lock:
                    self.local_buffer = to_flush + self.local_buffer
    
    def stop(self):
        """Stop reading from CAN bus"""
        self.running = False
        if self.read_thread:
            self.read_thread.join(timeout=2)
        if self.buffer_thread:
            self.buffer_thread.join(timeout=2)
        if self.bus:
            self.bus.shutdown()
        logger.info("CAN bus reading stopped")
    
    def get_data(self, block=False, timeout=None):
        """Get next telemetry data point from the queue"""
        try:
            return self.data_queue.get(block=block, timeout=timeout)
        except queue.Empty:
            return None


# ==========================================
# 2. Telemetry Processing Pipeline
# ==========================================

class TelemetryProcessor:
    """Process and analyze telemetry data"""
    
    def __init__(self, data_source):
        self.data_source = data_source
        self.running = False
        self.processed_data = queue.Queue()
        self.field_efficiency_calculator = None  # We can use the previously defined function
        self.current_state = {
            "engine": {},
            "hydraulic": {},
            "position": {},
            "implement": {}
        }
        self.metrics = {
            "field_efficiency": 0,
            "fuel_efficiency": 0,
            "area_covered": 0,
            "working_time": 0,
            "idle_time": 0,
            "start_time": None,
            "last_timestamp": None
        }
        self._last_rpm = 0
    
    def start_processing(self):
        """Start the telemetry processing pipeline"""
        if self.running:
            return
        
        self.running = True
        self.process_thread = threading.Thread(target=self._process_loop)
        self.process_thread.daemon = True
        self.process_thread.start()
        
        # Set the start time for session metrics
        self.metrics["start_time"] = time.time()
        logger.info("Telemetry processing started")
    
    def _process_loop(self):
        """Main processing loop"""
        while self.running:
            # Get next data point
            data = self.data_source.get_data(block=True, timeout=1)
            if not data:
                continue
            
            # Update current state
            data_type = data.get("type", "unknown")
            if data_type in self.current_state:
                self.current_state[data_type].update(data)
            
            # Update timing metrics
            current_time = data.get("timestamp", time.time())
            if self.metrics["last_timestamp"]:
                time_diff = current_time - self.metrics["last_timestamp"]
                
                # Update working vs idle time
                if data_type == "engine" and "rpm" in data:
                    if data["rpm"] > 500:  # Engine is running
                        if data.get("load_percent", 0) > 20:  # Under load - working
                            self.metrics["working_time"] += time_diff
                        else:  # Idling
                            self.metrics["idle_time"] += time_diff
            
            self.metrics["last_timestamp"] = current_time
            
            # Process based on data type
            processed_data = self._process_by_type(data)
            
            # Calculate derived metrics periodically
            if random.random() < 0.05:  # ~5% chance each cycle
                self._calculate_derived_metrics()
            
            # Put on processed queue for alerting/display
            if processed_data:
                try:
                    self.processed_data.put(processed_data, block=False)
                except queue.Full:
                    pass
    
    def _process_by_type(self, data):
        """Process telemetry data based on type"""
        data_type = data.get("type", "unknown")
        processed = dict(data)  # Start with original data
        
        if data_type == "engine":
            # Process engine data
            if "rpm" in data and "load_percent" in data:
                # Calculate estimated fuel consumption (improved model)
                rpm = data["rpm"]
                load = data["load_percent"]
                
                # More sophisticated fuel model
                if rpm < 1000:
                    fuel_factor = 0.05
                elif rpm < 1800:
                    fuel_factor = 0.08
                else:
                    fuel_factor = 0.12
                    
                fuel_rate = (rpm * load * fuel_factor) / 10000.0  # Liters per hour
                processed["fuel_rate"] = fuel_rate
                
                # Engine health check with more parameters
                if data.get("temperature", 0) > 95:  # Celsius
                    processed["alert"] = "engine_overheating"
                    processed["alert_level"] = AlertLevel.WARNING
                    if data.get("temperature", 0) > 105:
                        processed["alert_level"] = AlertLevel.CRITICAL
                
                # New: Check for irregular RPM fluctuations
                if hasattr(self, '_last_rpm') and abs(rpm - self._last_rpm) > 500 and self._last_rpm > 0:
                    processed["alert"] = "irregular_rpm_fluctuation"
                    processed["alert_level"] = AlertLevel.WARNING
                self._last_rpm = rpm
        
        elif data_type == "hydraulic":
            # Process hydraulic system data
            if data.get("pressure", 0) > 180:  # Bar
                processed["alert"] = "high_hydraulic_pressure"
                processed["alert_level"] = AlertLevel.WARNING
            
            if data.get("oil_temp", 0) > 80:  # Celsius
                processed["alert"] = "hydraulic_overheating"
                processed["alert_level"] = AlertLevel.WARNING
        
        elif data_type == "position":
            # Process position/GPS data
            if "speed" in data:
                # Check if speed matches engine state
                engine_rpm = self.current_state.get("engine", {}).get("rpm", 0)
                if data["speed"] < 0.5 and engine_rpm > 1500:
                    processed["alert"] = "high_rpm_stationary"
                    processed["alert_level"] = AlertLevel.INFO
                
                # Update area calculation if implement is down
                implement_position = self.current_state.get("implement", {}).get("position", 0)
                if implement_position > 50 and data["speed"] > 0.5:  # Implement is working
                    implement_width = self.current_state.get("implement", {}).get("working_width", 3)
                    # Very simplified area calculation
                    area_increment = (data["speed"] / 3600) * implement_width * 0.1  # hectares
                    self.metrics["area_covered"] += area_increment
        
        elif data_type == "implement":
            # Process implement data
            pass
        
        return processed
    
    def _calculate_derived_metrics(self):
        """Calculate derived performance metrics"""
        # Calculate field efficiency
        if self.metrics["working_time"] > 0:
            implement_width = self.current_state.get("implement", {}).get("working_width", 3)
            area_covered = self.metrics["area_covered"]
            
            # Using the previously defined field efficiency function
            try:
                quality_factor = 0.85  # This would be derived from other sensors in a real system
                self.metrics["field_efficiency"] = calculate_field_efficiency(
                    area_covered=area_covered,
                    quality_factor=quality_factor,
                    time_spent=self.metrics["working_time"] / 3600,  # Convert to hours
                    theoretical_width=implement_width
                )
            except ValueError as e:
                logger.warning(f"Error calculating field efficiency: {e}")
        
        # Calculate fuel efficiency if we have area and engine data
        if self.metrics["area_covered"] > 0 and "fuel_rate" in self.current_state.get("engine", {}):
            fuel_used = self.current_state["engine"]["fuel_rate"] * (self.metrics["working_time"] / 3600)
            if fuel_used > 0:
                self.metrics["fuel_efficiency"] = self.metrics["area_covered"] / fuel_used  # ha/L
    
    def get_processed_data(self, block=False, timeout=None):
        """Get next processed data point"""
        try:
            return self.processed_data.get(block=block, timeout=timeout)
        except queue.Empty:
            return None
    
    def get_current_metrics(self):
        """Get current performance metrics"""
        return dict(self.metrics)
    
    def stop(self):
        """Stop the processing pipeline"""
        self.running = False
        if hasattr(self, 'process_thread'):
            self.process_thread.join(timeout=2)
        logger.info("Telemetry processing stopped")


# ==========================================
# 3. Alerting System
# ==========================================

class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = 1
    WARNING = 2
    CRITICAL = 3

class AlertManager:
    """Manage and distribute alerts based on telemetry data"""
    
    def __init__(self, data_source):
        self.data_source = data_source
        self.running = False
        self.alert_handlers = []
        self.alert_history = []
        self.max_history = 100
        self.alert_counts = {
            AlertLevel.INFO: 0,
            AlertLevel.WARNING: 0,
            AlertLevel.CRITICAL: 0
        }
        # Connectivity manager for handling rural connectivity issues
        self.connectivity = ConnectivityManager()
    
    def register_handler(self, handler):
        """Register a function to receive alerts"""
        if handler not in self.alert_handlers:
            self.alert_handlers.append(handler)
    
    def start_monitoring(self):
        """Start the alert monitoring system"""
        if self.running:
            return
        
        self.running = True
        self.connectivity.start()
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        logger.info("Alert monitoring started")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            # Get processed data
            data = self.data_source.get_processed_data(block=True, timeout=1)
            if not data:
                continue
            
            # Check for alerts in the data
            if "alert" in data and "alert_level" in data:
                self._handle_alert(data)
    
    def _handle_alert(self, data):
        """Process and distribute an alert"""
        alert_level = data["alert_level"]
        alert_type = data["alert"]
        
        # Create alert object
        alert = {
            "timestamp": data.get("timestamp", time.time()),
            "level": alert_level,
            "type": alert_type,
            "message": self._generate_alert_message(alert_type, data),
            "data": data
        }
        
        # Add to history
        self.alert_history.append(alert)
        if len(self.alert_history) > self.max_history:
            self.alert_history = self.alert_history[-self.max_history:]
        
        # Update counts
        self.alert_counts[alert_level] = self.alert_counts.get(alert_level, 0) + 1
        
        # Distribute to handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Error in alert handler: {e}")
        
        # Log alert
        log_method = logging.info
        if alert_level == AlertLevel.WARNING:
            log_method = logging.warning
        elif alert_level == AlertLevel.CRITICAL:
            log_method = logging.error
        
        log_method(f"ALERT: {alert['message']}")
        
        # For critical alerts, ensure they're sent even with poor connectivity
        if alert_level == AlertLevel.CRITICAL:
            self.connectivity.send_with_retry(alert)
    
    def _generate_alert_message(self, alert_type, data):
        """Generate a human-readable alert message"""
        messages = {
            "engine_overheating": f"Engine overheating! Temperature: {data.get('temperature')}°C",
            "high_hydraulic_pressure": f"High hydraulic pressure: {data.get('pressure')} bar",
            "hydraulic_overheating": f"Hydraulic oil overheating: {data.get('oil_temp')}°C",
            "high_rpm_stationary": f"High RPM while stationary: {data.get('rpm')} RPM",
            "irregular_rpm_fluctuation": f"Irregular RPM fluctuation detected: {data.get('rpm')} RPM",
            # Add more alert types here
        }
        
        return messages.get(alert_type, f"Unknown alert: {alert_type}")
    
    def get_alert_history(self):
        """Get alert history"""
        return self.alert_history.copy()
    
    def get_alert_counts(self):
        """Get alert counts by severity"""
        return dict(self.alert_counts)
    
    def stop(self):
        """Stop the alert monitoring system"""
        self.running = False
        self.connectivity.stop()
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=2)
        logger.info("Alert monitoring stopped")


# ==========================================
# 4. Connectivity Manager for Rural Environments
# ==========================================

class ConnectivityManager:
    """Manage connectivity in rural environments with poor signal"""
    
    def __init__(self, check_interval=30):
        self.check_interval = check_interval  # seconds
        self.running = False
        self.online = False
        self.last_check = 0
        self.message_queue = queue.Queue()
        self.storage_path = "offline_messages.json"
        self.load_stored_messages()
    
    def start(self):
        """Start connectivity management"""
        if self.running:
            return
        
        self.running = True
        self.check_thread = threading.Thread(target=self._connectivity_check_loop)
        self.check_thread.daemon = True
        self.check_thread.start()
        logger.info("Connectivity management started")
    
    def _connectivity_check_loop(self):
        """Periodically check connectivity and process queued messages"""
        while self.running:
            now = time.time()
            if now - self.last_check >= self.check_interval:
                self.online = self._check_connectivity()
                self.last_check = now
                
                if self.online:
                    self._process_queued_messages()
            
            time.sleep(1)  # Avoid tight loop
    
    def _check_connectivity(self):
        """Check if we have connectivity - in a real system, would ping server"""
        # Simulate rural connectivity - 70% chance of being online
        online = random.random() < 0.7
        if online:
            logger.debug("Connectivity check: Online")
        else:
            logger.debug("Connectivity check: Offline")
        return online
    
    def _process_queued_messages(self):
        """Process queued messages when connectivity is restored"""
        sent_count = 0
        while not self.message_queue.empty() and self.online:
            try:
                message = self.message_queue.get(block=False)
                success = self._send_message(message)
                if success:
                    sent_count += 1
                else:
                    # Put back in queue if send failed
                    self.message_queue.put(message)
                    break
            except queue.Empty:
                break
        
        if sent_count > 0:
            logger.info(f"Sent {sent_count} queued messages after connectivity restored")
            self.save_stored_messages()  # Update stored messages
    
    def _send_message(self, message):
        """Send a message to the central system"""
        # In a real system, this would use HTTP requests or MQTT
        # Here we just simulate success/failure
        success = random.random() < 0.9  # 90% success rate when online
        if not success:
            logger.warning("Failed to send message, will retry later")
        return success
    
    def send_with_retry(self, message):
        """Send a message with retry logic for poor connectivity"""
        if not self.online:
            # Store for later
            logger.info("Offline, queueing message for later delivery")
            self.message_queue.put(message)
            self.save_stored_messages()
            return False
        
        # Try to send immediately
        success = self._send_message(message)
        if not success:
            # Queue for retry
            self.message_queue.put(message)
            self.save_stored_messages()
        
        return success
    
    def load_stored_messages(self):
        """Load stored messages from disk"""
        try:
            with open(self.storage_path, 'r') as f:
                messages = json.load(f)
                for msg in messages:
                    self.message_queue.put(msg)
            logger.info(f"Loaded {len(messages)} stored messages")
        except (FileNotFoundError, json.JSONDecodeError):
            logger.info("No stored messages found or file corrupt")
    
    def save_stored_messages(self):
        """Save queued messages to disk"""
        try:
            # Convert queue to list
            messages = []
            temp_queue = queue.Queue()
            
            while not self.message_queue.empty():
                msg = self.message_queue.get()
                messages.append(msg)
                temp_queue.put(msg)
            
            # Restore queue
            self.message_queue = temp_queue
            
            with open(self.storage_path, 'w') as f:
                json.dump(messages, f)
            
            logger.debug(f"Saved {len(messages)} messages to disk")
        except Exception as e:
            logger.error(f"Error saving messages to disk: {e}")
    
    def stop(self):
        """Stop connectivity management"""
        self.running = False
        if hasattr(self, 'check_thread'):
            self.check_thread.join(timeout=2)
        
        # Save any remaining messages
        self.save_stored_messages()
        logger.info("Connectivity management stopped")


# ==========================================
# Main System Integration
# ==========================================

class TractorMonitoringSystem:
    """Main system to integrate all components"""
    
    def __init__(self):
        # Create components
        self.can_reader = CANBusReader()
        self.processor = TelemetryProcessor(self.can_reader)
        self.alert_manager = AlertManager(self.processor)
        
        # Register example alert handler
        self.alert_manager.register_handler(self._alert_handler)
    
    def _alert_handler(self, alert):
        """Example alert handler"""
        # In a real system, this might:
        # - Send SMS for critical alerts
        # - Update dashboard UI
        # - Log to database
        level_name = alert["level"].name
        print(f"[{level_name}] {alert['message']}")
    
    def start(self):
        """Start the entire monitoring system"""
        self.can_reader.start_reading()
        self.processor.start_processing()
        self.alert_manager.start_monitoring()
        logger.info("Tractor monitoring system started")
    
    def stop(self):
        """Stop the entire monitoring system"""
        self.alert_manager.stop()
        self.processor.stop()
        self.can_reader.stop()
        logger.info("Tractor monitoring system stopped")
    
    def get_system_status(self):
        """Get overall system status"""
        metrics = self.processor.get_current_metrics()
        alerts = self.alert_manager.get_alert_counts()
        
        status = {
            "system_time": datetime.now().isoformat(),
            "uptime": time.time() - metrics.get("start_time", time.time()),
            "metrics": metrics,
            "alerts": {
                "info": alerts.get(AlertLevel.INFO, 0),
                "warning": alerts.get(AlertLevel.WARNING, 0),
                "critical": alerts.get(AlertLevel.CRITICAL, 0)
            }
        }
        
        return status
    
    def generate_efficiency_report(self):
        """Generate a comprehensive efficiency report"""
        metrics = self.processor.get_current_metrics()
        alerts = self.alert_manager.get_alert_history()
        
        # Get recent critical alerts
        critical_alerts = [a for a in alerts if a["level"] == AlertLevel.CRITICAL][-5:]
        
        report = {
            "report_time": datetime.now().isoformat(),
            "field_metrics": {
                "area_covered": metrics["area_covered"],
                "field_efficiency": metrics["field_efficiency"],
                "fuel_efficiency": metrics["fuel_efficiency"],
                "working_time_hours": metrics["working_time"] / 3600,
                "idle_time_hours": metrics["idle_time"] / 3600,
                "idle_percentage": (metrics["idle_time"] / (metrics["working_time"] + metrics["idle_time"])) * 100 if metrics["working_time"] + metrics["idle_time"] > 0 else 0
            },
            "alert_summary": {
                "total_alerts": sum(self.alert_manager.get_alert_counts().values()),
                "critical_alerts": len(critical_alerts),
                "recent_critical": [a["message"] for a in critical_alerts]
            },
            "recommendations": self._generate_recommendations(metrics)
        }
        
        return report
    
    def _generate_recommendations(self, metrics):
        """Generate operational recommendations based on metrics"""
        recommendations = []
        
        # Efficiency recommendations
        if metrics["field_efficiency"] < 0.7:
            recommendations.append("Field efficiency below target. Consider adjusting implement width or speed.")
        
        # Idle time recommendations
        if metrics["idle_time"] > metrics["working_time"] * 0.2:  # More than 20% idle time
            recommendations.append("High idle time detected. Review field operations to minimize non-productive time.")
        
        # Fuel efficiency recommendations
        if metrics.get("fuel_efficiency", 0) < 0.5:  # Less than 0.5 ha/L
            recommendations.append("Fuel efficiency is below optimal levels. Consider reducing engine RPM when possible.")
        
        return recommendations


# Example usage and integration with field efficiency calculator
if __name__ == "__main__":
    # Start the monitoring system
    tractor_system = TractorMonitoringSystem()
    tractor_system.start()
    
    try:
        # Run for sample period
        print("Tractor monitoring system running. Press Ctrl+C to stop.")
        report_counter = 0
        while True:
            # Every 10 seconds, print system status
            time.sleep(10)
            report_counter += 1
            
            status = tractor_system.get_system_status()
            
            print("\nSystem Status:")
            print(f"Uptime: {status['uptime']:.1f} seconds")
            print(f"Area covered: {status['metrics']['area_covered']:.2f} hectares")
            print(f"Field efficiency: {status['metrics']['field_efficiency']:.2f}")
            print(f"Alerts: {status['alerts']['info']} info, "
                  f"{status['alerts']['warning']} warnings, "
                  f"{status['alerts']['critical']} critical")
            
            # Generate efficiency report every 3rd cycle (30 seconds)
            if report_counter % 3 == 0:
                report = tractor_system.generate_efficiency_report()
                print("\n==== EFFICIENCY REPORT ====")
                print(f"Time: {report['report_time']}")
                print(f"Area covered: {report['field_metrics']['area_covered']:.2f} hectares")
                print(f"Field efficiency: {report['field_metrics']['field_efficiency']:.2f}")
                print(f"Idle percentage: {report['field_metrics']['idle_percentage']:.1f}%")
                
                if report['recommendations']:
                    print("\nRecommendations:")
                    for rec in report['recommendations']:
                        print(f"- {rec}")
                print("===========================")
    
    except KeyboardInterrupt:
        print("\nShutting down monitoring system...")
        tractor_system.stop()
        print("System stopped.")