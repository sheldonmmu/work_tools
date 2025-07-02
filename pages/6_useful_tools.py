# streamlit run main.py
 
import streamlit as st

### STYLE
# Read the CSS file
with open("styles.css") as f:
    css = f.read()

# Inject CSS with st.markdown
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

### CONTENT
st.title("Useful tools")

# Input area for user to paste a paragraph
text = st.text("A list of tools that maybe useful:")

# List of tools as (name, url) tuples
tools = [
    ("12ft ladder - remove paywalls", "https://12ft.io/"),
    ("APIs for Librarians - list", "https://github.com/sheldonmmu/library_apis"),
    ("Wayback Machine - archive web content", "https://web.archive.org/"),
    ("Archive.today  - archive web content", "https://archive.is/"),
]

for name, url in tools:
    st.markdown(
        f"- **{name}** [<span style='color:blackblue'>{url}</span>]({url})",
        unsafe_allow_html=True
    )