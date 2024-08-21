import streamlit as st
import pandas as pd
import openai
import requests
from io import BytesIO

# Function to load the Excel file from GitHub
@st.cache_data
def load_excel_from_github(username, repo, branch, filepath):
    url = f"https://raw.githubusercontent.com/{username}/{repo}/{branch}/{filepath}"
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return pd.read_excel(BytesIO(response.content))

# Streamlit application begins here
st.title('Excel AI Search Application')

# Retrieve the OpenAI API Key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load the A2Z list file
username = "jamesnicholls4m"
repo = "wordcloud-application"
branch = "main"
filepath = "NATA A2Z List - August 2024 - v1.xlsx"  # Assumed correct path

data = load_excel_from_github(username, repo, branch, filepath)

# Display input form
user_input = st.text_input("Enter the query text:")

if st.button("Search A2Z List"):
    if user_input:
        # Generate the prompt with available data
        data_str = data.head(20).to_string(index=False)  # Limit to first 20 rows for prompt size
        prompt = f"Based on the following data, provide the best match or information related to the input query.\n\nData:\n{data_str}\n\nQuery:\n{user_input}\n\nResponse:"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,  # Adjust as necessary
            temperature=0.7  # Adjust based on desired creativity
        )

        result = response.choices[0].text.strip()
        st.write(result)
    else:
        st.write("Please enter some text to search.")

# Save this script as streamlit_app.py and run it using the command:
# streamlit run streamlit_app.py

# Ensure you have the necessary packages installed
# pip install streamlit pandas openai requests
