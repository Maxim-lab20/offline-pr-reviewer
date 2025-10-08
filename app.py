import os
from flask import Flask, request, jsonify, Response
from github import Github
from service.gemini_llm_service import GeminiLLMService
from service.review_service import ReviewService
from service.rag_service import RAGService
from langchain_core.documents import Document

app = Flask(__name__)

github_token = os.environ.get("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GITHUB_TOKEN environment variable not set.")
g = Github(github_token)

llm_service = GeminiLLMService()
review_service = ReviewService()
rag_service = RAGService()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = llm_service.ask(question)
    return jsonify({"answer": response})

@app.route("/review", methods=["POST"])
def review_pr():
    code_snippet = request.get_data(as_text=True) or ""
    if not code_snippet.strip():
        return jsonify({"error": "No code snippet provided"}), 400

    review_result = review_service.decide_and_review(code_snippet)
    return Response(review_result or "", mimetype='text/plain')

@app.route("/ingest", methods=["POST"])
def ingest_documents_endpoint():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read file content as text
        file_content = file.read().decode('utf-8')

        # Wrap in Document object
        document = Document(
            page_content=file_content,
            metadata={"source": file.filename}
        )

        # Ingest into vectorstore
        rag_service.ingest_document([document])

        return jsonify({
            "status": "success",
            "message": f"File {file.filename} ingested successfully."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error ingesting file {file.filename}: {e}"
        }), 500

@app.route("/documents", methods=["GET"])
def list_documents_endpoint():
    try:
        limit = int(request.args.get("limit", 10))  # default = 10
        docs = rag_service.list_documents(limit=limit)
        return jsonify({"status": "success", "documents": docs}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/github-webhook", methods=["POST"])
def github_webhook():
    payload = request.get_json()
    print(payload)

    if request.headers.get("X-GitHub-Event") == "pull_request":
        action = payload.get("action")
        if action in ["opened", "synchronize"]:
            pull_request = payload.get("pull_request")
            repo_name = pull_request["base"]["repo"]["full_name"]
            pull_request_number = pull_request["number"]
            print(f"Received PR {pull_request_number} in {repo_name} with action: {action}")
            
            repo = g.get_user().get_repo(repo_name.split("/")[1]) # Assuming repo_name is "owner/repo"
            pr = repo.get_pull(pull_request_number)
            
            for file in pr.get_files():
                if file.patch:
                    print(f"Reviewing file: {file.filename}")
                    review_result = review_service.decide_and_review(file.patch)
                    print(f"Review for {file.filename}: {review_result}")
                    if review_result:
                        pr.create_issue_comment(f"Review for {file.filename}:\n{review_result}")
                
    
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
