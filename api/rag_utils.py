
import os
from django.conf import settings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

vector_db = None
qa_chain = None

def initialize_rag():
    global vector_db, qa_chain
    
    # 1. Check if API Key exists
    if not settings.GEMINI_API_KEY:
        print("Warning: GEMINI API Key not found.")
        return


    kb_path = os.path.join(settings.BASE_DIR, 'knowledge_base', 'faq.txt')
    if not os.path.exists(kb_path):
        print(f"Warning: Knowledge base not found at {kb_path}")
        return

    loader = TextLoader(kb_path)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=settings.GEMINI_API_KEY)
    vector_db = FAISS.from_documents(texts, embeddings)

    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(openai_api_key=settings.GEMINI_API_KEY),
        chain_type="stuff",
        retriever=vector_db.as_retriever()
    )
    print("RAG Pipeline Initialized Successfully.")

def get_rag_response(query):
    global qa_chain
    if qa_chain is None:
        initialize_rag()
    
    if qa_chain:
        try:
            return qa_chain.run(query)
        except Exception as e:
            return f"Error generating response: {str(e)}"
    else:
        return "System is not ready. Please check knowledge base setup."