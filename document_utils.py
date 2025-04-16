from transformers import pipeline
import re

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
labels = ["bank statement", "payslip", "tax return", "employment letter", "id proof"]

def classify_docs(docs):
    results = []
    for doc in docs:
        result = classifier(doc["text"], labels)
        results.append({
            "filename": doc["filename"],
            "classification": result["labels"][0],
            "confidence": result["scores"][0]
        })
    return results

def validate_docs(docs):
    checks = []
    for doc in docs:
        missing = []
        if "payslip" in doc.get("classification", "").lower():
            for kw in ["gross pay", "net pay", "period", "employee"]:
                if kw not in doc["text"].lower():
                    missing.append(kw)
        checks.append({
            "filename": doc["filename"],
            "missing_fields": missing
        })
    return checks

def extract_income(text):
    gross = re.findall(r'Gross Pay[:\s]*\$?([\d,]+)', text)
    net = re.findall(r'Net Pay[:\s]*\$?([\d,]+)', text)
    return {
        "gross": gross[0].replace(',', '') if gross else None,
        "net": net[0].replace(',', '') if net else None
    }
