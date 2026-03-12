import streamlit as st


def render_home():
    st.markdown("""
    <div style='text-align:center; padding:40px 0 20px'>
        <h1 style='font-size:3rem;'>🏥 MedAnalyze AI</h1>
        <p style='font-size:1.2rem; color:#888;'>
            Upload your medical report and get instant AI-powered analysis,<br>
            key findings, and personalized next-step recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class='feature-card'>
            <h3>📤 Upload</h3>
            <p>PDF, TXT, or Image reports</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='feature-card'>
            <h3>🔍 Analyze</h3>
            <p>Deep AI-powered report analysis</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='feature-card'>
            <h3>💬 Chat</h3>
            <p>Ask follow-up questions about your report</p>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class='feature-card'>
            <h3>📂 History</h3>
            <p>Access previous analyses anytime</p>
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.subheader("🚀 Quick Start")
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("""
        **How to use MedAnalyze AI:**
        1. Click **Analyze Report** in the sidebar
        2. Upload your medical report (PDF, TXT, or image)
        3. Click **Analyze** to get full AI analysis
        4. Ask follow-up questions in **Chat with AI**
        5. View past analyses in **History**
        """)
    with col_b:
        st.warning("""
        **⚕️ Medical Disclaimer**

        MedAnalyze AI is for **informational purposes only**.
        It does NOT replace professional medical advice,
        diagnosis, or treatment. Always consult a qualified
        healthcare provider for medical decisions.
        """)

    st.divider()
    if st.button("📋 Start Analyzing a Report →", type="primary", use_container_width=True):
        st.session_state.page = "Analyze Report"
        st.rerun()
