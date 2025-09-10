from flask import Flask, request, jsonify
from service.llm_service import LLMService
from service.review_service import ReviewService

app = Flask(__name__)

llm_service = LLMService()
review_service = ReviewService()

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
    data = request.get_json()
    code_snippet = data.get("code_snippet", "")
    if not code_snippet:
        return jsonify({"error": "No code snippet provided"}), 400

    review_result = review_service.decide_and_review(code_snippet)

    return jsonify({"review": review_result})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
