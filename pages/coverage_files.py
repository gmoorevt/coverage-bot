import streamlit as st
import docuploader

# Page title
st.set_page_config(page_title='Coverage Files')
st.header('Coverage Files')

# Page header
#st.write('Select a Drug coverage PDF or Upload a new one.')

placeholder = st.empty()

placeholder.text('Select a Drug coverage PDF or Upload a new one.')


docs = docuploader.s3_manager.list_files()

placeholder.text("Select a Drug coverage PDF or Upload a new one.")

ls = docs
filenames = []
fileurl = []
links = []

for file in ls:
    filenames.append(file)
    # create lints
    url = docuploader.s3_manager.get_public_url('formulary-extra.pdf')
    link_text = file
    link_html = f'<a href="{url}" target="_blank">{link_text}</a>'
    links.append(link_html)


filegroup = st.radio('Select a file',filenames,index=None)
filegroup = None


st.subheader("Click to open a file and see it's contents")
link_container = st.container()

for l in links:
    link_container.markdown(l,unsafe_allow_html=True)

# if filegroup is not None:
#     st.text('You selected: ' + filegroup)
#     st.text('Upload a new file to train the bot on')

    