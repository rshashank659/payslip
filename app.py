# app.py
# Full-featured Payslip Generator Frontend (Python-only, Flask)
# Run: python app.py

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
import os
import subprocess
import pandas as pd
import zipfile
from datetime import datetime

app = Flask(__name__)
app.secret_key = "payslip_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
PAYSLIP_FOLDER = os.path.join(BASE_DIR, "payslips")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PAYSLIP_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"csv","xlsx","xls"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("csv_file")
    month = request.form.get("month")

    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only CSV or Excel files allowed"}), 400

    # Preserve original extension
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Read file correctly
    if ext == "csv":
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    # Save a CSV copy for payslip_generator.py
    csv_path = filepath.replace(f".{ext}", ".csv")
    df.to_csv(csv_path, index=False)

    # 👉 RUN payslip generator in correct directory
    generator_script = os.path.join(BASE_DIR, "payslip_generator.py")

    result = subprocess.run(
        ["python", generator_script, csv_path],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return jsonify({
            "error": "Payslip generation failed",
            "details": result.stderr
        }), 500

    preview = df.head(10).to_dict(orient="records")

    return jsonify({
        "message": "Payslips generated successfully",
        "preview": preview
    })


@app.route("/download", methods=["GET"])
def download_zip():
    zip_path = os.path.join(BASE_DIR, "payslips.zip")

    pdf_files = [
        f for f in os.listdir(PAYSLIP_FOLDER)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        return jsonify({
            "error": "No payslip PDFs found to download"
        }), 400

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in pdf_files:
            zipf.write(
                os.path.join(PAYSLIP_FOLDER, file),
                file
            )

    return send_file(zip_path, as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True)