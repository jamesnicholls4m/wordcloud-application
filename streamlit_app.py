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
@st.cache()
def load_data():
    r = requests.get(file_url)
    if r.status_code == 200:
        data = BytesIO(r.content)
        df = pd.read_excel(data)
        return df
    else:
        st.error("Failed to load the file from GitHub.")
        return pd.DataFrame()

def search_a2z_list(input_text, df):
    prompt = f"Given the data in the table below, find the best match for the input query: {input_text}\n\n{df.head(10).to_string(index=False)}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
    )
    response_text = response.choices[0].text.strip()
    
    # Simple parsing (adjust according to actual format)
    try:
        parts = response_text.split("\n")
        name = parts[0].split(":")[-1].strip()
        phone = parts[1].split(":")[-1].strip()
    except IndexError:
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
