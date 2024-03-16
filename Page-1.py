import streamlit as st
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.lib import colors

# Improved functions

def register_fonts():
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'fonts/DejaVuSans-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', 'fonts/DejaVuSerif-Italic.ttf'))

def add_paragraph(canvas, text, x, y, width, height, style):
    frame = Frame(x, y, width, height, showBoundary=1)
    story = [Paragraph(text, style)]
    frame.addFromList([KeepInFrame(width, height, story)], canvas)

def create_pdf(text_area1, text_area2, use_bold, use_italic, add_line, dark_mode):
    pdf_name = "example.pdf"
    c = canvas.Canvas(pdf_name, pagesize=A4)
    register_fonts()

    style = ParagraphStyle(name='Regular', fontName='DejaVuSans', fontSize=14)
    if use_bold:
        style.fontName = 'DejaVuSans-Bold'
    if use_italic:
        style.fontName = 'DejaVuSerif-Italic'

    if dark_mode:
        c.setFillColor(colors.grey)
        c.rect(0, 0, A4[0], A4[1], fill=1)
        style.textColor = colors.whitesmoke

    add_paragraph(c, text_area1, 100, 750, 400, 100, style)
    add_paragraph(c, text_area2, 100, 600, 400, 100, style)

    if add_line:
        c.setStrokeColor(colors.black)
        c.line(100, 550, 500, 550)

    c.save()
    return pdf_name


def register_fonts():
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'fonts/DejaVuSans-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', 'fonts/DejaVuSerif-Italic.ttf'))

def create_canvas(xValue, yValue, width, height, attributedText1, attributedText2, add_line, use_bold=False, use_italic=False, dark_mode=False):
    pdf_name = "example.pdf"
    c = canvas.Canvas(pdf_name, pagesize=A4)
    register_fonts()

    # Set background for dark mode
    if dark_mode:
        c.setFillColor(colors.black)
        c.rect(0, 0, A4[0], A4[1], fill=1)

    # Set text color based on dark mode
    text_color = colors.whitesmoke if dark_mode else colors.black

    # Adjust the rest of your function to use `text_color` for the text

    # Your existing logic for creating the content...

    c.save()
    return pdf_name


st.set_page_config(
    page_title="Text Editor to PDF",
    page_icon="📝",
    layout="wide",
)


st.write("# Text On PDF 📝")

container = st.container()
with container:
    text_area1 = st.text_area("Enter Text 1",key=1,label_visibility="hidden")
    text_area2 = st.text_area("Enter Text 2",key=2,label_visibility="hidden")
    use_bold = st.checkbox("Use Bold", key="use_bold")
    use_italic = st.checkbox("Use Italic", key="use_italic")
    add_line = st.checkbox("add_line", key="add_line")
btn = st.button("Generate PDF")

Pdf_container = st.container()
if btn:
    with Pdf_container:
        pdf_name = create_canvas(100,750,6,5,text_area1, text_area2,add_line,use_bold,use_italic)
        pdf_file = open(pdf_name, "rb").read()
        b64_pdf = base64.b64encode(pdf_file).decode('utf-8')
        Pdf_container.markdown(f'<embed src="data:application/pdf;base64,{b64_pdf}" width="700" height="1000" type="application/pdf">', unsafe_allow_html=True)
        st.download_button(
        label="Download PDF",
        data=pdf_file,
        file_name="example.pdf",
        mime="application/pdf"
        )
        


# Dark Mode Toggle
dark_mode = st.checkbox("Dark Mode", key="dark_mode")

# Generate PDF button action
if btn:
    pdf_name = create_canvas(100, 750, 6, 5, text_area1, text_area2, add_line, use_bold, use_italic, dark_mode)  # Pass `dark_mode` here
    # The rest of your logic for displaying and downloading the PDF
