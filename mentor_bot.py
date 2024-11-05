# -*- coding: utf-8 -*-
"""Mentor Chatbot with Streamlit and OpenAI API Integration"""

import os
import random
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st
import openai

# Ensure the necessary nltk data is downloaded
nltk.download('vader_lexicon')

# Set the OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the MentorBot class
class MentorBot:
    def __init__(self):
        self.user_info = {}
        self.sia = SentimentIntensityAnalyzer()

    def greet(self):
        greetings = [
            "Hello! I'm here to support you on your journey.",
            "Hey there! How can I help you today?",
            "Hi! I'm here to listen and assist you."
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

    def deliver_feedback(self, feedback, delivery_preference="constructive"):
        feedback_responses = {
            "constructive": f"I have some constructive feedback for you: {feedback}. Remember, feedback is here to help you grow.",
            "supportive": f"Here’s something I think could help you shine even more: {feedback}. You’re already doing so well!",
            "humor": f"So, funny story—{feedback}. Keep up the great work,
