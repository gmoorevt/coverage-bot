import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Create an S3 client
s3 = boto3.client('s3')

# Specify the bucket name
bucket_name = 'cmtx-bot-storage'

# List all objects in the bucket
response = s3.list_objects_v2(Bucket=bucket_name)

# Iterate over the objects and print their names and links
for obj in response['Contents']:
    file_name = obj['Key']
    file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    print(file_name)
    print(file_url)
    

def readPDF(pdf_reader):

    print(pdf_reader)
    # pdf_reader = PdfReader(pdf)
    text = ""
    page_counter = 1
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
    # show user input
    st.divider()

    user_question = st.chat_input("Ask questions about the coverage...")
    
    if user_question:

        docs = knowledge_base.similarity_search(user_question)
        
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=user_question)
        
        st.chat_message(response)

