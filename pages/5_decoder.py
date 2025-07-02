# streamlit run main.py
 
import streamlit as st
import html

### STYLE
# Read the CSS file
with open("styles.css") as f:
    css = f.read()

# Inject CSS with st.markdown
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

### CONTENT
st.title("Decode Drupal Edit Text")

# Input area for user to paste a paragraph
text = st.text_area("Change ugly Drupal text into human readable. Paste your text here:")

def human_readable_text(s):
    # Decode double-encoded HTML entities
    for _ in range(2):
        s = html.unescape(s)
    return s

if st.button("Decode"):
    if text:
        decoded = human_readable_text(text)
        st.text_area("Decoded text:", value=decoded, height=150)
    else:
        st.info("Please enter some text to decode.")