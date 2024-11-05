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
            "humor": f"So, funny story—{feedback}. Keep up the great work, you're making strides!"
        }
        return feedback_responses.get(delivery_preference, "constructive")

    def generate_ai_feedback(self, feedback_request, style="constructive"):
        prompt = (
            f"As a mentor and coach, provide a detailed and supportive response based on the following feedback style: {style}. "
            f"Here is the feedback content: '{feedback_request}'."
        )
        response = openai.Completion.create(
            engine="text-davinci-003",  # or "gpt-4" if you're using GPT-4
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['text'].strip()

    def mentor_session(self):
        st.write(self.greet())
        
        # Input for user name
        name_response = self.get_user_name()
        if name_response:
            st.write(name_response)

        # Conversation input
        user_input = st.text_input("Tell me what’s on your mind, or type 'exit' to end the session:")

        if user_input:
            # Respond based on sentiment
            st.write(self.respond_to_emotion(user_input))
            
            # Define feedback and ask user for feedback style
            feedback = "Your recent work shows great potential, but you might want to focus on improving X."
            st.write("How would you like feedback delivered?")
            feedback_style = st.selectbox("Choose a style:", ["constructive", "supportive", "humor"])

            if feedback_style:
                # Generate AI-enhanced feedback
                ai_feedback = self.generate_ai_feedback(feedback, feedback_style)
                st.write(ai_feedback)

# Instantiate the bot and start the mentor session
if 'mentor_bot' not in st.session_state:
    st.session_state.mentor_bot = MentorBot()

st.session_state.mentor_bot.mentor_session()

