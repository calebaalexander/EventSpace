import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta, date
import json

# Configure the Streamlit page
st.set_page_config(
    page_title="Event Space Analytics",
    page_icon="🎉",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .weather-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background: #f8f9fa;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def get_weather_data(location, date_str, api_key):
    """
    Get weather data using Visual Crossing API
    """
    try:
        # Format the API URL
        base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        url = f"{base_url}/{location}/{date_str}"
        
        params = {
            "unitGroup": "us",  # US units
            "key": api_key,
            "contentType": "json",
            "include": "days"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error parsing weather response: {str(e)}")
        return None

def celsius_to_fahrenheit(celsius):
    """Convert celsius to fahrenheit"""
    return (celsius * 9/5) + 32

def get_weather_icon(condition):
    """Map weather conditions to emojis"""
    condition = condition.lower()
    icons = {
        'clear': '☀️',
        'sunny': '☀️',
        'partly cloudy': '⛅',
        'cloudy': '☁️',
        'rain': '🌧️',
        'snow': '🌨️',
        'thunderstorm': '⛈️',
        'fog': '🌫️',
        'wind': '💨'
    }
    
    for key in icons:
        if key in condition:
            return icons[key]
    return '🌤️'  # default icon

def display_weather_analysis(weather_data, event_date):
    """Enhanced weather analysis display"""
    if weather_data and 'days' in weather_data and len(weather_data['days']) > 0:
        day_data = weather_data['days'][0]
        
        st.subheader("📊 Weather Forecast Analysis")
        
        # Create three columns for weather metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Temperature",
                f"{day_data['temp']}°F",
                delta=f"Feels like {day_data['feelslike']}°F"
            )
            
        with col2:
            st.metric(
                "Humidity",
                f"{day_data['humidity']}%",
                delta=None
            )
            
        with col3:
            st.metric(
                "Precipitation",
                f"{day_data['precip']} in",
                delta=f"{day_data['precipprob']}% chance" if 'precipprob' in day_data else None
            )
            
        with col4:
            st.metric(
                "Wind",
                f"{day_data['windspeed']} mph",
                delta=f"Gusts {day_data['windgust']} mph" if 'windgust' in day_data else None
            )
        
        # Weather condition card
        icon = get_weather_icon(day_data['conditions'])
        st.markdown(
            f"""
            <div class="weather-card">
                <h3 style="margin-bottom:1rem;">{icon} Weather Conditions</h3>
                <p style="font-size:1.1em;">{day_data['conditions']}</p>
                <p>Description: {day_data['description']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Add weather recommendations
        st.subheader("🎯 Event Planning Recommendations")
        recommendations = generate_weather_recommendations(day_data)
        for rec in recommendations:
            st.write(f"• {rec}")
            
        # Historical comparison if available
        if 'historical' in weather_data:
            st.subheader("📈 Historical Comparison")
            # Add historical analysis here
            
    else:
        st.warning("Weather data not available for the selected date.")

def generate_weather_recommendations(weather_data):
    """Generate event planning recommendations based on weather"""
    recommendations = []
    
    # Temperature recommendations
    if weather_data['temp'] < 50:
        recommendations.append("Consider providing outdoor heaters or moving indoors")
        recommendations.append("Prepare warm beverages for guests")
    elif weather_data['temp'] > 85:
        recommendations.append("Ensure adequate shade and cooling options")
        recommendations.append("Provide plenty of water and cold beverages")
        
    # Precipitation recommendations
    if weather_data['precipprob'] > 30:
        recommendations.append("Have a backup indoor location or tent arrangement")
        recommendations.append("Consider providing umbrellas or covered walkways")
        
    # Wind recommendations
    if weather_data['windspeed'] > 15:
        recommendations.append("Secure all decorations and lightweight furniture")
        recommendations.append("Consider wind barriers for outdoor areas")
        
    # Humidity recommendations
    if weather_data['humidity'] > 70:
        recommendations.append("Consider providing fans or dehumidifiers for comfort")
    
    return recommendations

def main():
    st.title("📈 Event Space Analytics Dashboard")
    
    # Move API key to sidebar
    with st.sidebar:
        st.subheader("Configuration")
        api_key = st.text_input("Visual Crossing API Key", 
                               value="KRLYNZU9RASBDGAB3688F8WPL",  # Default key from example
                               type="password")
        location = st.text_input("Default Location (ZIP or City)", 
                               value="12051")  # Default location from example
    
    # Create main form
    with st.form("event_form"):
        st.subheader("Event Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.text_input("Client Name")
            event_date = st.date_input(
                "Event Date",
                min_value=date.today(),
                value=date.today() + timedelta(days=30)
            )
            event_type = st.selectbox(
                "Event Type",
                options=["Wedding", "Corporate Event", "Birthday", "Conference", "Other"]
            )
        
        with col2:
            total_cost = st.number_input(
                "Total Cost ($)",
                min_value=0.0,
                step=100.0,
                format="%.2f"
            )
            attendance = st.number_input(
                "Expected Attendance",
                min_value=1,
                step=1
            )
            venue_location = st.selectbox(
                "Venue Location",
                options=["Indoor", "Outdoor", "Both"]
            )
        
        caterer = st.text_input("Caterer/Vendor Name")
        
        submit_button = st.form_submit_button("Submit Event Details")
    
    if submit_button:
        if not api_key:
            st.error("Please enter your Visual Crossing API key in the sidebar.")
            return
            
        # Show success message
        st.success("Event details submitted successfully!")
        
        # Get weather data
        with st.spinner("Fetching weather data..."):
            date_str = event_date.strftime("%Y-%m-%d")
            weather_data = get_weather_data(location, date_str, api_key)
        
        if weather_data:
            # Display weather analysis
            display_weather_analysis(weather_data, event_date)
            
            # Display event summary
            st.header("📋 Event Summary")
            summary_col1, summary_col2 = st.columns(2)
            
            with summary_col1:
                st.write(f"**Client:** {client_name}")
                st.write(f"**Event Type:** {event_type}")
                st.write(f"**Date:** {event_date.strftime('%B %d, %Y')}")
                st.write(f"**Venue Type:** {venue_location}")
            
            with summary_col2:
                st.write(f"**Total Cost:** ${total_cost:,.2f}")
                st.write(f"**Expected Attendance:** {attendance}")
                st.write(f"**Caterer:** {caterer}")
                st.write(f"**Location:** {weather_data.get('resolvedAddress', location)}")

if __name__ == "__main__":
    main()
