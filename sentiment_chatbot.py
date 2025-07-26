import streamlit as stw
from textblob import TextBlob
import random
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download NLTK data 
nltk.download('vader_lexicon')

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Chatbot responses
POSITIVE_RESPONSES = [
    "I'm glad you're happy! 😊 How can I assist you further?",
    "Great to hear you're positive! What else can I do?",
    "Your enthusiasm is contagious! 🌟 How may I help?"
]

NEGATIVE_RESPONSES = [
    "I'm sorry you're feeling this way. 😔 How can I help?",
    "That sounds tough. Let me try to make it better.",
    "I'm here to help with whatever's bothering you."
]

NEUTRAL_RESPONSES = [
    "Got it. How can I assist you today?",
    "I see. What would you like help with?",
    "Understood. What can I do for you?"
]

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = analyzer.polarity_scores(text)
    compound_score = analysis['compound']
    
    if compound_score >= 0.1:
        return "positive", compound_score
    elif compound_score <= -0.1:
        return "negative", compound_score
    else:
        return "neutral", compound_score

# Function to generate chatbot response
def get_chatbot_response(sentiment):
    if sentiment == "positive":
        return random.choice(POSITIVE_RESPONSES)
    elif sentiment == "negative":
        return random.choice(NEGATIVE_RESPONSES)
    else:
        return random.choice(NEUTRAL_RESPONSES)

# Streamlit UI
stw.title("🤖 Sentiment-Aware Chatbot")
stw.write("Chat with me! I can understand your emotions.")

# Initialize chat history
if "messages" not in stw.session_state:
    stw.session_state.messages = []

# Display chat messages
for message in stw.session_state.messages:
    with stw.chat_message(message["role"]):
        stw.markdown(message["content"])

# Chat input
if prompt := stw.chat_input("Type your message..."):
    # Add user message to chat history
    stw.session_state.messages.append({"role": "user", "content": prompt})
    with stw.chat_message("user"):
        stw.markdown(prompt)
    
    # Analyze sentiment
    sentiment, score = analyze_sentiment(prompt)
    
    # Get chatbot response
    response = get_chatbot_response(sentiment)
    
    # Add sentiment analysis info
    sentiment_info = f"*[Detected: {sentiment} (score: {score:.2f})]*"
    full_response = f"{response}\n\n{sentiment_info}"
    
    # Add assistant response to chat history
    stw.session_state.messages.append({"role": "assistant", "content": full_response})
    with stw.chat_message("assistant"):
        stw.markdown(full_response)