# app.py
# Full-featured Payslip Generator Frontend (Python-only, Flask)
# Run: python3 app.py

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
import os
import sys
import subprocess
import pandas as pd
import zipfile
from datetime import datetime
import traceback
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "payslip_secret_key_change_in_production"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
PAYSLIP_FOLDER = os.path.join(BASE_DIR, "payslips")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PAYSLIP_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "xlsm"}


def get_python_executable():
    """Get the correct Python executable (python3, python, or sys.executable)"""
    # Try to find python3 first (most common on macOS/Linux)
    for cmd in ['python3', 'python', sys.executable]:
        try:
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"Using Python executable: {cmd}")
                return cmd
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    # Fallback to sys.executable
    logger.warning(f"Using fallback Python: {sys.executable}")
    return sys.executable


PYTHON_CMD = get_python_executable()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def dashboard():
    """Render the main dashboard"""
    try:
        return render_template("dashboard.html")
    except Exception as e:
        logger.error(f"Error rendering dashboard: {e}")
        return f"Error loading dashboard: {str(e)}", 500


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle CSV/Excel upload and generate payslips"""
    try:
        logger.info("Upload request received")
        
        # Get file from request
        file = request.files.get("csv_file")
        month = request.form.get("month", datetime.now().strftime("%B-%Y"))

        # Validate file
        if not file or file.filename == "":
            logger.warning("No file selected")
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            logger.warning(f"Invalid file type: {file.filename}")
            return jsonify({"error": "Only CSV or Excel files allowed"}), 400

        logger.info(f"Processing file: {file.filename}")

        # Save file with timestamp
        ext = file.filename.rsplit(".", 1)[1].lower()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"employees_{timestamp}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        file.save(filepath)
        logger.info(f"File saved to: {filepath}")

        # Read file based on extension
        try:
            if ext == "csv":
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
            
            logger.info(f"Loaded {len(df)} records from file")
            
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return jsonify({
                "error": "Failed to read file",
                "details": str(e)
            }), 400

        # Validate required columns
        required_cols = ["EMP_ID", "Name", "Email"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            logger.error(f"Missing required columns: {missing_cols}")
            return jsonify({
                "error": f"Missing required columns: {', '.join(missing_cols)}",
                "details": f"Your CSV must have these columns: {', '.join(required_cols)}"
            }), 400

        # Save as CSV for payslip generator (if not already CSV)
        if ext != "csv":
            csv_path = filepath.replace(f".{ext}", ".csv")
            df.to_csv(csv_path, index=False)
            logger.info(f"Converted to CSV: {csv_path}")
        else:
            csv_path = filepath

        # Run payslip generator
        generator_script = os.path.join(BASE_DIR, "payslip_generator.py")
        
        if not os.path.exists(generator_script):
            logger.error(f"Generator script not found: {generator_script}")
            return jsonify({
                "error": "Payslip generator script not found",
                "details": f"Missing: {generator_script}"
            }), 500

        logger.info(f"Running payslip generator with {PYTHON_CMD}...")
        
        result = subprocess.run(
            [PYTHON_CMD, generator_script, csv_path],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        # Log the output
        if result.stdout:
            logger.info(f"Generator output: {result.stdout}")
        if result.stderr:
            logger.warning(f"Generator stderr: {result.stderr}")

        if result.returncode != 0:
            logger.error(f"Generator failed with code {result.returncode}")
            return jsonify({
                "error": "Payslip generation failed",
                "details": result.stderr or "Unknown error",
                "stdout": result.stdout
            }), 500

        # Prepare preview data
        preview = df.head(10).to_dict(orient="records")
        
        # Clean NaN values for JSON serialization
        for record in preview:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None

        logger.info(f"Successfully processed {len(df)} employees")

        return jsonify({
            "message": f"Successfully generated {len(df)} payslips",
            "preview": preview,
            "total": len(df)
        })

    except subprocess.TimeoutExpired:
        logger.error("Payslip generation timeout")
        return jsonify({
            "error": "Processing timeout",
            "details": "Generation took too long. Try with fewer employees."
        }), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": "Unexpected error occurred",
            "details": str(e),
            "type": type(e).__name__
        }), 500


@app.route("/download", methods=["GET"])
def download_zip():
    """Download all generated payslips as ZIP"""
    try:
        logger.info("Download request received")
        
        zip_path = os.path.join(BASE_DIR, "payslips.zip")

        # Check if payslips folder exists
        if not os.path.exists(PAYSLIP_FOLDER):
            logger.error("Payslips folder not found")
            return jsonify({
                "error": "Payslips folder not found"
            }), 404

        # Get all PDF files
        pdf_files = [
            f for f in os.listdir(PAYSLIP_FOLDER)
            if f.lower().endswith(".pdf")
        ]

        if not pdf_files:
            logger.warning("No PDF files found")
            return jsonify({
                "error": "No payslip PDFs found to download",
                "details": "Generate payslips first"
            }), 400

        logger.info(f"Creating ZIP with {len(pdf_files)} files")

        # Create ZIP file
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in pdf_files:
                file_path = os.path.join(PAYSLIP_FOLDER, file)
                zipf.write(file_path, file)

        logger.info(f"ZIP created successfully: {zip_path}")
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name="payslips.zip",
            mimetype="application/zip"
        )

    except Exception as e:
        logger.error(f"Download error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": "Download failed",
            "details": str(e)
        }), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "python": PYTHON_CMD
    })


@app.route("/stats", methods=["GET"])
def get_stats():
    """Get statistics about generated payslips"""
    try:
        pdf_files = []
        if os.path.exists(PAYSLIP_FOLDER):
            pdf_files = [
                f for f in os.listdir(PAYSLIP_FOLDER)
                if f.lower().endswith(".pdf")
            ]
        
        return jsonify({
            "total_payslips": len(pdf_files),
            "payslips_folder": PAYSLIP_FOLDER,
            "files": pdf_files[:10]  # First 10 files
        })
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({"error": str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal error: {e}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    logger.info("Starting Flask application...")
    logger.info(f"Python executable: {PYTHON_CMD}")
    logger.info(f"Base directory: {BASE_DIR}")
    logger.info(f"Upload folder: {UPLOAD_FOLDER}")
    logger.info(f"Payslip folder: {PAYSLIP_FOLDER}")
    
    app.run(host="0.0.0.0", port=5000, debug=True)