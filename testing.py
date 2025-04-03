def calculate_field_efficiency(area_covered, quality_factor, time_spent, theoretical_width):
    """
    Calculate agricultural field efficiency.
    
    Efficiency = (area covered × quality factor) ÷ (time × theoretical width)
    
    Parameters:
        area_covered (float): Area covered in hectares or acres
        quality_factor (float): Quality factor between 0 and 1
                               (1 being perfect quality, 0 being no quality)
        time_spent (float): Time spent in hours
        theoretical_width (float): Theoretical working width in meters or feet
    
    Returns:
        float: Field efficiency as a decimal (multiply by 100 for percentage)
        
    Raises:
        ValueError: If input parameters are invalid
    """
    # Input validation
    if area_covered <= 0:
        raise ValueError("Area covered must be positive")
    
    if not 0 <= quality_factor <= 1:
        raise ValueError("Quality factor must be between 0 and 1")
        
    if time_spent <= 0:
        raise ValueError("Time spent must be positive")
        
    if theoretical_width <= 0:
        raise ValueError("Theoretical width must be positive")
    
    # Calculate field efficiency
    efficiency = (area_covered * quality_factor) / (time_spent * theoretical_width)
    
    return efficiency


def format_efficiency_report(area_covered, quality_factor, time_spent, theoretical_width, units=None):
    """
    Calculate field efficiency and return a formatted report.
    
    Parameters:
        area_covered (float): Area covered
        quality_factor (float): Quality factor between 0 and 1
        time_spent (float): Time spent
        theoretical_width (float): Theoretical working width
        units (dict, optional): Dictionary containing unit labels
                               e.g. {'area': 'hectares', 'width': 'meters', 'time': 'hours'}
    
    Returns:
        str: Formatted efficiency report
    """
    if units is None:
        units = {'area': 'hectares', 'width': 'meters', 'time': 'hours'}
    
    try:
        efficiency = calculate_field_efficiency(
            area_covered, quality_factor, time_spent, theoretical_width
        )
        
        report = f"""
Field Efficiency Report:
-----------------------
Area covered: {area_covered} {units.get('area', 'units')}
Quality factor: {quality_factor:.2f} (on scale of 0-1)
Time spent: {time_spent} {units.get('time', 'hours')}
Theoretical width: {theoretical_width} {units.get('width', 'units')}
-----------------------
Field efficiency: {efficiency:.4f} ({efficiency*100:.2f}%)
"""
        return report
    
    except ValueError as e:
        return f"Error calculating efficiency: {str(e)}"

# Example usage
# efficiency = calculate_field_efficiency(50, 0.85, 8, 10)
# print(f"Field efficiency: {efficiency:.4f} ({efficiency*100:.2f}%)")

# report = format_efficiency_report(
#     area_covered=50,
#     quality_factor=0.85,
#     time_spent=8,
#     theoretical_width=10,
#     units={'area': 'hectares', 'width': 'meters', 'time': 'hours'}
# )
# print(report)