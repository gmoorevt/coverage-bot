from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import docuploader
import util, chatbotlogger as cblogger

       
def set_debug():
    st.session_state.debug = st.session_state.debug_check
    
def main():

    # Page title
    st.set_page_config(page_title='CareMetx PDF reader')
    st.header('CareMetx Coverage Bot 💬')
    
    if "benifit_file_slected" not in st.session_state:
        st.session_state.benifit_file_slected = False
    if "file_name" not in st.session_state:
        st.session_state.file_name = None
    if "debug" not in st.session_state:
        st.session_state.debug = False
    if "user" not in st.session_state:
        st.session_state.user = "anonymous"

    if st.session_state.debug:
        util.util.debug_info()

    
    debug_check = st.sidebar.checkbox("Debug Mode",value=st.session_state.debug,key="debug_check")

    if debug_check:
        st.session_state.debug = True
    else:
        st.session_state.debug = False
    
    intro = """
        Select a Drug coverage PDF and upload to break the document up and store in a vector model.  They use OpenAI to leverage LLM's to understand questions and look for similar answers in the PDF data. Then "ask" the bot a question about the coverage.

        - _What is the J code?_
        - _Is there a pre authorization needed?_
        - *What is the duration of coverage?*
        - _etc..._
        ### How to use the demo

        1. Go to the "Coverage Files" tab and either select a coverage file that has been uploaded previously or upload a new file.
        2. Click on the "Chat" tab and let the model load into memory and then start asking questions.

        The purpose of this demo is to prototype different types of document parsing and embedding strategies while collecting typical "questions" we have about the coverage information.  
    """
    st.markdown(intro)
    
        
if __name__ == '__main__':
    main()
