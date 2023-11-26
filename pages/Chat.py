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
import docuploader

# Page title
st.set_page_config(page_title='Chatbot')
st.header('Chatbot')

st.sidebar.write(st.session_state.file_name)
st.sidebar.write(st.session_state.benifit_file_slected)
st.sidebar.write(st.session_state)

def readPDF2(pdf_reader):

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




placeholder = st.empty()

if st.session_state.file_name is None:
    placeholder.write('Select a Drug coverage PDF.')
else:
    placeholder.write(f"Selected file: {st.session_state.file_name}")

    pdf = docuploader.load_pdf_from_s3(st.session_state.file_name)

    readPDF2(pdf)



botcontainer = st.container()


