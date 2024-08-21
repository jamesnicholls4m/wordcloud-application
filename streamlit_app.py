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
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    return df

# Load the data
df = load_data()

# Display DataFrame columns for debugging
st.write("Columns in the DataFrame:", df.columns.tolist())

# Streamlit application
st.title("A2Z List Search Application")

# Text input field
user_input = st.text_input("Enter text to search for a name and phone number")

if st.button("Search A2Z List"):
    if user_input:
        # Perform case-insensitive search across all columns
        mask = df.apply(lambda row: row.astype(str).str.contains(user_input, case=False, na=False).any(), axis=1)
        result = df[mask]
        
        # Display results for debugging
        st.write("Search mask:", mask)
        st.write("Search results DataFrame:", result)
        
        if not result.empty:
            st.write("Results found:")
            for _, row in result.iterrows():
                # Update these keys to match your actual column names
                name = row.get('Name', 'N/A')  
                phone = row.get('Phone', 'N/A')
                st.write(f"Name: {name}")
                st.write(f"Phone: {phone}")
        else:
            st.write("No results found.")
    else:
        st.write("Please enter a text to search.")
