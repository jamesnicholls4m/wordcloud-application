import streamlit as st
import pandas as pd
import openai
import requests
from io import BytesIO

@st.cache
def load_excel_from_github(username, repo, branch, filepath):
    url = f"https://raw.githubusercontent.com/{username}/{repo}/{branch}/{filepath}"
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return pd.read_excel(BytesIO(response.content))

st.title('Excel AI Search Application')

# Retrieve the OpenAI API Key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load the A2Z list file
username = "jamesnicholls4m"
repo = "wordcloud-application"
branch = "main"
filepath = "wordcloud-application/NATA A2Z List - August 2024 - v1.xlsx"

data = load_excel_from_github(username, repo, branch, filepath)

# Input text data from the user
user_input = st.text_input("Enter the query text:")

if st.button("Search A2Z List"):
    if user_input:
        # Using fuzzy matching to find the best match for simplicity
        from fuzzywuzzy import process
        
        choices = data['Name'].tolist()  # Assuming 'Name' is the column
        best_match = process.extractOne(user_input, choices)
        
        if best_match and best_match[1] > 75:  # 75 is a threshold for match confidence
            matched_row = data[data['Name'] == best_match[0]]
            result_name = matched_row['Name'].values[0]
            result_phone = matched_row['Phone Number'].values[0]  # Assuming 'Phone Number' is the column
            st.write(f"Best Match: {result_name}, Phone Number: {result_phone}")
        else:
            st.write("No good match found.")
    else:
        st.write("Please enter some text to search.")
