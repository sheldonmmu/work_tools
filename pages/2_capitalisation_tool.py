### tut (inc free deployment) https://www.youtube.com/watch?v=D0D4Pa22iG0
# streamlit run main.py

import streamlit as st
import re

### STYLE
# Read the CSS file
with open("styles.css") as f:
    css = f.read()

# Inject CSS with st.markdown
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

### CONTENT
st.title("Capitalization App")

text = st.text_input("Change uppercase words in to capitalised sentences. Paste your text here:")

def custom_title_case(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)

# Create a button
if st.button("Enter"):
    if text:
        capitalized_text = custom_title_case(text)
        st.subheader("Capitalized Text:")
        st.write(capitalized_text)

        # Capitalize the first word of the sentence
        capitalized_sentence = text.capitalize()
        st.subheader("Capitalized Sentence:")
        st.write(capitalized_sentence)