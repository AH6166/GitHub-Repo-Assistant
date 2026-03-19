# GitHub-Repo-Assistant
Answer natural-language questions over codebases

## Tech Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.8+
- **Embeddings**: OpenAI Embeddings API
- **Vector Store**: ChromaDB
- **LLM**: OpenAI GPT-3.5-turbo
- **Libraries**: LangChain, PyGitHub, Sentence Transformers

## Architecture
The system ingests codebases from GitHub repositories or ZIP file uploads. Code files are chunked into 1000-character segments with 200-character overlap for optimal processing. OpenAI embeddings capture semantic meaning of each chunk. Embeddings are stored in ChromaDB vector database for efficient similarity search. User questions trigger semantic retrieval of relevant code snippets. Finally, GPT-3.5-turbo generates contextual answers using retrieved information and the original query.

## Setup

1. Clone or download this repository.

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   Get your API key from [OpenAI](https://platform.openai.com/api-keys).

5. Run the application:
   ```
   streamlit run app.py
   ```

## Project Structure
- `app.py`: Main Streamlit application containing the web interface, repository loading logic, embedding generation, and question-answering pipeline
- `requirements.txt`: Python dependencies including Streamlit, LangChain, OpenAI, ChromaDB, and PyGitHub
- `.env.example`: Template file showing required environment variables (copy to `.env` and add your API keys)
- `.gitignore`: Specifies files and directories to exclude from Git (virtual environments, API keys, vector database)
- `README.md`: This documentation file
- `chroma_db/`: Directory created at runtime to store vector embeddings and indexed repository data

## Usage

1. Open the web app in your browser.

2. Choose how to provide the repository:
   - **GitHub URL**: Enter the URL of a public GitHub repository. Optionally provide a GitHub token for private repos.
   - **Upload ZIP**: Upload a ZIP file containing the repository.

3. Click "Load Repository" or "Process ZIP" to load the codebase.

4. Click "Process and Index Repository" to chunk the code, generate embeddings, and store them.

5. Ask questions about the codebase in natural language, such as:
   - "What does this project do?"
   - "How is authentication implemented?"
   - "Which files are related to database logic?"
   - "Summarize the API structure"
   - "Where is this bug likely coming from?"

## Features

- Supports both GitHub repository URLs and ZIP file uploads
- Uses embeddings for semantic search and retrieval
- Leverages OpenAI's GPT model for generating answers
- Persistent storage of indexed repositories using ChromaDB

## Requirements

- Python 3.8+
- OpenAI API key
- GitHub token (optional, for private repositories)
