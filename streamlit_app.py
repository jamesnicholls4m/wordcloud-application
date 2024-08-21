import streamlit as st
import pandas as pd
import openai
import requests
from io import BytesIO
from fuzzywuzzy import process

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
filepath = "NATA A2Z List - August 2024 - v1.xlsx" # Adjusted based on possible file structure

data = load_excel_from_github(username, repo, branch, filepath)

# Display input form
user_input = st.text_input("Enter the query text:")

# Define the columns expected in the data
expected_columns = ["Name", "Phone Number"]

if st.button("Search A2Z List"):
    if user_input:
        if all(col in data.columns for col in expected_columns):
            names = data['Name'].tolist()

            # Use OpenAI to interpret the input query
            prompt = f"Based on the provided names list, find the best match for the input text. Names: {names}. Input: {user_input}"
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50
            )

            best_name = response.choices[0].text.strip()
            st.write(f"Best Match Name: {best_name}")
            
            # Find the phone number corresponding to the best match name
            if best_name in data['Name'].values:
                phone_number = data.loc[data['Name'] == best_name, 'Phone Number'].values[0]
                st.write(f"Phone Number: {phone_number}")
            else:
                st.write("No matching name found in the data.")
        else:
            st.write(f"The expected columns ({expected_columns}) were not found in the Excel file.")
    else:
        st.write("Please enter some text to search.")

# Save this script as streamlit_app.py and run it using the command:
# streamlit run streamlit_app.py

# Ensure you have the necessary packages installed
# pip install streamlit pandas openai requests fuzzywuzzy
