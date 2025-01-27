import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import random
import snowflake.connector
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
    API_KEY = "YOUR_API_KEY"  # Store this in st.secrets in production
    
    # Convert date to Unix timestamp
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    timestamp = int(dt.timestamp())
    
    # OpenWeatherMap coordinates for New York (customize for your location)
    lat = "40.7128"
    lon = "-74.0060"
    
    url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine"
    params = {
        "lat": lat,
        "lon": lon,
        "dt": timestamp,
        "appid": API_KEY,
        "units": "imperial"
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['current']['temp'],
                'conditions': data['current']['weather'][0]['main'],
                'humidity': data['current']['humidity']
            }
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None

# Function to create weather trend visualization
def create_weather_trend_plot(dates, temperatures, precipitation):
    fig = go.Figure()
    
    # Add temperature line
    fig.add_trace(go.Scatter(
        x=dates,
        y=temperatures,
        name='Temperature (°F)',
        line=dict(color='#FF9900', width=2)
    ))
    
    # Add precipitation line
    fig.add_trace(go.Scatter(
        x=dates,
        y=precipitation,
        name='Precipitation (%)',
        line=dict(color='#00BFFF', width=2),
        yaxis='y2'
    ))
    
    # Update layout
    fig.update_layout(
        title='30-Day Historical Weather Trend',
        xaxis_title='Date',
        yaxis_title='Temperature (°F)',
        yaxis2=dict(
            title='Precipitation (%)',
            overlaying='y',
            side='right'
        ),
        height=400,
        showlegend=True
    )
    
    return fig

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
            
            if weather_data:
                st.subheader("Historical Weather Conditions")
                
                # Create metrics
                col1a, col1b, col1c = st.columns(3)
                with col1a:
                    st.metric("Temperature", f"{weather_data['temperature']}°F")
                with col1b:
                    st.metric("Conditions", weather_data['conditions'])
                with col1c:
                    st.metric("Humidity", f"{weather_data['humidity']}%")
            else:
                st.warning("Using sample weather data for demonstration")
                st.metric("Typical Temperature", "72°F")
                st.metric("Typical Conditions", "Partly Cloudy")
                st.metric("Typical Humidity", "45%")
        
        with col2:
            # Generate sample data for visualization
            dates = pd.date_range(end=event_date, periods=30, freq='D')
            temperatures = [65 + random.uniform(-5, 5) for _ in range(30)]
            precipitation = [random.uniform(0, 100) for _ in range(30)]
            
            # Create and display weather trend
            fig = create_weather_trend_plot(dates, temperatures, precipitation)
            st.plotly_chart(fig, use_container_width=True)
        
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
