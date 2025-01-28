import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta, date
import json
from dateutil.relativedelta import relativedelta
import calendar

# Configure the Streamlit page
st.set_page_config(
    page_title="Event Space Analytics",
    page_icon="🎉",
    layout="wide"
)

# Add custom CSS with better styling
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
        padding: 1rem;
        border-radius: 0.5rem;
        background: #fff5f7;
        margin: 0.5rem 0;
        border: 1px solid #ffb6c1;
    }
    .timeline-month {
        font-size: 1.2rem;
        font-weight: bold;
        color: #ff69b4;
        margin-bottom: 0.5rem;
    }
    .timeline-task {
        padding: 0.5rem;
        margin: 0.25rem 0;
        background: white;
        border-radius: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)

def get_weather_data(location, date_str, api_key):
    """Get weather data using Visual Crossing API"""
    try:
        base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        url = f"{base_url}/{location}/{date_str}"
        
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

def generate_timeline(client_name, wedding_date):
    """Generate wedding planning timeline"""
    today = date.today()
    wedding = datetime.strptime(wedding_date, '%Y-%m-%d').date()
    months_until_wedding = (wedding.year - today.year) * 12 + wedding.month - today.month
    
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
    
    st.header("📅 Your Custom Wedding Timeline", divider=True)
    st.write(f"Planning timeline for {client_name}'s wedding on {wedding_date}")
    
    # Generate monthly timeline
    for i in range(min(13, months_until_wedding + 1)):
        month_date = wedding - relativedelta(months=i)
        month_name = month_date.strftime("%B %Y")
        
        with st.expander(f"{i} Months Out - {month_name}"):
            tasks = timeline_tasks.get(i, [])
            for task in tasks:
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    st.checkbox("", key=f"{i}-{task}")
                with col2:
                    st.write(task)

def main():
    st.title("📈 Event Space Analytics Dashboard")
    
    # Move API key to sidebar
    with st.sidebar:
        st.subheader("Configuration")
        api_key = st.text_input("Visual Crossing API Key", 
                               value="KRLYNZU9RASBDGAB3688F8WPL",
                               type="password")
        location = st.text_input("Default Location (ZIP or City)", 
                               value="12051")
    
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["Event Details", "Wedding Timeline"])
    
    with tab1:
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
            
            if weather_data and event_type == "Wedding":
                # Generate timeline
                generate_timeline(client_name, date_str)
            
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
    
    with tab2:
        st.header("Wedding Planning Timeline Generator")
        timeline_col1, timeline_col2 = st.columns(2)
        
        with timeline_col1:
            timeline_name = st.text_input("Enter Your Name")
        with timeline_col2:
            timeline_date = st.date_input(
                "Select Wedding Date",
                min_value=date.today(),
                value=date.today() + timedelta(days=365)
            )
        
        if st.button("Generate Timeline"):
            if timeline_name and timeline_date:
                generate_timeline(timeline_name, timeline_date.strftime("%Y-%m-%d"))
            else:
                st.warning("Please enter your name and wedding date to generate a timeline.")

if __name__ == "__main__":
    main()
