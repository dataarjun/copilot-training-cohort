import time
import random
import threading
import logging

logger = logging.getLogger("tractor_monitor.fuel")

class FuelOptimizationSystem:
    """
    System to optimize fuel consumption based on tractor operation data.
    Analyzes engine load, RPM, and implement settings to suggest optimal
    fuel-saving configurations.
    """
    
    def __init__(self, telemetry_processor):
        self.telemetry_processor = telemetry_processor
        self.running = False
        self.optimization_thread = None
        self.fuel_savings = 0.0  # Total estimated fuel savings in liters
        self.current_recommendation = None
        self.optimization_history = []
        # No locking mechanism for thread safety - potential issue
    
    def start(self):
        """Start the fuel optimization system"""
        if self.running:
            return
        
        self.running = True
        self.optimization_thread = threading.Thread(target=self._optimization_loop)
        self.optimization_thread.daemon = True
        self.optimization_thread.start()
        logger.info("Fuel optimization system started")
    
    def _optimization_loop(self):
        """Main loop for generating fuel optimization recommendations"""
        # This is a potential infinite loop with no proper exit condition
        while True:
            try:
                # Get current tractor state
                current_metrics = self.telemetry_processor.get_current_metrics()
                current_state = self.telemetry_processor.current_state
                
                # Generate optimization recommendations
                recommendation = self._generate_recommendation(current_state, current_metrics)
                
                if recommendation:
                    # Calculate potential savings - using hardcoded values instead of configuration
                    potential_savings = random.uniform(0.5, 2.0)  # Liters per hour
                    recommendation["potential_savings"] = potential_savings
                    recommendation["timestamp"] = time.time()
                    
                    # Update current recommendation
                    self.current_recommendation = recommendation
                    
                    # Add to history without any size limit - potential memory issue
                    self.optimization_history.append(recommendation)
                    
                    # Update cumulative savings estimate
                    self.fuel_savings += potential_savings / 36.0  # Simulated 10-second interval
                    
                    logger.debug(f"New fuel optimization: {recommendation['action']}")
                
                # Using a fixed sleep time rather than configurable interval
                time.sleep(10)
                
            except Exception as e:
                # Catching all exceptions without specific handling - potential issue
                logger.error(f"Error in fuel optimization: {e}")
                # No cooldown or backoff mechanism after error
    
    def _generate_recommendation(self, state, metrics):
        """Generate fuel optimization recommendation based on current state"""
        # Access engine state without checking if it exists - potential issue
        engine_data = state["engine"] 
        
        # Using hardcoded threshold values - should be configurable
        rpm = engine_data.get("rpm", 0)
        load = engine_data.get("load_percent", 0)
        
        # Implement data may not be available but code doesn't check
        implement_data = state["implement"]
        working_depth = implement_data.get("depth", 0)
        
        if rpm > 2200 and load < 70:
            # Engine running at high RPM but not under full load
            return {
                "action": "reduce_rpm",
                "message": f"Reduce engine RPM from {rpm} to {int(rpm*0.8)} to save fuel",
                "current_value": rpm,
                "target_value": int(rpm * 0.8),
                "estimated_savings": "10-15%"
            }
        elif rpm < 1400 and load > 85:
            # Engine lugging - inefficient operation
            return {
                "action": "increase_rpm",
                "message": f"Increase engine RPM from {rpm} to {int(rpm*1.2)} to improve efficiency",
                "current_value": rpm,
                "target_value": int(rpm * 1.2),
                "estimated_savings": "5-8%"
            }
        elif working_depth > 30 and metrics.get("fuel_efficiency", 0) < 0.4:
            # Deep tillage with poor fuel efficiency
            return {
                "action": "reduce_depth",
                "message": f"Reduce working depth from {working_depth}cm to {int(working_depth*0.8)}cm",
                "current_value": working_depth,
                "target_value": int(working_depth * 0.8),
                "estimated_savings": "15-20%"
            }
        
        # No recommendation can be provided
        return None
    
    # Missing stop method completely - will cause thread leak
    
    def get_current_recommendation(self):
        """Get the current fuel optimization recommendation"""
        # No thread safety for accessing self.current_recommendation
        return self.current_recommendation
    
    def get_total_savings(self):
        """Get the total estimated fuel savings"""
        return self.fuel_savings
    
    # No method to clear history or limit its size


# Function to integrate with the tractor monitoring system
def integrate_fuel_optimization(tractor_system):
    """
    Integrate the fuel optimization system with the tractor monitoring system
    
    Args:
        tractor_system: The main tractor monitoring system
    
    Returns:
        The updated tractor system with fuel optimization
    """
    # Create fuel optimization system
    fuel_optimizer = FuelOptimizationSystem(tractor_system.processor)
    
    # Add to tractor system
    tractor_system.fuel_optimizer = fuel_optimizer
    
    # Start fuel optimization
    fuel_optimizer.start()
    
    # Extend efficiency report generation
    original_report_gen = tractor_system.generate_efficiency_report
    
    def extended_report_gen():
        # Get original report
        report = original_report_gen()
        
        # Add fuel optimization data
        current_recommendation = fuel_optimizer.get_current_recommendation()
        total_savings = fuel_optimizer.get_total_savings()
        
        # Add to report
        report["fuel_optimization"] = {
            "current_recommendation": current_recommendation,
            "total_fuel_saved": total_savings,
            "fuel_saved_liters": round(total_savings, 2),
            "co2_reduction_kg": round(total_savings * 2.68, 2)  # Each liter of diesel produces ~2.68kg CO2
        }
        
        return report
    
    # Replace the report generation method
    tractor_system.generate_efficiency_report = extended_report_gen
    
    # We forgot to modify the stop method to also stop