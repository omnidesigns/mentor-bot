# -*- coding: utf-8 -*-
"""Ally - Your Work Buddy with Streamlit and OpenAI API Integration"""

import os
import random
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st
import openai
from openai.error import RateLimitError

# Ensure the necessary nltk data is downloaded
nltk.download('vader_lexicon')

# Set the OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# CSS for robot icon and styling
st.markdown(
    """
    <style>
    .robot-icon {
        display: flex;
        align-items: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: #b51963; /* green color for the robot */
        margin-bottom: 15px;
    }
    .robot-head {
        display: inline-block;
        width: 40px;
        height: 40px;
        background-color: #b51963;
        border-radius: 8px;
        position: relative;
        margin-right: 10px;
    }
    .robot-head::before, .robot-head::after {
        content: '';
        position: absolute;
        width: 6px;
        height: 6px;
        background-color: #FFFFFF; /* white for eyes */
        top: 10px;
        border-radius: 50%;
    }
    .robot-head::before {
        left: 8px;
    }
    .robot-head::after {
        right: 8px;
    }
    .robot-mouth {
        position: absolute;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
        width: 16px;
        height: 4px;
        background-color: #FFFFFF; /* white mouth */
        border-radius: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the Ally (MentorBot) class
class AllyBot:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def greet(self):
        greetings = [
            "Hello! I'm Ally, your work buddy.",
            "Hi! Ally here, ready to help you navigate work!",
            "Hey there! It's Ally, your friendly work companion."
        ]
        return random.choice(greetings)

    def get_user_name(self):
        # Check if the user's name is stored in session state
        if 'name' not in st.session_state or not st.session_state['name']:
            st.session_state['name'] = st.text_input("What should I call you?")
        return st.session_state['name']

    def generate_feedback(self, feedback_request, style="constructive"):
        # Generate feedback based on the input and selected style
        prompt = (
            f"As a mentor and work buddy, respond with a {style} style to the following work-related concern: '{feedback_request}'."
            f" Provide detailed support and advice in a {style} tone."
        )
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Ally, a supportive and insightful work buddy."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response['choices'][0]['message']['content'].strip()
        
        except RateLimitError:
            return "I'm currently at my usage limit. Please try again later."

    def mentor_session(self):
        # Display robot icon and greeting message
        st.markdown('<div class="robot-icon"><div class="robot-head"><div class="robot-mouth"></div></div>Ally</div>', unsafe_allow_html=True)
        st.write(self.greet())
        
        # Get or prompt for the user's name
        user_name = self.get_user_name()
        
        # Display the name prompt until user has entered their name
        if not user_name:
            st.stop()  # Stop the execution until the user enters a name

        st.write(f"Nice to meet you, {user_name}!")

        # Prompt for the user's main question or concern
        user_input = st.text_input("What's on your mind?", help="Type your work-related question or concern here.")

        # If there is user input, proceed to feedback style selection
        if user_input:
            st.write(f"Thanks for sharing, {user_name}.")
            
            # Allow user to select feedback style
            st.write("How would you like my feedback delivered?")
            feedback_style = st.selectbox("Choose a style:", ["constructive", "supportive", "humor"])

            if feedback_style:
                # Generate Ally's response with the selected style
                ally_response = self.generate_feedback(user_input, feedback_style)

                # Add an emoji for each feedback style and personalize with the user's name
                style_emoji = {
                    "constructive": "🤓",
                    "supportive": "🤗",
                    "humor": "😀"
                }
                emoji = style_emoji.get(feedback_style, "🤔")
                st.write(f"Ally says {emoji}: {ally_response} {user_name}")

# Instantiate Ally and start the session
if 'ally_bot' not in st.session_state:
    st.session_state.ally_bot = AllyBot()

st.session_state.ally_bot.mentor_session()
