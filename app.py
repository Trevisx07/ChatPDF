import streamlit as st
from pdf_processor import extract_text_from_pdf, chunk_text
from vectorstore import build_or_load_vectorstore
from llm_chain import get_qa_chain
from voice_module import listen_from_mic, convert_text_to_audio, play_audio

st.set_page_config(page_title="Smart PDF Chat with Voice & LangChain RAG", layout="wide")
st.title("📚 Smart PDF Voice Assistant")

uploaded_file = st.file_uploader("📄 Upload your PDF", type="pdf")

if uploaded_file:
    with open("sample.pdf", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("🔍 Extracting and processing..."):
        text = extract_text_from_pdf("sample.pdf")
        chunks = chunk_text(text)
        vectorstore = build_or_load_vectorstore(chunks)
        qa_chain = get_qa_chain(vectorstore)
    st.success("✅ Document ready for Q&A!")

    mode = st.radio("Choose input mode:", ["📝 Type Question", "🎤 Speak Question"])

    if mode == "📝 Type Question":
        question = st.text_input("Ask a question:")
    else:
        if st.button("🎤 Start Voice Input"):
            question = listen_from_mic()
            st.text_input("Recognized Question:", value=question, key="voice_question")
    question = st.text_input("❓ Ask a question about the PDF")

    if st.button("💬 Get Answer") and question:
        with st.spinner("💡 Thinking..."):
            result = qa_chain({"query": question})
            answer = result["result"]

        st.markdown("### ✅ Answer:")
        st.write(answer)

    
        audio_path = convert_text_to_audio(answer)
        play_audio(audio_path)

       
        with st.expander("📚 Source Chunks"):
            for doc in result["source_documents"]:
                st.write(doc.page_content)
