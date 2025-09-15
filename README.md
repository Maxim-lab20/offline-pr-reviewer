# Offline PR Reviewers based on the detected language and retrieved context.

## Installation

Follow these steps to set up the project locally:

1.  **Python Installation**

    Ensure you have Python installed. If not, download and install it from [python.org](https://www.python.org/).

2.  **Install Python Dependencies**

    ```bash
    pip install flask langchain langchain-community ollama sentence-transformers faiss-cpu
    ```

3.  **Install Ollama**

    Download and install Ollama from [ollama.com](https://ollama.com/).

    After installation, pull the `gemma:2b` model:

    ```bash
    ollama pull gemma:2b
    ```

## RAG Context

Code standards and other relevant documentation are stored in the `RAG_CONTEXT` directory. These documents are loaded into the FAISS vector database to provide contextual information during code reviews.

- `RAG_CONTEXT/java_code_standards.txt`: Contains specific code standards for Java projects.
- `RAG_CONTEXT/python_code_standards.txt`: Contains specific code standards for Python projects.

## Usage

To run the Flask application, navigate to the root directory of the project (`C:\Users\XARA\Repositories\offline-pr-reviewer`) in your terminal and execute:

```bash
flask --app src.app run
```

Alternatively, you can set the `FLASK_APP` environment variable and then run `flask run`:

```bash
set FLASK_APP=src.app
flask run
```

The application will be available at `http://127.0.0.1:5000/`.

### API Endpoints

-   **`/ask` (POST)**: General LLM interaction.
    -   Request Body: `{"question": "Your question here"}`
    -   Response: `{"answer": "LLM's response"}`

-   **`/review` (POST)**: Code review endpoint.
    -   Request Body: `{"code_snippet": "Your code snippet here"}`
    -   Response: `{"review": "Code review comments"}`