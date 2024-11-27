import streamlit as st
from openai import OpenAI
import random

def eat_your_fruits():
    for i in range(10):
        print("I'm eating fruits", i)

st.set_page_config(page_title="Chat with Meteo Buddy", layout="centered", initial_sidebar_state="auto")
st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
    )

# Sidebar for API key input
st.sidebar.title("API Key Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to fetch response from OpenAI API
def fetch_response(query):
    if not api_key:
        return "Please enter your OpenAI API key in the sidebar."
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": query}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

# React to user input
if prompt := st.chat_input("Ask me anything..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    predicted_temperature = random.randint(6, 30)
    predicted_weather = random.choice(["sunny", "cloudy"])
    predicted_wind_speed = random.randint(3, 8)
    predicted_humidity = random.randint(50, 80)
    predicted_pressure = random.randint(700, 1013)

    print(f"""
        Predicted Temperature: {predicted_temperature}°C
        Predicted Weather: {predicted_weather}
        Predicted Wind Speed: {predicted_wind_speed} m/s
        Predicted Humidity: {predicted_humidity}%
        Predicted Pressure: {predicted_pressure} hPa

    """)

    # Fetch response from OpenAI API
    response = fetch_response(
        f"""
        The following is a conversation with Meteo Buddy, an AI assistant for weather predictions and meteorology insights.
        The assistant is knowledgeable, precise, and eager to help with weather-related queries.
        User: {prompt}
        Context:

        Weather Data: Meteo Buddy uses real-time data from a reliable weather API to provide accurate forecasts.
        Predicted Temperature: {predicted_temperature}°C
        Predicted Weather: {predicted_weather}
        Predicted Wind Speed: {predicted_wind_speed} m/s
        Predicted Humidity: {predicted_humidity}%
        Predicted Pressure: {predicted_pressure} hPa
        Technical Insights: The assistant can explain complex meteorological concepts and answer technical questions.
        Additional Features: Meteo Buddy can offer advice on weather preparedness and safety tips.
        AI:"
        """ 
        )
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})