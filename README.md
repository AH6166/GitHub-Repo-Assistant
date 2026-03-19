# GitHub-Repo-Assistant
Answer natural-language questions over codebases

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
