
import streamlit as st
import openai
import json

# Load user preferences from JSON file
def load_preferences(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Save user preferences to JSON file
def save_preferences(file_path, preferences):
    with open(file_path, 'w') as f:
        json.dump(preferences, f, indent=4)

# Initialize OpenAI API
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Generate response using OpenAI API
def generate_response(prompt, preferences):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Load preferences
preferences_file = 'marketing_assistant_memory.json'
preferences = load_preferences(preferences_file)

# Streamlit app
st.title("Marketing Assistant")

# Chat interface
st.subheader("Chat with your assistant")
user_input = st.text_input("You: ", "")
if st.button("Send"):
    if user_input:
        prompt = f"{preferences['user_preferences']['role']} who prefers {preferences['user_preferences']['tone']} responses: {user_input}"
        response = generate_response(prompt, preferences)
        st.text_area("Assistant:", value=response, height=200)

# Memory control
st.subheader("Memory Control")
if st.button("View Preferences"):
    st.json(preferences)

if st.button("Delete Preferences"):
    preferences = {}
    save_preferences(preferences_file, preferences)
    st.success("Preferences deleted.")

# Save updated preferences
save_preferences(preferences_file, preferences)
