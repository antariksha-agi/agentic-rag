from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def ingest(pdfpath: str):
    loader = PyPDFLoader(pdfpath)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name= "all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents=texts, embedding=embeddings)
    return vectorstore
    