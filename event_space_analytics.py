def display_weather_analysis(weather_data):
    """Display weather analysis without feels like and gust indicators"""
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
