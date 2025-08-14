import streamlit as st
import pandas as pd

### STYLE
# set in config.toml

st.title("Useful tools")

# Organize tools as a list of dictionaries (or as a DataFrame)
tools = [
    {
        "Category": "Archiving & Research",
        "Title": "12ft ladder",
        "Description": "Remove paywalls",
        "URL": "https://12ft.io/"
    },
    {
        "Category": "Archiving & Research",
        "Title": "Wayback Machine",
        "Description": "Archive web content",
        "URL": "https://web.archive.org/"
    },
    {
        "Category": "Archiving & Research",
        "Title": "Archive.today",
        "Description": "Archive web content",
        "URL": "https://archive.is/"
    },
    {
        "Category": "Archiving & Research",
        "Title": "APIs for Librarians",
        "Description": "List of library APIs",
        "URL": "https://github.com/sheldonmmu/library_apis"
    },
    {
        "Category": "Archiving & Research",
        "Title": "Haveibeenpwned",
        "Description": "Find out when/where your information was leaked",
        "URL": "https://haveibeenpwned.com/"
    },
    {
        "Category": "Productivity & Utilities",
        "Title": "Maildrop",
        "Description": "Get a temporary email address",
        "URL": "https://maildrop.cc/"
    },
    {
        "Category": "Productivity & Utilities",
        "Title": "Formula bot",
        "Description": "Create an Excel formula with Gen AI",
        "URL": "https://app.formulabot.com/excel-ai"
    },
    {
        "Category": "Design & Media",
        "Title": "Photopea",
        "Description": "Edit photos in your browser",
        "URL": "https://www.photopea.com/"
    },
    {
        "Category": "Design & Media",
        "Title": "Color designer",
        "Description": "Colour swatch hexcodes from an image",
        "URL": "https://colordesigner.io/color-palette-from-image"
    },
]

# Convert to DataFrame for easy display
df = pd.DataFrame(tools)

# If you want to group by category, you can do so:
for category in df['Category'].unique():
    st.markdown(f"### {category}")
    cat_df = df[df['Category'] == category][['Title', 'Description', 'URL']].copy()
    # Make the URLs clickable
    cat_df['URL'] = cat_df['URL'].apply(lambda x: f"[{x}]({x})")
    # Use Streamlit's markdown table rendering
    st.markdown(cat_df.to_markdown(index=False), unsafe_allow_html=True)
    st.markdown("---")
