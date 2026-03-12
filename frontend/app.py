import streamlit as st
from components.sidebar import render_sidebar
from pages.home import render_home
from pages.analysis import render_analysis
from pages.chat import render_chat
from pages.history import render_history

st.set_page_config(
    page_title="MedAnalyze AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "uploaded_report" not in st.session_state:
    st.session_state.uploaded_report = None

render_sidebar()

page = st.session_state.page

if page == "Home":
    render_home()
elif page == "Analyze Report":
    render_analysis()
elif page == "Chat with AI":
    render_chat()
elif page == "History":
    render_history()
