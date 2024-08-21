import streamlit as st
import openai
import pandas as pd
import requests
from io import BytesIO

# Initialize OpenAI with your API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# GitHub file details
username = "jamesnicholls4m"
repo = "wordcloud-application"
branch = "main"
file_path = "NATA A2Z List - August 2024 - v1.xlsx"
file_url = f"https://github.com/{username}/{repo}/raw/{branch}/{file_path}"

# Function to load Excel file from GitHub
@st.cache
def load_data():
    r = requests.get(file_url)
    data = BytesIO(r.content)
    df = pd.read_excel(data)
    return df

# Function to interact with GPT-4 model to search for the best match
def search_a2z_list(input_text, df):
    prompt = f"Find the best match for the following input: {input_text}"
    
    # Query the model
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=prompt,
        max_tokens=200
    )
    
    response_text = response.choices[0].text.strip()
    
    # Example of how to parse the response, assuming it gives specific 'Name' and 'Phone' tokens.
    # This part will depend on how the response is formatted by your specific prompt and model.
    if "Name:" in response_text and "Phone:" in response_text:
        name = response_text.split("Name:")[1].split("Phone:")[0].strip()
        phone = response_text.split("Phone:")[1].strip()
    else:
        name = "Not found"
        phone = "Not found"
    
    return name, phone

# Load data
df = load_data()

# Streamlit App configuration
st.title("A2Z List Search Application")
user_input = st.text_input("Enter query:", "Type here...")
search_button = st.button("Search A2Z List")

if search_button:
    if user_input:
        name, phone = search_a2z_list(user_input, df)
        st.write(f"**Name:** {name}")
        st.write(f"**Phone:** {phone}")
    else:
        st.write("Please enter a query to search the A2Z List.")
