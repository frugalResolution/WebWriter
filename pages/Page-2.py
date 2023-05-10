import streamlit as st
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import unicodedata
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph
from PIL import Image


# functions
from reportlab.pdfgen import canvas


# Set allowed file extensions
ALLOWED_EXTENSIONS = set(['pdf', 'png'])

def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a list to hold the uploaded images
images = []

# Define a function to display the images in a list view
def display_images():
    for img in images:
        st.image(img, use_column_width=True)


st.set_page_config(
    page_title="Text Editor to PDF",
    page_icon="📝",
    layout="wide",
)


st.write("# Text On PDF 📝")



switch_state = st.checkbox("Display Pdf",key=1)
if switch_state:
    input_file = 'example.pdf'
    pdf_file = open(input_file, "rb").read()
    b64_pdf = base64.b64encode(pdf_file).decode('utf-8')
    st.markdown(f'<embed src="data:application/pdf;base64,{b64_pdf}" width="700" height="1000" type="application/pdf">', unsafe_allow_html=True)
    st.download_button(
        label="Download PDF",
        data=pdf_file,
        file_name="example.pdf",
        mime="application/pdf"
        )


uploaded_files = st.file_uploader(
    label="Choose a file",
    accept_multiple_files=True,
    type=ALLOWED_EXTENSIONS
)

# Display uploaded files as a list
if uploaded_files:
    st.write("Uploaded files:")
    for file in uploaded_files:
        # Check if file is an allowed type
        if allowed_file(file.name):
            # Display file name and type
            if file.type == "image/png":
                image = Image.open(file)
                st.image(image, use_column_width=True)
            else:
                pdf_contents = file.read()
                b64_pdf = base64.b64encode(pdf_contents).decode('utf-8')
                st.markdown(f'<embed src="data:application/pdf;base64,{b64_pdf}" width="700" height="1000" type="application/pdf">', unsafe_allow_html=True)
                # st.write(pdf_contents, format='pdf')
        else:
            st.warning(f"{file.name} has an invalid file type.")