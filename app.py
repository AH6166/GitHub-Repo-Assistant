import streamlit as st
import os
import tempfile
import zipfile
from github import Github
from sentence_transformers import SentenceTransformer
import chromadb
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
import openai
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize models
embedder = SentenceTransformer('all-MiniLM-L6-v2')
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Chroma client
client = chromadb.PersistentClient(path="./chroma_db")

st.title("GitHub Repo Knowledge Assistant")

# Input method
input_method = st.radio("How to provide the repository?", ("GitHub URL", "Upload ZIP"))

repo_content = None
repo_name = None

if input_method == "GitHub URL":
    github_url = st.text_input("Enter GitHub repository URL (e.g., https://github.com/user/repo)")
    github_token = st.text_input("GitHub Token (optional, for private repos)", type="password")
    
    if st.button("Load Repository"):
        if github_url:
            try:
                # Parse URL
                parts = github_url.rstrip('/').split('/')
                if len(parts) >= 2:
                    owner = parts[-2]
                    repo = parts[-1]
                    repo_name = f"{owner}/{repo}"
                    
                    g = Github(github_token) if github_token else Github()
                    repo_obj = g.get_repo(repo_name)
                    
                    # Get all files
                    contents = repo_obj.get_contents("")
                    files = []
                    
                    def get_files(contents):
                        for content in contents:
                            if content.type == "file":
                                files.append((content.path, content.decoded_content.decode('utf-8', errors='ignore')))
                            elif content.type == "dir":
                                get_files(repo_obj.get_contents(content.path))
                    
                    get_files(contents)
                    
                    repo_content = files
                    st.success(f"Loaded {len(files)} files from {repo_name}")
                else:
                    st.error("Invalid GitHub URL")
            except Exception as e:
                st.error(f"Error loading repository: {str(e)}")
        else:
            st.error("Please enter a GitHub URL")

elif input_method == "Upload ZIP":
    uploaded_file = st.file_uploader("Upload repository ZIP file", type="zip")
    
    if uploaded_file is not None and st.button("Process ZIP"):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "repo.zip")
                with open(zip_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find the repo directory (assuming it's the only dir or first)
                repo_dir = None
                for item in os.listdir(temp_dir):
                    if os.path.isdir(os.path.join(temp_dir, item)) and item != "__MACOSX":
                        repo_dir = os.path.join(temp_dir, item)
                        repo_name = item
                        break
                
                if repo_dir:
                    files = []
                    for root, dirs, filenames in os.walk(repo_dir):
                        for filename in filenames:
                            filepath = os.path.join(root, filename)
                            try:
                                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read()
                                rel_path = os.path.relpath(filepath, repo_dir)
                                files.append((rel_path, content))
                            except:
                                pass  # Skip binary files
                    
                    repo_content = files
                    st.success(f"Processed {len(files)} files from {repo_name}")
                else:
                    st.error("Could not find repository directory in ZIP")
        except Exception as e:
            st.error(f"Error processing ZIP: {str(e)}")

# If repo loaded, process and store
if repo_content and repo_name:
    if st.button("Process and Index Repository"):
        with st.spinner("Processing repository..."):
            # Create collection
            collection_name = repo_name.replace('/', '_')
            try:
                client.delete_collection(collection_name)
            except:
                pass
            collection = client.create_collection(name=collection_name)
            
            # Chunk and embed
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = []
            
            for file_path, content in repo_content:
                if content.strip():  # Skip empty files
                    chunks = text_splitter.split_text(content)
                    for i, chunk in enumerate(chunks):
                        doc_id = f"{file_path}_{i}"
                        documents.append(Document(page_content=chunk, metadata={"source": file_path}))
            
            # Create vector store
            embeddings = OpenAIEmbeddings()
            vectorstore = Chroma.from_documents(documents, embeddings, collection_name=collection_name)
            
            st.session_state.vectorstore = vectorstore
            st.session_state.repo_name = repo_name
            st.success("Repository indexed successfully!")

# Question answering
if 'vectorstore' in st.session_state:
    st.header(f"Ask questions about {st.session_state.repo_name}")
    question = st.text_input("Enter your question:")
    
    if st.button("Ask"):
        if question:
            with st.spinner("Thinking..."):
                qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=st.session_state.vectorstore.as_retriever())
                answer = qa_chain.run(question)
                st.write("**Answer:**", answer)
        else:
            st.error("Please enter a question")