from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pdfplumber
import pytesseract
from document_utils import classify_docs, validate_docs, extract_income

app = Flask(__name__)
@app.route("/")
def home():
    return send_from_directory("templates", "index.html")

CORS(app)

@app.route('/')
def index():
    return "Mortgage Automation API is running."

@app.route('/upload', methods=['POST'])
def upload_documents():
    files = request.files.getlist("documents")
    extracted_data = []

    for file in files:
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            extracted_data.append({"filename": file.filename, "text": text})

    return jsonify({"data": extracted_data})

@app.route('/process', methods=['POST'])
def process_docs():
    docs = request.json.get("docs")
    sorted_docs = classify_docs(docs)
    validations = validate_docs(docs)
    income = [extract_income(doc["text"]) for doc in docs]

    return jsonify({
        "sorted_docs": sorted_docs,
        "validations": validations,
        "income_summary": income
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
