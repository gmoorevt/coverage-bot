import streamlit as st
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import docuploader,util, chatbotlogger as cblogger

# Page title
st.set_page_config(page_title='Chatbot')
st.header('Chatbot')

def readPDF2(pdf_reader):

    # Create session logger

    clogger = cblogger.ChatBotLogger()
    
    if "db_session_id" not in st.session_state: 
        st.session_state.db_session_id = clogger.log_session(st.session_state.user)

    clogger.update_session(st.session_state.db_session_id, {"file_name": st.session_state.file_name})

    # load model
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text()
        
    # split into chunkcs
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # create embeddings
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks,embeddings)
    # end model

    # Create session logger
    if "db_session_id" not in st.session_state:
        st.session_state.db_session_id = clogger.log_session(st.session_state.user)
    
    if "messages" not in st.session_state:
         st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]): 
            st.markdown(message["content"]) 
        
    if prompt := st.chat_input("Ask questions about the coverage..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt) 

        with st.chat_message("assistant"):
             
            message_placeholder = st.empty()
            full_response = ""
             
            docs = knowledge_base.similarity_search(prompt)
            
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=prompt)
                full_response += response
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response}) 
        clogger.log_message(st.session_state.user, st.session_state.db_session_id,prompt,full_response)  

st.sidebar.divider()
if st.session_state.file_name is not None:
    st.sidebar.subheader('Coverage File Loaded')
    st.sidebar.write(st.session_state.file_name)
    st.sidebar.markdown(docuploader.get_public_url(st.session_state.file_name),unsafe_allow_html=True)
else:
    st.sidebar.subheader('No Coverage File Loaded')
    st.sidebar.write('Please select or upload a file to get started.')

# Debug info
if st.session_state.debug:
        util.util.debug_info()


placeholder = st.empty()

if st.session_state.file_name is None:
    placeholder.write('Select a Drug coverage PDF.')
else:
    placeholder.write(f"Selected file: {st.session_state.file_name}")
    pdf = docuploader.load_pdf_from_s3(st.session_state.file_name)
    readPDF2(pdf)

botcontainer = st.container()


