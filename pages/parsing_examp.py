import streamlit as st
from PyPDF2 import PdfReader



st.set_page_config(page_title="Natural Lang Parsing")
st.header("Parsing types")



pdf = st.file_uploader("Upload a PDF",type=['pdf'])

if pdf is not None:
    text = ""
    doc = PdfReader(pdf)
    for page in doc.pages:
        text += page.extractText()



    question = st.text_input("Type your question")

    st.text(question)
    
    
    