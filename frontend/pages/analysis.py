import streamlit as st
from utils.file_processor import validate_file, process_uploaded_file
from utils.gemini_service import analyze_medical_report, analyze_medical_image
from utils.history_manager import save_analysis


def render_analysis():
    st.title("📋 Analyze Medical Report")
    st.caption("Upload your report below. Supported formats: PDF, TXT, PNG, JPG")
    st.divider()

    uploaded_file = st.file_uploader(
        "📤 Drop your medical report here",
        type=["pdf", "txt", "png", "jpg", "jpeg"],
        help="Max file size: 10 MB",
    )

    with st.expander("➕ Add additional context (optional)"):
        extra_context = st.text_area(
            "Patient notes / additional information",
            placeholder="e.g. Patient is 45 years old, diabetic, taking metformin...",
            height=100,
        )

    st.divider()

    analyze_btn = st.button(
        "🔍 Analyze Report", type="primary",
        use_container_width=True,
        disabled=(uploaded_file is None),
    )

    if analyze_btn and uploaded_file is not None:
        if not validate_file(uploaded_file):
            return

        with st.spinner("🧠 Analyzing your report with Gemini AI... Please wait."):
            file_data = process_uploaded_file(uploaded_file)

            if file_data["type"] == "error":
                st.error(file_data["content"])
                return

            if file_data["type"] == "text":
                content = file_data["content"]
                if extra_context.strip():
                    content += f"\n\nADDITIONAL CONTEXT:\n{extra_context}"
                result = analyze_medical_report(content)
            else:
                result = analyze_medical_image(
                    file_data["content"],
                    file_data.get("mime_type", "image/png"),
                )

        if result.startswith("❌"):
            st.error(result)
            return

        st.session_state.analysis_result = result
        st.session_state.uploaded_report = uploaded_file.name
        st.session_state.chat_history    = []
        save_analysis(uploaded_file.name, result)
        st.success("✅ Analysis complete!")

    if st.session_state.analysis_result:
        st.divider()
        st.subheader(f"📊 Analysis: {st.session_state.uploaded_report}")
        st.markdown(st.session_state.analysis_result)
        st.divider()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                "📥 Download Analysis",
                data=st.session_state.analysis_result,
                file_name=f"analysis_{st.session_state.uploaded_report}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col2:
            if st.button("💬 Ask Follow-up Questions",
                         use_container_width=True, type="secondary"):
                st.session_state.page = "Chat with AI"
                st.rerun()
        with col3:
            if st.button("🔄 Analyze Another Report", use_container_width=True):
                st.session_state.analysis_result = None
                st.session_state.uploaded_report = None
                st.rerun()
    else:
        st.markdown("""
        <div style='text-align:center; padding:40px; color:#888;'>
            <h3>👆 Upload a report above to get started</h3>
            <p>Your analysis will appear here</p>
        </div>
        """, unsafe_allow_html=True)
