import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding:10px 0 20px'>
            <h1 style='color:#2196F3; font-size:2rem;'>🏥 MedAnalyze</h1>
            <p style='color:#888; font-size:0.85rem;'>AI-Powered Medical Report Analysis</p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        nav_items = {
            "🏠 Home":           "Home",
            "📋 Analyze Report": "Analyze Report",
            "💬 Chat with AI":   "Chat with AI",
            "📂 History":        "History",
        }
        for label, page_key in nav_items.items():
            active = st.session_state.page == page_key
            if st.button(label, use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.page = page_key
                st.rerun()

        st.divider()
        from config.settings import GEMINI_API_KEY
        if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
            st.success("✅ Gemini API Connected")
        else:
            st.error("❌ API Key Missing")
            st.markdown("[Get Gemini API Key →](https://aistudio.google.com/app/apikey)")

        st.divider()
        from utils.history_manager import get_all_history
        history = get_all_history()
        c1, c2 = st.columns(2)
        c1.metric("Reports", len(history))
        c2.metric("Chats", len(st.session_state.chat_history))
        st.caption("⚕️ Not a substitute for medical advice")
