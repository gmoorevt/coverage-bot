import streamlit as st

import docuploader
import util, chatbotlogger as cblogger

logger = cblogger.ChatBotLogger()

# Page title
st.set_page_config(page_title='Coverage Files')
st.header('Coverage Files')
if "debug" in st.session_state:
    if st.session_state.debug:
        util.util.debug_info()  
    
page_stale = False

# Page header
#st.write('Select a Drug coverage PDF or Upload a new one.')

def file_selection_on_change():
    st.session_state.file_name = st.session_state.file_selection
    st.session_state.benifit_file_slected = True
    
    st.session_state.db_session_id = logger.log_session(st.session_state.user)
    logger.update_session(st.session_state.db_session_id, {"file_name": st.session_state.file_name})
    
    st.toast(f"Selected file: {st.session_state.file_name}")
    if "messages" in st.session_state:
        st.session_state.messages = []

def get_index_of_file(file_name,filelist):
    try:
        index = filelist.index(file_name)
        return index
    except ValueError:
        return None

placeholder = st.empty()

with placeholder.container():
    st.write('Loading files...')

docs = docuploader.s3_manager.list_files()
with placeholder.container():
    st.write("Select a Drug coverage PDF or Upload a new one.")

ls = docs
filenames = []
fileurl = []
links = []

for file in ls:
    filenames.append(file)
    # create lints
    url = docuploader.s3_manager.get_public_url(file)
    link_text = file
    link_html = f'<a href="{url}" target="_blank">{link_text}</a>'
    links.append(link_html)


filegroup = st.radio('Select a file',filenames,
                     index=get_index_of_file(st.session_state.file_name,filenames),
                     key="file_selection",
                     on_change=file_selection_on_change
                     )


#load_file_btn = st.button('Load File',disabled=True,key="load_file_btn")

# if filegroup is not None:
#     st.toast(f"Selected file: {filegroup}",key="file_selected_toast")
#     st.session_state.file_name = filegroup
#     st.session_state.benifit_file_slected = True
#     placeholder.write(f"Selected file: {st.session_state.file_name}")
    
    

if st.session_state.file_selection is not None:
    load_file_btn = False
    st.write(f'Ready to load {st.session_state.file_selection} into the model.')
    st.write('Click the "Chat" tab to start asking questions.')
    

st.divider()

# PDF upload
st.write("Upload a benifit coverage PDF and then 'ask' the bot questions about it`s contents.") 
pdf = st.file_uploader("Coverage file", type=['pdf'])
if pdf is not None:
    # Upload file to s3
    docuploader.save_file(pdf)
    docuploader.get_files()
    page_stale = True
    
# Open PDF file in new window
st.subheader("Click to open a file and see it's contents",divider=True)
link_container = st.container()

for l in links:
    link_container.markdown(l,unsafe_allow_html=True)


    
