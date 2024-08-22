import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Function to load data from GitHub
@st.cache
def load_data_from_github(username, repo, branch, file_path):
    url = f"https://github.com/{username}/{repo}/raw/{branch}/{file_path}"
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    data = pd.read_excel(BytesIO(response.content))
    return data

# Search function
def search_a2z_list(dataframe, query):
    dataframe = dataframe.applymap(str)  # Ensure all data are in string format
    # Filter rows based on query
    filtered_df = dataframe[dataframe.apply(lambda row: row.str.contains(query, case=False).any(), axis=1)]
    st.write(f"Query: '{query}'")  # Debug: Show the input query
    st.write("Filtered DataFrame:", filtered_df.head())  # Debug: Show the filtered DataFrame
    return filtered_df

# Load the data from GitHub
username = "jamesnicholls4m"
repo = "wordcloud-application"
branch = "main"
file_path = "NATA A2Z List - August 2024 - v1.xlsx"

data = load_data_from_github(username, repo, branch, file_path)

# Display the dataframe to inspect the data
st.write("Loaded DataFrame:")
st.write(data.head())

# Show column names
st.write("Column names:", data.columns)

# Streamlit app
st.title("Excel AI Web Application")
st.write("Search the A2Z list for an appropriate name and phone number")

query = st.text_input("Enter your search text:")
if st.button("Search A2Z List"):
    if query:
        results = search_a2z_list(data, query)
        if not results.empty:
            st.write(f"Found {len(results)} matches:")
            display_columns = [
                "Subject", "Standard", "Activity", "Service", 
                "NSW 02 9736 8222", "VIC 03 9274 8200", "QLD 07 3721 7300", 
                "WA 08 9486 2800", "SA 08 8179 3400"
            ]
            # Show all columns if expected column names are present
            missing_columns = [col for col in display_columns if col not in results.columns]
            if not missing_columns:
                st.dataframe(results[display_columns])  # Displaying specific columns
            else:
                st.write(f"The following expected columns are missing from the data: {missing_columns}")
        else:
            st.write("No matches found")
    else:
        st.write("Please enter search text")
