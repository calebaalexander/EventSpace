import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta, date
import json
from dateutil.relativedelta import relativedelta

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
    .timeline-card {
        background: #fff5f7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #ffb6c1;
    }
    .timeline-month {
        color: #ff1493;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

def get_weather_data(date_str):
    """Get weather data using Visual Crossing API"""
    try:
        api_key = "KRLYNZU9RASBDGAB3688F8WPL"
        base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        url = f"{base_url}/12051/{date_str}"
        
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

def display_wedding_timeline(event_date, client_name):
    """Display wedding planning timeline"""
    st.header("📅 Wedding Planning Timeline")
    
    today = date.today()
    wedding_date = datetime.strptime(event_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date()
    months_until = (wedding_date.year - today.year) * 12 + wedding_date.month - today.month
    
    timeline_tasks = {
        12: [
            "Have conversation with wedding stakeholders",
            "Set your wedding budget",
            "Research and tour venues",
            "Begin pulling style inspiration"
        ],
        11: [
            "Touch base with priority vendors",
            "Finalize your date and venue",
            "Start booking key vendors",
            "Determine your wedding party"
        ],
        10: [
            "Start shopping for wedding attire",
            "Book hotel room blocks",
            "Research transportation options"
        ],
        9: [
            "Choose save-the-dates",
            "Plan your entertainment",
            "Begin booking rentals",
            "Schedule engagement photos"
        ],
        8: [
            "Create wedding website",
            "Send save-the-dates",
            "Start registry process",
            "Research honeymoon destinations"
        ],
        7: [
            "Shop for wedding party attire",
            "Finalize vendor contracts",
            "Book rehearsal dinner venue"
        ],
        6: [
            "Begin premarital counseling",
            "Shop for wedding bands",
            "Book hair and makeup team",
            "Complete invitation suite"
        ],
        5: [
            "Order invitations",
            "Plan your menu",
            "Buy additional outfits",
            "Finalize honeymoon plans"
        ],
        4: [
            "Send shower invites",
            "Create music wishlist",
            "Plan personalized details",
            "Finalize ceremony program"
        ],
        3: [
            "Attend wedding shower",
            "Purchase thank you gifts",
            "Schedule hair/makeup trial",
            "Send formal invitations"
        ],
        2: [
            "Enjoy bachelor/bachelorette party",
            "Start writing vows",
            "Plan favors and welcome bags"
        ],
        1: [
            "Apply for marriage license",
            "Final dress fittings",
            "Create seating chart",
            "Final vendor meetings"
        ],
        0: [
            "Rehearsal dinner",
            "Welcome party",
            "The Big Day!",
            "Begin your happily ever after"
        ]
    }

    # Create timeline display
    for i in range(min(13, months_until + 1)):
        month_date = wedding_date - relativedelta(months=i)
        month_name = month_date.strftime("%B %Y")
        
        with st.expander(f"{i} Months Out - {month_name}", expanded=(i == months_until)):
            tasks = timeline_tasks.get(i, [])
            for task in tasks:
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    st.checkbox("", key=f"{i}-{task}")
                with col2:
                    st.write(task)

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
        
        with col2:
            event_type = st.selectbox(
                "Event Type",
                options=["Wedding", "Corporate Event", "Birthday", "Conference", "Other"]
            )
            attendance = st.number_input(
                "Expected Attendance",
                min_value=1,
                step=1
            )
        
        caterer = st.text_input("Caterer/Vendor Name")
        
        submit_button = st.form_submit_button("Submit Event Details")
    
    if submit_button:
        # Show success message
        st.success("Event details submitted successfully!")
        
        # Get weather data
        with st.spinner("Fetching weather data..."):
            date_str = event_date.strftime("%Y-%m-%d")
            weather_data = get_weather_data(date_str)
        
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
            
            with summary_col2:
                st.write(f"**Expected Attendance:** {attendance}")
                st.write(f"**Caterer:** {caterer}")
            
            # Display wedding timeline if event type is Wedding
            if event_type == "Wedding":
                display_wedding_timeline(event_date, client_name)

if __name__ == "__main__":
    main()
