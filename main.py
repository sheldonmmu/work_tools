import streamlit as st

# Read the CSS file
with open("styles.css") as f:
    css = f.read()

# Inject CSS with st.markdown
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title("Sheldon's Tools and Experiments")
st.image('https://miro.medium.com/v2/resize:fit:1100/format:webp/1*yvRmV4yeH8YwSpJpgqIxpA.png', caption='Image Caption')

st.subheader("Useful links:")
st.link_button("Streamlit emoji codes", "https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/")