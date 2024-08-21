import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Function to load the Excel file from GitHub
@st.cache
def load_data():
    url = "https://github.com/jamesnicholls4m/wordcloud-application/blob/main/NATA%20A2Z%20List%20-%20August%202024%20-%20v1.xlsx?raw=true"
    response = requests.get(url)
    file = BytesIO(response.content)
    xls = pd.ExcelFile(file)
    # Assuming the relevant data is in the first sheet, adjust if necessary
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    return df

# Load the data
df = load_data()

# Streamlit application
st.title("A2Z List Search Application")

# Text input field
user_input = st.text_input("Enter text to search for a name and phone number")

if st.button("Search A2Z List"):
    if user_input:
        # Assume a simple search by checking if the input text appears in any cell
        mask = df.apply(lambda row: row.astype(str).str.contains(user_input, case=False).any(), axis=1)
        result = df[mask]
        
        if not result.empty:
            st.write("Results found:")
            for _, row in result.iterrows():
                st.write(f"Name: {row['Name']}")   # Adjust according to actual column names
                st.write(f"Phone: {row['Phone']}") # Adjust according to actual column names
        else:
            st.write("No results found.")
    else:
        st.write("Please enter a text to search.")
