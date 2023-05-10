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

# functions

def register_fonts():
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'fonts/DejaVuSans-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', 'fonts/DejaVuSerif-Italic.ttf'))

def create_canvas(xValue,yValue,width,height,attributedText1, attributedText2,add_line,use_bold:False,use_italic:False):
    pdf_name = "example.pdf"
    c = canvas.Canvas(pdf_name, pagesize=A4)
    register_fonts()
    if use_bold and use_italic:
        regular_para1 = Paragraph(attributedText1, style=ParagraphStyle(name='BoldItalic', fontName='DejaVuSans-Bold', fontSize=14))
        regular_para2 = Paragraph(attributedText2, style=ParagraphStyle(name='BoldItalic', fontName='DejaVuSans-Bold', fontSize=14))
    elif use_bold:
        regular_para1 = Paragraph(attributedText1, style=ParagraphStyle(name='Bold', fontName='DejaVuSans-Bold', fontSize=14))
        regular_para2 = Paragraph(attributedText2, style=ParagraphStyle(name='Bold', fontName='DejaVuSans-Bold', fontSize=14))
    elif use_italic:
        regular_para1 = Paragraph(attributedText1, style=ParagraphStyle(name='Italic', fontName='DejaVuSerif-Italic', fontSize=14))
        regular_para2 = Paragraph(attributedText2, style=ParagraphStyle(name='Italic', fontName='DejaVuSerif-Italic', fontSize=14))
    else:
        regular_para1 = Paragraph(attributedText1, style=ParagraphStyle(name='Regular', fontName='DejaVuSans', fontSize=14))
        regular_para2 = Paragraph(attributedText2, style=ParagraphStyle(name='Regular', fontName='DejaVuSans', fontSize=14))
    
    regular_para1.wrapOn(c, width*inch, height*inch)
    regular_para1.drawOn(c, xValue, yValue)
    regular_para2.wrapOn(c, width*inch, height*inch)
    regular_para2.drawOn(c, xValue, yValue-200)
    if add_line:
            c.setStrokeColor(colors.black)
            c.setLineWidth(1)
            c.line(100, 100, 500, 100)
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
        

