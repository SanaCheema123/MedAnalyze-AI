import streamlit as st
from utils.gemini_service import chat_with_ai


def render_chat():
    st.title("💬 Chat with AI")

    if not st.session_state.get("analysis_result"):
        st.warning("⚠️ No report analyzed yet.")
        st.info("Please go to **Analyze Report** first, then come back to chat.")
        if st.button("📋 Go to Analyze Report", type="primary"):
            st.session_state.page = "Analyze Report"
            st.rerun()
        return

    st.caption(f"💡 Chatting about: **{st.session_state.uploaded_report}**")
    st.divider()

    if not st.session_state.chat_history:
        st.markdown("""
        <div style='text-align:center; padding:20px; color:#888;'>
            <p>Ask anything about your medical report below 👇</p>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask about your report...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("🧠 Thinking..."):
                response = chat_with_ai(
                    user_message=user_input,
                    analysis_context=st.session_state.analysis_result,
                    chat_history=st.session_state.chat_history,
                )
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    if st.session_state.chat_history:
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        with col2:
            chat_export = "\n\n".join([
                f"{m['role'].upper()}: {m['content']}"
                for m in st.session_state.chat_history
            ])
            st.download_button(
                "📥 Export Chat",
                data=chat_export,
                file_name="chat_export.txt",
                mime="text/plain",
                use_container_width=True,
            )

    st.divider()
    st.subheader("💡 Suggested Questions")
    suggestions = [
        "What are the most critical findings in this report?",
        "Which values are outside the normal range?",
        "What specialist should I see based on these results?",
        "Can you explain what these results mean in simple terms?",
        "What lifestyle changes do these results suggest?",
        "Is this an emergency or can I wait for a regular appointment?",
    ]
    cols = st.columns(3)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(suggestion, use_container_width=True, key=f"sug_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": suggestion})
                response = chat_with_ai(
                    user_message=suggestion,
                    analysis_context=st.session_state.analysis_result,
                    chat_history=st.session_state.chat_history,
                )
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
