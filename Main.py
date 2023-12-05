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
        
This is a prototype designed to lean how LLM models and PDF chunking algorithms can be applied to extract specific  information from random health insurance public files.

A chat interface is used to create a mechanism to collect insights into the types of information that is of interest in a file.  

The model is not trained on any specific file format to ensure the approach is scalable across any file format created by a health insurance  provider.

The file selected will be parsed and loaded into a vector database.  A combination of similarity algorithms are run and then fed to OpenAI to format the response in a coherent result.  

To use the prototype, either select a file that has been uploaded previously or upload a new file.

Then "ask" the bot a question about the coverage.

- What is the J code?
	- What are the warnings?
        - Is there a pre authorization needed?
        - *What is the duration of coverage?*
        - etc...
### How to use the demo
1. Go to the "Coverage Files" tab and either select a coverage file that has been uploaded previously or upload a new file.
2. Click on the "Chat" tab and let the model load into memory and then start asking questions. 
    """
    st.markdown(intro)
    
        
if __name__ == '__main__':
    main()
