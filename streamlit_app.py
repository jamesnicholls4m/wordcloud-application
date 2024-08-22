import streamlit as st
import pandas as pd
import requests
from io import BytesIO

@st.cache
def load_data_from_github(username, repo, branch, file_path):
    url = f"https://github.com/{username}/{repo}/raw/{branch}/{file_path}"
    response = requests.get(url)
    response.raise_for_status() # Check for request errors
    data = pd.read_excel(BytesIO(response.content))
    st.write("Data successfully loaded: ", data.head()) # Add a debug statement
    return data

def search_a2z_list(dataframe, query):
    # Filter rows based on query
    filtered_df = dataframe[dataframe.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    st.write(f"Query: {query}") # Debug: Show the input query
    st.write("Filtered DataFrame: ", filtered_df) # Debug: Show the filtered DataFrame
    return filtered_df

# Load the data from GitHub
username = "jamesnicholls4m"
repo = "wordcloud-application"
branch = "main"
file_path = "NATA A2Z List - August 2024 - v1.xlsx"

data = load_data_from_github(username, repo, branch, file_path)

# Streamlit app
st.title("Excel AI Web Application")
st.write("Search the A2Z list for an appropriate name and phone number")

query = st.text_input("Enter your search text:")
if st.button("Search A2Z List"):
    if query:
        results = search_a2z_list(data, query)
        if not results.empty:
            st.write(f"Found {len(results)} matches:")
            st.dataframe(results[['Name', 'Phone Number']]) # Displaying only Name and Phone Number columns
        else:
            st.write("No matches found")
    else:
        st.write("Please enter search text")

# Run the app
# To run this app, save it to a file (e.g., app.py) and run `streamlit run app.py` in your terminal.
