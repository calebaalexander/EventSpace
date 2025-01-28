import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta, date
import json
from dateutil.relativedelta import relativedelta

# [Previous code remains the same until the weather data function]

def get_weather_data(date_str):
    """Get weather data using Visual Crossing API"""
    try:
        api_key = "KRLYNZU9RASBDGAB3688F8WPL"
        base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        
        # Explicitly set location to 12051
        location = "12051"
        url = f"{base_url}/{location}/{date_str}"
        
        params = {
            "unitGroup": "us",
            "key": api_key,
            "contentType": "json",
            "include": "days"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Print response for debugging
        print(f"Weather API Response: {response.json()}")
        
        return response.json()
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error parsing weather response: {str(e)}")
        return None

def display_weather_analysis(weather_data):
    """Display weather analysis"""
    if weather_data and 'days' in weather_data and len(weather_data['days']) > 0:
        day_data = weather_data['days'][0]
        
        st.header("📊 Weather Forecast Analysis")
        
        # Create four columns for weather metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Temperature",
                f"{day_data['temp']}°F",
                delta=None
            )
            
        with col2:
            st.metric(
                "Humidity",
                f"{day_data['humidity']}%",
                delta=None
            )
            
        with col3:
            precip_chance = day_data.get('precipprob', 0)
            precip_amount = day_data.get('precip', 0)
            st.metric(
                "Precipitation",
                f"{precip_chance}% ({precip_amount} in)",
                delta=None
            )
            
        with col4:
            wind_speed = day_data.get('windspeed', 0)
            st.metric(
                "Wind",
                f"{wind_speed} mph",
                delta=None
            )
        
        # Weather condition card with improved description handling
        conditions = day_data.get('conditions', 'No conditions available')
        description = day_data.get('description', conditions)  # Use conditions as fallback
        
        st.markdown(
            f"""
            <div class="weather-card">
                <h3>☁️ Weather Conditions</h3>
                <p>{conditions}</p>
                <p><strong>Description:</strong> {description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# [Previous timeline code remains the same]

# Main application
st.title("Event Space Analytics")

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
    
    with col2:
        event_type = st.selectbox(
            "Event Type",
            options=["Wedding", "Corporate Event", "Birthday", "Conference", "Other"]
        )
        # Modified attendance input with default 100 and no +/-
        attendance = st.number_input(
            "Expected Attendance",
            min_value=1,
            value=100,
            step=1,
            format="%d"  # Use integer format
        )
    
    caterer = st.text_input("Caterer/Vendor Name")
    
    submit_button = st.form_submit_button("Submit Event Details")

# [Rest of the code remains the same]
