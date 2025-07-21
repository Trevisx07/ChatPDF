from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# Embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Gemini LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Use the following pieces of context to answer the question.

Context:
{context}

Question:
{question}

Answer:
""",
)

def get_qa_chain(faiss_index):
    retriever = faiss_index.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_PROMPT}
    )
    return chain
