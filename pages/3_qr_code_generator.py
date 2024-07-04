import streamlit as st
import segno
import io

### STYLE
# Read the CSS file
with open("styles.css") as f:
    css = f.read()

# Add custom CSS for spacing
custom_css = """
<style>
    .column-spacer {
        width: 2rem;
    }
    .title-spacer {
        height: 2rem;
    }
</style>
"""

# Inject CSS with st.markdown
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
st.markdown(custom_css, unsafe_allow_html=True)

### CONTENT

def generate_qr_code(url, filename):
    qr_code = segno.make_qr(url)
    buffer = io.BytesIO()
    qr_code.save(
        buffer,
        kind="png",
        scale=8,
        border=2
    )
    buffer.seek(0)
    return buffer

st.title("QR Code Generator")

# Add space after the title
st.markdown('<div class="title-spacer"></div>', unsafe_allow_html=True)

# Create three columns: left column, spacer, right column
col1, spacer, col2 = st.columns([4, 1, 5])

# Left column for input fields
with col1:
    url = st.text_input("Enter the URL for the QR code:", key="url_input")
    filename = st.text_input("Enter the filename for the QR code (without .png):", key="filename_input")
    
    if st.button("Generate QR Code"):
        if url and filename:
            qr_buffer = generate_qr_code(url, filename)
            st.success(f"QR Code for {url} generated successfully!")
            st.download_button(
                label="Download QR Code",
                data=qr_buffer,
                file_name=f"{filename}.png",
                mime="image/png"
            )
        else:
            st.warning("Please enter both URL and filename.")

# Spacer column
with spacer:
    st.markdown('<div class="column-spacer"></div>', unsafe_allow_html=True)

# Right column for QR code preview
with col2:
    st.markdown("### Preview")
    if url:
        st.image(generate_qr_code(url, "preview"), caption="QR Code Preview", use_column_width=False)