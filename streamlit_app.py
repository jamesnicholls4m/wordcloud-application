import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import string
import io

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Define function to preprocess text
def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text)
    # Convert to lower case
    tokens = [word.lower() for word in tokens]
    # Remove punctuation
    tokens = [word for word in tokens if word.isalpha()]
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Generate word cloud
def generate_wordcloud(text, max_words, max_font_size, additional_stopwords, color, case):
    # Add additional stopwords
    stop_words = set(STOPWORDS)
    stop_words.update(additional_stopwords)
    
    if case == 'Upper case':
        text = text.upper()
    elif case == 'Lower case':
        text = text.lower()

    wordcloud = WordCloud(stopwords=stop_words,
                          max_words=max_words,
                          max_font_size=max_font_size,
                          colormap=color,
                          background_color='white').generate(text)
    
    return wordcloud

# Streamlit app
st.title('Word Cloud Generator')

# Input text
uploaded_file = st.file_uploader("Upload a .txt or .csv file", type=["txt", "csv"])
input_text = st.text_area("Or input your text here:")

if uploaded_file is not None:
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        text = " ".join(df.iloc[:,0].dropna().astype(str))
    elif uploaded_file.type == "text/plain":
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        text = stringio.read()
else:
    text = input_text

preprocessed_text = preprocess_text(text)

# Word cloud settings
st.sidebar.header("Word Cloud Settings")
num_words = st.sidebar.slider("Maximum number of words", min_value=10, max_value=500, value=100)
min_frequency = st.sidebar.slider("Minimum word frequency", min_value=1, max_value=10, value=1)
max_font_size = st.sidebar.slider("Maximum font size", min_value=10, max_value=100, value=60)
text_color = st.sidebar.selectbox("Text color", options=['black', 'Colorful'])
text_case = st.sidebar.selectbox("Text case", options=['Original', 'Upper case', 'Lower case'])
additional_stopwords = st.sidebar.text_area("Additional stopwords (separated by commas)").split(',')

if st.button('Generate Word Cloud'):
    wordcloud = generate_wordcloud(preprocessed_text, num_words, max_font_size - min_frequency, additional_stopwords, text_color, text_case)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
    st.download_button('Download PNG', data=wordcloud.to_image(), file_name='wordcloud.png', mime='image/png')
