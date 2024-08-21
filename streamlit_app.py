import streamlit as st
import pandas as pd
import openai

# Fetch OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load data from GitHub
@st.cache_data
def load_data_from_github():
    url = ('https://raw.githubusercontent.com/jamesnicholls4m/wordcloud-application/main/'
           'NATA%20A2Z%20List%20-%20August%202024%20-%20v1.xlsx')
    df = pd.read_excel(url)
    return df

# Function to search the A2Z list
def search_a2z_list(df, input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that provides contact details."},
            {"role": "user", "content": f"Find the best matching contact for: {input_text}"}
        ]
    )

    message = response['choices'][0]['message']['content'].strip()
    st.write(f"ChatGPT Interpretation: {message}")

    # Process the response to search in relevant columns
    match = df[df.apply(lambda row: row.astype(str).str.contains(message, case=False).any(), axis=1)]
    if not match.empty:
        return match.iloc[0][['Subject', 'Standard', 'Activity', 'Service', 'NSW 02 9736 8222', 
                              'VIC 03 9274 8200', 'QLD 07 3721 7300', 'WA 08 9486 2800', 
                              'SA 08 8179 3400']]
    else:
        return None

# Streamlit Application UI
def main():
    st.title("A2Z List Search Application using OpenAI")
    
    # Text input from user
    user_input = st.text_input("Enter details to search for the contact:")
    
    if st.button("Search A2Z List"):
        df = load_data_from_github()
        result = search_a2z_list(df, user_input)

        if result is not None:
            st.write("Match Found:")
            st.write(result.to_frame().T)
        else:
            st.write("No matching contact found.")

if __name__ == "__main__":
    main()
