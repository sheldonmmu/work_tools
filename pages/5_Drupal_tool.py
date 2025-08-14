# streamlit run main.py
import streamlit as st
import html
import re

### STYLE
# set in config.toml

# 🔹 UI
st.title("Drupal Text Cleaning Tool")

text = st.text_area("Paste your text here:")

option = st.radio(
    "Choose what you want to remove:",
    ("Remove UTF encoding only", "Remove HTML tags only", "Remove both")
)

# 🔹 Helper functions
def decode_html_entities(s):
    for _ in range(2):  # Handle double encoding
        s = html.unescape(s)
    return s

def remove_html_tags(s):
    return re.sub(r'<.*?>', '', s)

# 🔹 Processing
if st.button("Process"):
    if not text:
        st.info("Please paste some text above.")
    else:
        if option == "Remove UTF encoding only":
            result = decode_html_entities(text)
        elif option == "Remove HTML tags only":
            result = remove_html_tags(text)
        elif option == "Remove both":
            result = remove_html_tags(decode_html_entities(text))
        st.text_area("Output:", value=result, height=150)
