import streamlit as st
from bookops_worldcat import WorldcatAccessToken, MetadataSession
import random
import xml.etree.ElementTree as ET
import requests
import os
from requests.exceptions import ConnectTimeout, RequestException, HTTPError
import json

### STYLE
# Read the CSS file
with open("styles.css") as f:
    css = f.read()

# Inject CSS with st.markdown
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# API creds
CLIENT_ID = st.secrets["client_id"]
CLIENT_SECRET = st.secrets["client_secret"]

### CONTENT

st.title("WorldCat Library Item Explorer")

# Function to extract specific fields from XML
def extract_fields(xml_string):
    root = ET.fromstring(xml_string)
    
    # Define namespace
    ns = {'marc': 'http://www.loc.gov/MARC21/slim'}
    
    # Extract author (100)
    author = root.find('.//marc:datafield[@tag="100"]', ns)
    author = ' '.join([subfield.text for subfield in author.findall('marc:subfield', ns) if subfield.text]) if author is not None else "No author found"

    # Extract title (245)
    title = root.find('.//marc:datafield[@tag="245"]', ns)
    title = ' '.join([subfield.text for subfield in title.findall('marc:subfield', ns) if subfield.text]) if title is not None else "No title found"

    # Extract ISBNs (020)
    isbns = root.findall('.//marc:datafield[@tag="020"]/marc:subfield[@code="a"]', ns)
    isbns = [isbn.text for isbn in isbns] if isbns else ["No ISBN found"]

    # Extract subject headings (600-699)
    subject_headings = []
    for tag in range(600, 700):
        fields = root.findall(f'.//marc:datafield[@tag="{tag}"]', ns)
        for field in fields:
            heading = ' -- '.join([subfield.text for subfield in field.findall('marc:subfield', ns) if subfield.text])
            subject_headings.append(heading)

    return author, title, isbns, subject_headings

# Generate random OCLC number
def generate_random_number():
    num_digits = random.choice([7, 8, 9])
    first_digit = random.randint(1, 9)
    remaining_digits = [random.randint(0, 9) for _ in range(num_digits - 1)]
    all_digits = [first_digit] + remaining_digits
    return int(''.join(map(str, all_digits)))

# Function to get book cover
def get_book_cover(isbns):
    cover_image = None
    is_default_image = True
    for isbn in isbns:
        try:
            api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if 'items' in data and 'volumeInfo' in data['items'][0] and 'imageLinks' in data['items'][0]['volumeInfo']:
                cover_url = data['items'][0]['volumeInfo']['imageLinks'].get('thumbnail')
                if cover_url:
                    cover_image = requests.get(cover_url).content
                    is_default_image = False
                    break
        except (ConnectTimeout, RequestException):
            print(f"Error occurred while fetching cover image from Google Books API for ISBN: {isbn}")

    if cover_image is None:
        images_folder = 'images'
        if os.path.exists(images_folder):
            image_files = [f for f in os.listdir(images_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if image_files:
                random_image = random.choice(image_files)
                default_image_path = os.path.join(images_folder, random_image)
                try:
                    with open(default_image_path, 'rb') as f:
                        cover_image = f.read()
                except Exception as e:
                    print(f"Error reading default image {default_image_path}: {e}")
            else:
                print(f"No image files found in the {images_folder} folder.")
        else:
            print(f"The {images_folder} folder does not exist.")

    return cover_image, is_default_image

# Main app logic
token = WorldcatAccessToken(
    key=CLIENT_ID,
    secret=CLIENT_SECRET,
    scopes="WorldCatMetadataAPI",
    agent="my_app/version 1.0"
)

st.write("Click the button to fetch a random WorldCat item!")

if st.button("Get Random WorldCat Item"):
    with MetadataSession(authorization=token) as session:
        max_attempts = 100
        valid_item_found = False
        for attempt in range(max_attempts):
            try:
                oclc_number = generate_random_number()
                response = session.bib_get(oclc_number)
                
                if response.status_code == 200:
                    valid_item_found = True
                    author, title, isbns, subject_headings = extract_fields(response.text)

                    st.subheader("Item Details")

                    # Create two columns
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        # Get and display book cover
                        cover_image, is_default_image = get_book_cover(isbns)
                        if cover_image:
                            caption = "No book cover available" if is_default_image else "Book Cover"
                            st.image(cover_image, caption=caption, width=200)

                    with col2:
                        st.write(f"**OCLC Number:** {oclc_number}")
                        st.write(f"**Author:** {author}")
                        st.write(f"**Title:** {title}")
                        st.write(f"**ISBNs:** {', '.join(isbns)}")
                        st.write(f"**Subject Headings:** {', '.join(subject_headings)}")

                    break  # If successful, exit the loop

            except HTTPError as e:
                if e.response.status_code == 404:
                    continue  # Try another random number
                else:
                    try:
                        error_data = e.response.json()
                        st.write(f"Last error: {e}. Server response: {error_data}")
                    except json.JSONDecodeError:
                        st.write(f"Last error: {e}. Server response: {e.response.text}")
                    break
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
                break

        if not valid_item_found:
            st.write("Error occurred while fetching a record. Please try again.")
            try:
                error_data = json.loads(f"{{\"type\":\"NOT_FOUND\",\"title\":\"Unable to perform the bib read operation.\",\"detail\":{{\"summary\":\"NOT_FOUND\",\"description\":\"Not able to find the requested Bib\"}}}}")
                st.write(f"Last error: 404 Client Error: Not Found for url: https://metadata.api.oclc.org/worldcat/manage/bibs/{oclc_number}. Server response: {error_data}")
            except json.JSONDecodeError:
                st.write(f"Last error: 404 Client Error: Not Found for url: https://metadata.api.oclc.org/worldcat/manage/bibs/{oclc_number}. Server response: {{'type':'NOT_FOUND','title':'Unable to perform the bib read operation.','detail':{'summary':'NOT_FOUND','description':'Not able to find the requested Bib'}}}")