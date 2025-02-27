import streamlit as st
import requests
from datetime import datetime

# Function to fetch weather data
def get_weather(city):
    API_KEY = "f8cb952227a9226d7088520604acec5a"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    
    if response.get("cod") != 200:
        return None
    
    weather = {
        "temp": response["main"]["temp"],
        "condition": response["weather"][0]["main"],
        "icon": f"http://openweathermap.org/img/wn/{response['weather'][0]['icon']}@2x.png"
    }
    return weather

# Function to fetch real-time events from Eventbrite
def get_real_time_events(state):
    EVENTBRITE_API_KEY = "OV2PT6EZSUWH6KKEG6F2"
    url = f"https://www.eventbriteapi.com/v3/events/search/?q={state}&location.address={state}&token={EVENTBRITE_API_KEY}"
    response = requests.get(url).json()
    
    events = []
    if "events" in response:
        for event in response["events"][:5]:  # Limit to 5 events
            events.append(f"{event['name']['text']} - {event['start']['local'][:10]}")
    
    return events

# Streamlit UI
st.title("Northeast India Travel Advisor")
st.sidebar.header("Plan Your Trip")

# Select state
destination = st.sidebar.selectbox("Select State", [
    "Arunachal Pradesh", "Assam", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Tripura"
])
travel_date = st.sidebar.date_input("Select Travel Date", datetime.today())

# Fetch weather data
weather = get_weather(destination)
if weather:
    st.markdown(f"### Weather in {destination}")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(weather["icon"], width=80)
    with col2:
        st.write(f"**{weather['condition']}**")
        st.write(f"Temperature: {weather['temp']}°C")
else:
    st.warning("Weather data unavailable")

# Display real-time events
events = get_real_time_events(destination)
if events:
    st.markdown("### Upcoming Events")
    for event in events:
        st.write(f"- {event}")
else:
    st.warning("No real-time events found")

# Suggest alternative activities based on weather
if weather:
    if "Rain" in weather["condition"]:
        st.markdown("### Suggested Rainy Day Activities")
        st.write("- Visit museums and cultural centers")
        st.write("- Try local cafes and indoor markets")
    else:
        st.markdown("### Suggested Outdoor Activities")
        st.write("- Explore scenic trails and viewpoints")
        st.write("- Attend local festivals and markets")
