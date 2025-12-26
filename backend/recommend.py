import pandas as pd

def recommend_for_high_pollution(age, aqi):
    """
    Takes user age and predicted AQI, returns health recommendations.
    This is what final.py and gui.py actually call!
    """
    advice = []

    # Determine AQI category (standard EPA scale)
    if aqi <= 50:
        category = "Good"
        advice.append("Air quality is good. Normal activities OK.")
    elif aqi <= 100:
        category = "Moderate"
        advice.append("Unusually sensitive people should reduce prolonged outdoor exertion.")
    elif aqi <= 150:
        category = "Unhealthy for Sensitive Groups"
        advice.append("Sensitive groups should reduce outdoor exertion.")
    elif aqi <= 200:
        category = "Unhealthy"
        advice.append("Everyone should reduce prolonged outdoor exertion.")
    elif aqi <= 300:
        category = "Very Unhealthy"
        advice.append("Everyone should avoid prolonged outdoor exertion.")
    else:
        category = "Hazardous"
        advice.append("STAY INDOORS! Health warning of emergency conditions.")

    # Age-specific recommendations
    if age < 12:
        advice.append("CHILDREN: Avoid outdoor activities, stay in well-ventilated indoor spaces.")
    elif age >= 60:
        advice.append("SENIORS: Stay indoors, use air purifier if available.")
    elif 12 <= age < 18:
        advice.append("TEENS: No outdoor sports or heavy exercise.")

    # Additional advice for bad air
    if aqi > 150:
        advice.append("Wear N95 or KN95 mask if you must go outside.")
        advice.append("Keep windows closed, use air purifier indoors.")

    return f"\nAQI Category: {category} (AQI: {int(aqi)})\n\n" + "\n".join(advice)

def classify_concern_level(score):
    """
    Converts the 0-10 concern score into a binary High/Low classification.
    Adjust the threshold (e.g., 5) as needed.
    """
    if score > 5:
        return 'High'
    else:
        return 'Low'

def generate_advice_by_concern(concern_score, user_data, privacy_mode=False):
    """
    Triggers advice based on the Concern Level (High/Low) instead of raw AQI.
    """
    concern_level = classify_concern_level(concern_score)
    
    advice = []
    advice.append(f"--- Report for Concern Score: {concern_score}/10 ({concern_level.upper()}) ---")

    if concern_level == 'High':
        advice.append("🚨 STATUS: HIGH CONCERN LEVEL")
        advice.append("General Actions:")
        advice.append("- The perceived pollution risk is high. Assume poor air quality.")
        advice.append("- Wear a mask (N95) if heading out.")
        
        if not privacy_mode:
            if user_data.get('Respiratory_difficulties') == 'Yes':
                advice.append("‼️ HEALTH: You have respiratory issues. High concern levels imply you should stay indoors.")
            
            if user_data.get('Parent') == 'Yes':
                advice.append("👨‍👩‍👧 FAMILY: Prevent children from playing outside until concern levels drop.")
                
            
            age = str(user_data.get('Age_group'))
            if '55' in age or '65' in age:
                advice.append("👴 SENIOR: High concern warrants strict indoor stay for older adults.")
        else:
            advice.append("(Specific health recommendations hidden - Privacy Mode ON)")

    else: # Low Concern
        advice.append("✅ STATUS: LOW CONCERN LEVEL")
        advice.append("- Perceived pollution risk is low.")
        advice.append("- Standard outdoor activities are likely safe.")
        
        if not privacy_mode and user_data.get('Respiratory_difficulties') == 'Yes':
            advice.append("NOTE: Even with low concern, keep your inhaler nearby just in case.")

    return "\n".join(advice)