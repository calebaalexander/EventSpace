import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random
from datetime import date

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
    </style>
    """, unsafe_allow_html=True)

# Function to get historical weather data
def get_historical_weather(date_str, location="New York"):
    """
    Get historical weather data using OpenWeatherMap API
    Replace 'YOUR_API_KEY' with actual API key
    """
    # For demo purposes, return mock data
    return {
        'temperature': 72,
        'conditions': 'Partly Cloudy',
        'humidity': 45
    }

# Main application
def main():
    st.title("Event Space Analytics Dashboard")
    
    # Create main form
    with st.form("event_form"):
        st.subheader("Event Details")
        
        # Create two columns for form layout
        col1, col2 = st.columns(2)
        
        with col1:
            # Client Information
            client_name = st.text_input("Client Name")
            event_date = st.date_input(
                "Event Date",
                min_value=date.today(),
                value=date.today() + timedelta(days=30)
            )
            event_type = st.selectbox(
                "Event Type",
                options=["Wedding", "Business", "Personal"]
            )
        
        with col2:
            # Event Details
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
            caterer = st.text_input("Caterer/Vendor Name")
        
        # Submit button
        submit_button = st.form_submit_button("Submit Event Details")
    
    # Handle form submission
    if submit_button:
        # Display confirmation
        st.success("Event details submitted successfully!")
        
        # Weather Analysis Section
        st.header("Weather Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Get weather data for selected date
            weather_data = get_historical_weather(str(event_date))
            
            st.subheader("Historical Weather Conditions")
            
            # Create metrics
            col1a, col1b, col1c = st.columns(3)
            with col1a:
                st.metric("Temperature", f"{weather_data['temperature']}°F")
            with col1b:
                st.metric("Conditions", weather_data['conditions'])
            with col1c:
                st.metric("Humidity", f"{weather_data['humidity']}%")
        
        with col2:
            # Generate sample data for visualization
            dates = pd.date_range(end=event_date, periods=30, freq='D')
            temperatures = [65 + random.uniform(-5, 5) for _ in range(30)]
            
            # Create DataFrame for plotting
            weather_df = pd.DataFrame({
                'Date': dates,
                'Temperature': temperatures
            })
            
            # Use Streamlit's native line chart
            st.line_chart(weather_df.set_index('Date'))
        
        # Event Summary
        st.header("Event Summary")
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.write(f"**Client:** {client_name}")
            st.write(f"**Event Type:** {event_type}")
            st.write(f"**Date:** {event_date.strftime('%B %d, %Y')}")
        
        with summary_col2:
            st.write(f"**Total Cost:** ${total_cost:,.2f}")
            st.write(f"**Expected Attendance:** {attendance}")
            st.write(f"**Caterer:** {caterer}")

# Run the application
if __name__ == "__main__":
    main()
