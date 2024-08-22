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
def search_a2z_list_by_standard(dataframe, query):
    dataframe = dataframe.applymap(str)  # Ensure all data are in string format
    filtered_df = dataframe[dataframe['Standard'].str.contains(query, case=False, na=False)]
    return filtered_df

# Function to get contact details by state
def get_contact_details(row):
    states = {
        'NSW': 'NSW 02 9736 8222',
        'VIC': 'VIC 03 9274 8200',
        'QLD': 'QLD 07 3721 7300',
        'WA': 'WA 08 9486 2800',
        'SA': 'SA 08 8179 3400'
    }
    for state, phone_col in states.items():
        if phone_col in row and row[phone_col] != '':
            return state, row[phone_col]
    return "State not found", "Phone number not found"

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

# Streamlit app UI
st.title("Excel AI Web Application")
st.write("Search the A2Z list for the most appropriate contact person and their state phone number")

query = st.text_input("Enter your search text:")
if st.button("Search A2Z List"):
    if query:
        results = search_a2z_list_by_standard(data, query)
        if not results.empty:
            st.write(f"Found {len(results)} matches.")
            
            for _, row in results.iterrows():
                contact_name = row.get('Subject', 'Unknown')
                state, phone_number = get_contact_details(row)
                response = f"The best person to contact is {contact_name} in {state} on {phone_number}."
                st.write(response)
        else:
            st.write("No matches found")
    else:
        st.write("Please enter search text")
