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
    page_title="Academic Paper Summarizer",
    layout="centered"
)

st.title("📄 Academic Paper Summarizer (RAG)")
st.write("This tool summarizes academic papers using Retrieval Augmented Generation.")

# Load PDF from data folder

pdf_path = "data/paper.pdf"

if not os.path.exists(pdf_path):
    st.error("paper.pdf not found in data folder")
else:
    if st.button("Generate Summary"):
        with st.spinner("Reading and summarizing the paper..."):

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

        st.subheader("📌 Paper Summary")
        st.write(summary["result"])
