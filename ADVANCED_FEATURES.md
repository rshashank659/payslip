# Advanced Features and Customization Guide

## Table of Contents
1. [Adding Company Logo](#adding-company-logo)
2. [Customizing PDF Layout](#customizing-pdf-layout)
3. [Multi-Language Support](#multi-language-support)
4. [Cloud Integration](#cloud-integration)
5. [Automated Scheduling](#automated-scheduling)
6. [Custom Email Templates](#custom-email-templates)
7. [Excel Format Payslips](#excel-format-payslips)
8. [Digital Signatures](#digital-signatures)
9. [Batch Processing](#batch-processing)
10. [Integration with HR Systems](#integration-with-hr-systems)

---

## Adding Company Logo

### 1. Prepare Logo Image
- Format: PNG or JPG
- Recommended size: 200x100 pixels
- Place in project folder as `company_logo.png`

### 2. Modify PDF Generator

In `payslip_generator.py`, add to `generate_payslip_pdf()` function:

```python
# After creating canvas
from reportlab.lib.utils import ImageReader

# Add logo
if os.path.exists('company_logo.png'):
    logo = ImageReader('company_logo.png')
    c.drawImage(logo, 50, height - 80, width=100, height=50, 
                preserveAspectRatio=True, mask='auto')
```

---

## Customizing PDF Layout

### Change Fonts

```python
# In generate_payslip_pdf function
c.setFont("Times-Roman", 12)  # Instead of Helvetica

# Available fonts:
# Helvetica, Helvetica-Bold, Helvetica-Oblique
# Times-Roman, Times-Bold, Times-Italic
# Courier, Courier-Bold, Courier-Oblique
```

### Change Colors

```python
# Set text color (RGB values 0-1)
c.setFillColorRGB(0, 0, 0.5)  # Dark blue

# Set background color
c.setFillColorRGB(0.9, 0.9, 0.9)  # Light gray
c.rect(x, y, width, height, fill=1)
```

### Add Page Numbers

```python
# At end of generate_payslip_pdf
page_num = f"Page 1 of 1"
c.setFont("Helvetica", 8)
c.drawRightString(width - 50, 30, page_num)
```

### Add QR Code

```python
# Install: pip install qrcode[pil]
import qrcode
from io import BytesIO

# Generate QR code
qr = qrcode.QRCode(version=1, box_size=3)
qr.add_data(f"EMP:{employee_data['EMP_ID']};MONTH:{employee_data['Month']}")
qr.make(fit=True)

# Create image
qr_img = qr.make_image(fill_color="black", back_color="white")
buffer = BytesIO()
qr_img.save(buffer, format='PNG')
buffer.seek(0)

# Add to PDF
c.drawImage(ImageReader(buffer), width - 100, 50, width=70, height=70)
```

---

## Multi-Language Support

### 1. Create Translation Dictionary

```python
translations = {
    'en': {
        'net_pay': 'Net Pay',
        'gross_earning': 'Gross Earning',
        'deductions': 'Deductions'
    },
    'hi': {
        'net_pay': 'नेट वेतन',
        'gross_earning': 'सकल कमाई',
        'deductions': 'कटौती'
    }
}
```

### 2. Add Language Parameter

```python
def generate_payslip_pdf(self, employee_data: Dict, output_path: str, 
                         language: str = 'en') -> bool:
    trans = translations[language]
    
    # Use translations
    c.drawString(x, y, trans['net_pay'])
```

---

## Cloud Integration

### Google Drive Upload

```python
# Install: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

from googleapiclient.discovery import build
from google.oauth2 import service_account

def upload_to_drive(file_path, folder_id=None):
    """Upload payslip to Google Drive"""
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json', scopes=SCOPES)
    
    service = build('drive', 'v3', credentials=credentials)
    
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id] if folder_id else []
    }
    
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()
    
    return file.get('webViewLink')
```

### Dropbox Upload

```python
# Install: pip install dropbox

import dropbox

def upload_to_dropbox(file_path, access_token):
    """Upload payslip to Dropbox"""
    dbx = dropbox.Dropbox(access_token)
    
    with open(file_path, 'rb') as f:
        dbx.files_upload(
            f.read(),
            f'/Payslips/{os.path.basename(file_path)}',
            mode=dropbox.files.WriteMode.overwrite
        )
```

---

## Automated Scheduling

### Windows Task Scheduler

Create `run_monthly_payslips.bat`:
```batch
@echo off
cd C:\PayslipGenerator
python payslip_generator.py monthly_payroll.csv
echo Process completed at %date% %time% >> scheduler.log
```

Schedule in Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Monthly Payslip Generation"
4. Trigger: Monthly (select day)
5. Action: Start a program
   - Program: `C:\PayslipGenerator\run_monthly_payslips.bat`

### Linux/Mac Cron Job

```bash
# Edit crontab
crontab -e

# Add line (runs on 1st of every month at 9 AM)
0 9 1 * * cd /home/user/PayslipGenerator && python3 payslip_generator.py monthly_payroll.csv >> cron.log 2>&1
```

### Python Scheduler (APScheduler)

```python
# Install: pip install apscheduler

from apscheduler.schedulers.blocking import BlockingScheduler

def monthly_job():
    generator = PayslipGenerator('config.json')
    generator.process_payslips('monthly_payroll.csv')

scheduler = BlockingScheduler()
scheduler.add_job(monthly_job, 'cron', day=1, hour=9)  # 1st of month, 9 AM
scheduler.start()
```

---

## Custom Email Templates

### HTML Email Template

Create `email_template.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background-color: #4CAF50; color: white; padding: 20px; }
        .content { padding: 20px; }
        .footer { background-color: #f1f1f1; padding: 10px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Payslip for {{MONTH}}</h2>
    </div>
    <div class="content">
        <p>Dear {{NAME}},</p>
        <p>Please find attached your payslip for {{MONTH}}.</p>
        <p><strong>Net Salary: ₹{{NET_PAY}}</strong></p>
        <p>If you have any questions, please contact HR.</p>
    </div>
    <div class="footer">
        <p>This is an automated email. Please do not reply.</p>
    </div>
</body>
</html>
```

### Use Template in Code

```python
def send_email_with_template(self, to_email, employee_name, net_pay, month, payslip_path):
    with open('email_template.html', 'r') as f:
        template = f.read()
    
    # Replace placeholders
    html_body = template.replace('{{NAME}}', employee_name)
    html_body = html_body.replace('{{MONTH}}', month)
    html_body = html_body.replace('{{NET_PAY}}', f'{net_pay:,.2f}')
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg.attach(MIMEText(html_body, 'html'))
    # ... rest of email code
```

---

## Excel Format Payslips

```python
# Install: pip install openpyxl xlsxwriter

def generate_payslip_excel(self, employee_data: Dict, output_path: str):
    """Generate Excel format payslip"""
    import xlsxwriter
    
    workbook = xlsxwriter.Workbook(output_path)
    worksheet = workbook.add_worksheet('Payslip')
    
    # Formats
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4CAF50',
        'font_color': 'white',
        'align': 'center'
    })
    
    bold_format = workbook.add_format({'bold': True})
    money_format = workbook.add_format({'num_format': '₹#,##0.00'})
    
    # Company header
    worksheet.merge_range('A1:F1', 'RS MAN-TECH', header_format)
    worksheet.write('A2', 'Salary Slip for ' + employee_data['Month'])
    
    # Employee details
    row = 4
    worksheet.write(row, 0, 'Employee ID:', bold_format)
    worksheet.write(row, 1, employee_data['EMP_ID'])
    # ... continue with other fields
    
    # Earnings and deductions table
    worksheet.write(10, 0, 'Earnings', header_format)
    worksheet.write(10, 3, 'Deductions', header_format)
    # ... add rows
    
    # Net pay
    worksheet.write(20, 0, 'Net Pay:', bold_format)
    worksheet.write(20, 1, employee_data['Net_Pay'], money_format)
    
    workbook.close()
```

---

## Digital Signatures

### Using ReportLab Signature

```python
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def add_signature(self, pdf_path, signature_image):
    """Add digital signature to PDF"""
    from PyPDF2 import PdfFileWriter, PdfFileReader
    from reportlab.pdfgen import canvas
    from io import BytesIO
    
    # Create signature overlay
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # Add signature image
    sig_img = ImageReader(signature_image)
    can.drawImage(sig_img, 400, 50, width=100, height=50, 
                  preserveAspectRatio=True)
    
    # Add text
    can.setFont("Helvetica", 8)
    can.drawString(400, 40, "Authorized Signatory")
    can.save()
    
    # Merge with existing PDF
    packet.seek(0)
    overlay = PdfFileReader(packet)
    existing = PdfFileReader(open(pdf_path, "rb"))
    output = PdfFileWriter()
    
    page = existing.getPage(0)
    page.mergePage(overlay.getPage(0))
    output.addPage(page)
    
    with open(pdf_path, "wb") as f:
        output.write(f)
```

---

## Batch Processing

### Process Multiple Months

```python
def process_multiple_months(self, csv_directory):
    """Process payslips for multiple months"""
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        month_name = csv_file.replace('_payroll.csv', '')
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing {month_name}")
        logger.info(f"{'='*60}")
        
        self.process_payslips(os.path.join(csv_directory, csv_file))
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_employee_parallel(self, employee_data):
    """Process single employee (for parallel execution)"""
    # ... same logic as current processing
    pass

def process_payslips_parallel(self, csv_file, max_workers=5):
    """Process payslips in parallel"""
    df = self.load_employee_data(csv_file)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(self.process_employee_parallel, row.to_dict()): idx
            for idx, row in df.iterrows()
        }
        
        for future in as_completed(futures):
            idx = futures[future]
            try:
                future.result()
                logger.info(f"Completed employee {idx + 1}")
            except Exception as e:
                logger.error(f"Error processing employee {idx + 1}: {e}")
```

---

## Integration with HR Systems

### REST API Endpoint

```python
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

@app.route('/generate-payslips', methods=['POST'])
def generate_payslips_api():
    """API endpoint to trigger payslip generation"""
    data = request.json
    csv_path = data.get('csv_file')
    
    if not csv_path or not os.path.exists(csv_path):
        return jsonify({'error': 'Invalid CSV file'}), 400
    
    # Run in background
    def run_generator():
        generator = PayslipGenerator('config.json')
        generator.process_payslips(csv_path)
    
    thread = threading.Thread(target=run_generator)
    thread.start()
    
    return jsonify({'status': 'Processing started'}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Database Integration

```python
import sqlite3

def save_to_database(self, employee_data, payslip_path):
    """Save payslip record to database"""
    conn = sqlite3.connect('payroll.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO payslips 
        (emp_id, name, month, net_pay, pdf_path, generated_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    ''', (
        employee_data['EMP_ID'],
        employee_data['Name'],
        employee_data['Month'],
        employee_data['Net_Pay'],
        payslip_path
    ))
    
    conn.commit()
    conn.close()
```

---

## Performance Optimization

### 1. Batch Email Sending

```python
def send_batch_emails(self, email_list, delay=1):
    """Send emails in batches with delays"""
    for idx, email_data in enumerate(email_list):
        self.send_email(**email_data)
        
        # Delay to avoid rate limiting
        if (idx + 1) % 50 == 0:
            logger.info("Pausing for 60 seconds...")
            time.sleep(60)
        else:
            time.sleep(delay)
```

### 2. Caching Templates

```python
class PayslipGenerator:
    def __init__(self, config_file):
        # ... existing code
        self._template_cache = {}
    
    def get_template(self, template_name):
        """Cache templates for reuse"""
        if template_name not in self._template_cache:
            with open(template_name, 'r') as f:
                self._template_cache[template_name] = f.read()
        return self._template_cache[template_name]
```

### 3. Memory Management

```python
import gc

def process_payslips(self, csv_file, chunk_size=100):
    """Process in chunks to manage memory"""
    df = self.load_employee_data(csv_file)
    total = len(df)
    
    for start_idx in range(0, total, chunk_size):
        end_idx = min(start_idx + chunk_size, total)
        chunk = df.iloc[start_idx:end_idx]
        
        # Process chunk
        for idx, row in chunk.iterrows():
            self.process_employee(row.to_dict())
        
        # Force garbage collection
        gc.collect()
        logger.info(f"Processed {end_idx}/{total} employees")
```

---

## Security Enhancements

### 1. Encrypt Configuration

```python
# Install: pip install cryptography

from cryptography.fernet import Fernet

def encrypt_config():
    """Encrypt sensitive configuration"""
    key = Fernet.generate_key()
    cipher = Fernet(key)
    
    with open('config.json', 'rb') as f:
        encrypted = cipher.encrypt(f.read())
    
    with open('config.encrypted', 'wb') as f:
        f.write(encrypted)
    
    # Save key securely
    with open('secret.key', 'wb') as f:
        f.write(key)
```

### 2. PDF Password Protection

```python
from PyPDF2 import PdfFileWriter, PdfFileReader

def password_protect_pdf(input_path, output_path, password):
    """Add password protection to PDF"""
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(open(input_path, 'rb'))
    
    for page_num in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page_num))
    
    pdf_writer.encrypt(password)
    
    with open(output_path, 'wb') as f:
        pdf_writer.write(f)
```

---

## Monitoring and Analytics

### Generate Reports

```python
def generate_summary_report(self):
    """Generate processing summary report"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_processed': self.success_count + self.error_count,
        'successful': self.success_count,
        'failed': self.error_count,
        'email_stats': {
            'sent': self.email_success,
            'failed': self.email_failed
        },
        'whatsapp_stats': {
            'sent': self.whatsapp_success,
            'failed': self.whatsapp_failed
        }
    }
    
    with open('processing_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    return report
```

---

For more customization ideas or help implementing these features, refer to the main documentation or create custom modules based on your specific needs.
