import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from openai import OpenAI
from config import OPENAI_API_KEY

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

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
    if r.status_code == 200:
        data = BytesIO(r.content)
        df = pd.read_excel(data)
        return df
    else:
        st.error("Failed to load the file from GitHub.")
        return pd.DataFrame()

# Function to interact with GPT-4 model to search for the best match
def search_a2z_list(input_text, df):
    # Convert DataFrame to string for the prompt
    data_sample = df.head(10).to_string(index=False)
    prompt = f"Given the following data, find the best match for the input query:\n\nData:\n{data_sample}\n\nQuery: {input_text}"

    # Define the conversation for the chat model
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    # Query the GPT-4 model
    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_text = response.choices[0].message["content"].strip()

    # Simplistic parsing, adjust based on actual response format
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
