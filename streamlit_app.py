import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Function to load data from the GitHub URL
@st.cache
def load_data_from_github():
    url = "https://raw.githubusercontent.com/jamesnicholls4m/wordcloud-application/main/NATA%20A2Z%20List%20-%20August%202024%20-%20v1.xlsx"
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_excel(BytesIO(response.content))
        return data
    else:
        st.error("Failed to fetch file. Check the URL.")
        return None

# Main function to run the Streamlit app
def main():
    st.title('Excel AI Web Application')

    # Load data from GitHub
    data = load_data_from_github()

    if data is not None:
        # Display initial data for verification (optional)
        st.write("Data loaded successfully. Here's a preview:")
        st.write(data.head())

        # Text input form field
        user_input = st.text_input("Enter text data")

        # Button to trigger search
        if st.button('Search A2Z List'):
            if user_input:
                result = search_data(user_input, data)
                st.write("Search Results:")
                st.write(result)
            else:
                st.write("Please enter some text to search.")
    else:
        st.write("Failed to load data from GitHub. Ensure the URL is correct and file is accessible.")

# Function to search data based on input text
def search_data(input_text, data):
    # Replace 'text_column' with the actual column name you intend to search
    search_results = data[data['text_column'].str.contains(input_text, case=False, na=False)]
    return search_results

if __name__ == "__main__":
    main()
