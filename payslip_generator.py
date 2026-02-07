"""
Payslip Generator - Automated Employee Payslip Generation and Distribution System
Generates PDF payslips from CSV data and sends via Email and WhatsApp
"""

import pandas as pd
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# WhatsApp integration (optional)
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("payslip_generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PayslipGenerator:

    def __init__(self, config_file: str = "config.json"):
        self.config = self._load_config(config_file)
        self.output_dir = Path(self.config.get("output_directory", "payslips"))
        self.output_dir.mkdir(exist_ok=True)

        self.success_count = 0
        self.error_count = 0
        self.email_success = 0
        self.email_failed = 0

    # ---------------- CONFIG ----------------
    def _load_config(self, config_file: str) -> Dict:
        with open(config_file, "r") as f:
            return json.load(f)

    # ---------------- CSV ----------------
    def load_employee_data(self, csv_file: str) -> pd.DataFrame:
        df = pd.read_csv(csv_file)

        required = ["EMP_ID", "Name", "Email"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        return df

    # ---------------- NUMBER TO WORDS ----------------
    def number_to_words(self, num: float) -> str:
        ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
        teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen',
                 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']

        def convert(n):
            if n < 10:
                return ones[n]
            if n < 20:
                return teens[n - 10]
            if n < 100:
                return tens[n // 10] + (' ' + ones[n % 10] if n % 10 else '')
            return ones[n // 100] + ' Hundred' + (' ' + convert(n % 100) if n % 100 else '')

        num = int(num)
        if num == 0:
            return "Zero Rupees Only"

        result = ""
        if num >= 100000:
            result += convert(num // 100000) + " Lakh "
            num %= 100000
        if num >= 1000:
            result += convert(num // 1000) + " Thousand "
            num %= 1000
        if num > 0:
            result += convert(num)

        return result.strip() + " Rupees Only"

    # ---------------- PDF ----------------
    def generate_payslip_pdf(self, employee_data: Dict, output_path: str) -> bool:
        try:
            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4

            # -------- LOGO --------
            logo_path = os.path.join("assets", "image.png")
            if os.path.exists(logo_path):
                c.drawImage(
                    logo_path,
                    x=50,
                    y=height - 90,
                    width=1.5 * inch,
                    height=1.0 * inch,
                    preserveAspectRatio=True,
                    mask="auto"
                )

            # -------- HEADER --------
            y = height - 120
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(width / 2, y, "FORM XIX - WAGE SLIP")

            y -= 20
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(width / 2, y, "RS MAN-TECH")

            y -= 14
            c.setFont("Helvetica", 9)
            c.drawCentredString(width / 2, y, "#14, 3rd Cross, Parappana Agrahara, Bangalore-100")

            # -------- EMPLOYEE DETAILS --------
            y -= 40
            left, right = 70, 320

            def label(x, y, text):
                c.setFont("Helvetica-Bold", 9)
                c.drawString(x, y, text)

            def value(x, y, text):
                c.setFont("Helvetica", 9)
                c.drawString(x, y, str(text))

            label(left, y, "EMP Code:")
            value(left + 100, y, employee_data.get("EMP_ID"))

            label(right, y, "Designation:")
            value(right + 90, y, employee_data.get("Designation", "N/A"))

            y -= 18
            label(left, y, "Name:")
            value(left + 100, y, employee_data.get("Name"))

            label(right, y, "Bank A/c:")
            value(right + 90, y, employee_data.get("Bank_AC", "N/A"))

            y -= 18
            label(left, y, "UAN:")
            value(left + 100, y, employee_data.get("UAN_No", "N/A"))

            label(right, y, "DOJ:")
            value(right + 90, y, employee_data.get("DOJ", "N/A"))

            # -------- NET PAY --------
            y -= 40
            net = employee_data.get("Net_Pay", 0)

            c.setFont("Helvetica-Bold", 10)
            c.drawString(left, y, f"Net Pay: ₹ {net:.2f}")

            y -= 18
            c.setFont("Helvetica", 8)
            c.drawString(left, y, self.number_to_words(net))

            # -------- FOOTER --------
            y -= 30
            c.setFont("Helvetica-Oblique", 7)
            c.drawCentredString(width / 2, y, "This is a system generated payslip. No signature required.")

            c.save()
            logger.info(f"PDF generated: {output_path}")
            return True

        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return False

    # ---------------- EMAIL ----------------
    def send_email(self, to_email: str, name: str, pdf_path: str, month: str) -> bool:
        try:
            email_cfg = self.config["email"]
            if not email_cfg.get("enabled"):
                return False

            msg = MIMEMultipart()
            msg["From"] = email_cfg["sender_email"]
            msg["To"] = to_email
            msg["Subject"] = f"Payslip - {month}"

            body = f"""Dear {name},

Please find attached your payslip for {month}.

Regards,
RS MAN-TECH HR
"""
            msg.attach(MIMEText(body, "plain"))

            with open(pdf_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(pdf_path)}"')
                msg.attach(part)

            server = smtplib.SMTP(email_cfg["smtp_server"], email_cfg["smtp_port"])
            server.starttls()
            server.login(email_cfg["sender_email"], email_cfg["password"])
            server.send_message(msg)
            server.quit()

            return True

        except Exception as e:
            logger.error(f"Email failed: {e}")
            return False

    # ---------------- PROCESS ----------------
    def process_payslips(self, csv_file: str):
        df = self.load_employee_data(csv_file)

        for _, row in df.iterrows():
            data = row.to_dict()
            name = data.get("Name")
            month = data.get("Month", datetime.now().strftime("%B-%Y"))
            file_name = f"{data['EMP_ID']}_{month}.pdf"
            path = self.output_dir / file_name

            if self.generate_payslip_pdf(data, str(path)):
                self.success_count += 1
                if self.send_email(data["Email"], name, str(path), month):
                    self.email_success += 1
            else:
                self.error_count += 1

        logger.info(f"Done | PDFs: {self.success_count} | Emails: {self.email_success}")


# ---------------- MAIN ----------------
def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python payslip_generator.py employees.csv")
        return

    gen = PayslipGenerator("config.json")
    gen.process_payslips(sys.argv[1])


if __name__ == "__main__":
    main()
