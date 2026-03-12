import streamlit as st
from utils.history_manager import get_all_history, clear_history


def render_history():
    st.title("📂 Analysis History")
    st.caption("All previously analyzed reports are saved here.")
    st.divider()

    history = get_all_history()

    if not history:
        st.markdown("""
        <div style='text-align:center; padding:40px; color:#888;'>
            <h3>📭 No history yet</h3>
            <p>Analyze a report to see it here</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📋 Analyze a Report", type="primary"):
            st.session_state.page = "Analyze Report"
            st.rerun()
        return

    col_a, col_b = st.columns([5, 1])
    with col_a:
        st.subheader(f"📊 {len(history)} Report(s) Analyzed")
    with col_b:
        if st.button("🗑️ Clear All", type="secondary"):
            clear_history()
            st.success("History cleared.")
            st.rerun()

    st.divider()

    for record in reversed(history):
        with st.expander(f"📄 {record['filename']}  —  {record['timestamp']}", expanded=False):
            st.markdown(record["analysis"])
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download",
                    data=record["analysis"],
                    file_name=f"analysis_{record['filename']}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key=f"dl_{record['id']}",
                )
            with col2:
                if st.button("💬 Chat About This",
                             use_container_width=True,
                             key=f"chat_{record['id']}"):
                    st.session_state.analysis_result = record["analysis"]
                    st.session_state.uploaded_report = record["filename"]
                    st.session_state.chat_history    = []
                    st.session_state.page            = "Chat with AI"
                    st.rerun()
