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

# Debugging: Print the API key status (remove this in production)
if openai.api_key:
    print("OpenAI API key successfully loaded.")
else:
    print("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Define the Ally (MentorBot) class
class AllyBot:
    def __init__(self):
        self.user_info = {}
        self.sia = SentimentIntensityAnalyzer()

    def greet(self):
        greetings = [
            "Hello! I'm Ally, your work buddy.",
            "Hi! Ally here, ready to help you navigate work!",
            "Hey there! It's Ally, your friendly work companion."
        ]
        return random.choice(greetings)

    def get_user_name(self):
        if 'name' not in self.user_info:
            self.user_info['name'] = st.text_input("What should I call you?")
        return f"Nice to meet you, {self.user_info['name']}!" if self.user_info['name'] else ""

    def respond_to_emotion(self, text):
        sentiment_score = self.sia.polarity_scores(text)['compound']
        if sentiment_score >= 0.5:
            response = "I'm glad you're feeling positive! Let me know how I can assist you further."
        elif sentiment_score <= -0.5:
            response = "It sounds like things might be challenging. I'm here to support you however you need."
        else:
            response = "Thanks for sharing. I'm here to provide any support or advice you need."
        return response

    def generate_feedback(self, feedback_request, style="constructive"):
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
        st.write(self.greet())
        
        # Input for user name
        name_response = self.get_user_name()
        if name_response:
            st.write(name_response)

        # Conversation input
        user_input = st.text_input("What's on your mind?", help="Type your work-related question or concern here.")

        # Define feedback and ask user for feedback style if the user enters text
        if user_input:
            user_name = self.user_info.get('name', 'there')
            st.write(f"Thanks for sharing, {user_name}.")
            st.write(self.respond_to_emotion(user_input))
            
            # Select feedback style
            st.write("How would you like my feedback delivered?")
            feedback_style = st.selectbox("Choose a style:", ["constructive", "supportive", "humor"])

            if feedback_style:
                # Generate feedback based on the user input and selected style
                ally_response = self.generate_feedback(user_input, feedback_style)

                # Display Ally's response with an appropriate emoji
                style_emoji = {
                    "constructive": "🤓",
                    "supportive": "🤗",
                    "humor": "😀"
                }
                emoji = style_emoji.get(feedback_style, "🤔")
                st.write(f"Ally says {emoji}: {ally_response}")

# Instantiate Ally and start the session
if 'ally_bot' not in st.session_state:
    st.session_state.ally_bot = AllyBot()

st.session_state.ally_bot.mentor_session()
