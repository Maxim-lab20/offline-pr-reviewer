from flask import Flask, request, jsonify
from llm_service import LLMService

app = Flask(__name__)

# Initialize the service with Ollama model
llm_service = LLMService(model_name="gemma:2b")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = llm_service.ask(question)
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
