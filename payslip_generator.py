import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
from s3_utils import upload_to_s3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def generate_payslip_pdf(emp_data, month):
    """
    emp_data: dict with employee + salary info
    month: 'Dec-25'
    """

    template = env.get_template("payslip.html")

    html_content = template.render(
        company=emp_data["company"],
        emp=emp_data["emp"],
        salary=emp_data["salary"],
        deduction=emp_data["deduction"],
        net_pay=emp_data["net_pay"],
        net_pay_words=emp_data["net_pay_words"],
        month=month,
    )

    filename = f"{emp_data['emp']['emp_id']}_{month}.pdf"
    local_pdf_path = os.path.join(OUTPUT_DIR, filename)

    HTML(
        string=html_content,
        base_url=BASE_DIR  # IMPORTANT for logo rendering
    ).write_pdf(local_pdf_path)

    # Upload to S3
    s3_key = f"payslips/{month}/{filename}"
    upload_to_s3(local_pdf_path, s3_key)
    # delete temp file
    os.remove(local_pdf_path)
    return {
        "s3_key": s3_key,
    }
