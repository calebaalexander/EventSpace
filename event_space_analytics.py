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
    </style>
    """, unsafe_allow_html=True)

def get_weather_data(location, date_str):
    """Get weather data using Visual Crossing API"""
    try:
        api_key = "KRLYNZU9RASBDGAB3688F8WPL"  # Hardcoded API key
        base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        url = f"{base_url}/12051/{date_str}"  # Hardcoded location
        
        params = {
            "unitGroup": "us",
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

def display_weather_analysis(weather_data):
    """Enhanced weather analysis display"""
    if weather_data and 'days' in weather_data and len(weather_data['days']) > 0:
        day_data = weather_data['days'][0]
        
        st.header("📊 Weather Forecast Analysis")
        
        # Create four columns for weather metrics
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
            precip_chance = day_data.get('precipprob', 0)
            precip_amount = day_data.get('precip', 0)
            st.metric(
                "Precipitation",
                f"{precip_chance}% ({precip_amount} in)",
                delta=None
            )
            
        with col4:
            wind_speed = day_data.get('windspeed', 0)
            wind_gust = day_data.get('windgust', 0)
            st.metric(
                "Wind",
                f"{wind_speed} mph",
                delta=f"Gusts {wind_gust} mph" if wind_gust else None
            )
        
        # Weather condition card
        st.markdown(
            f"""
            <div class="weather-card">
                <h3>☁️ Weather Conditions</h3>
                <p>{day_data['conditions']}</p>
                <p><strong>Description:</strong> {day_data.get('description', 'No description available')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

def main():
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
        # Show success message
        st.success("Event details submitted successfully!")
        
        # Get weather data
        with st.spinner("Fetching weather data..."):
            date_str = event_date.strftime("%Y-%m-%d")
            weather_data = get_weather_data("12051", date_str)
        
        if weather_data:
            # Display weather analysis
            display_weather_analysis(weather_data)
            
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

if __name__ == "__main__":
    main()
