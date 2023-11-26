import streamlit as st

class util:

    def debug_info():
        st.sidebar.divider()
        st.sidebar.subheader('Debug Info')  
        st.sidebar.write(st.session_state.file_name)
        st.sidebar.write(st.session_state.benifit_file_slected)
        st.sidebar.write(st.session_state)

    