import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA

# CONFIG
load_dotenv()

st.set_page_config(
    page_title="ScholarSense | AI Academic Paper Summarizer",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for a premium look
st.markdown("""
    <style>
    /* Main background and font */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Center the title */
    .main-title {
        font-size: 3rem !important;
        font-weight: 800;
        text-align: center;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
        letter-spacing: -0.05rem;
    }
    
    .sub-title {
        font-size: 1.2rem;
        text-align: center;
        color: #4b5563;
        margin-bottom: 2rem;
    }

    /* Glassmorphism containers */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 1.5rem;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        margin-bottom: 2rem;
    }

    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.75rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
        border: none;
        color: white;
    }

    /* Output header */
    .summary-header {
        color: #1e3a8a;
        font-size: 1.8rem;
        font-weight: 700;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6b7280;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🎓 ScholarSense</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AI-Powered Academic Paper Summarization via RAG</p>', unsafe_allow_html=True)

# Centering the UI elements
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    pdf_path = "data/paper.pdf"
    
    if not os.path.exists(pdf_path):
        st.error("🚨 paper.pdf not found in 'data/' folder. Please add your PDF file.")
    else:
        st.info(f"📂 Detected Paper: **{os.path.basename(pdf_path)}**")
        
        if st.button("✨ Generate Intelligent Summary"):
            with st.spinner("🧠 Analyzing and distilling research content..."):

                # Read PDF
                reader = PdfReader(pdf_path)
                paper_text = ""
                for page in reader.pages:
                    paper_text += page.extract_text()

                # Split text into chunks
                splitter = CharacterTextSplitter(
                    chunk_size=800,
                    chunk_overlap=100
                )
                chunks = splitter.split_text(paper_text)

                # Create embeddings and vector store
                embeddings = OpenAIEmbeddings()
                vectorstore = FAISS.from_texts(chunks, embeddings)

                # Create RAG chain
                llm = OpenAI(temperature=0)
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    retriever=vectorstore.as_retriever()
                )

                # Query for summarization
                query = """
                Summarize this academic paper clearly.
                Include:
                - Problem statement
                - Methodology
                - Key results
                - Conclusion
                """

                summary = qa_chain.invoke(query)

                st.markdown('<h2 class="summary-header">📌 Research Distillation</h2>', unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="glass-card" style="background: white;">
                        {summary["result"]}
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Built with 💙 using LangChain, OpenAI, and FAISS</div>', unsafe_allow_html=True)
