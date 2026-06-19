from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Load documents
import os
from langchain_community.document_loaders import TextLoader

docs = []

for file in os.listdir("knowledge_base"):
    if file.endswith(".txt"):
        loader = TextLoader(
            os.path.join("knowledge_base", file),
            encoding="utf-8"
        )
        docs.extend(loader.load())


# Split documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

documents = splitter.split_documents(docs)

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Create vector db
db = Chroma.from_documents(
    documents,
    embedding_model,
    persist_directory="vectorstore"
)

print("Vector database created")