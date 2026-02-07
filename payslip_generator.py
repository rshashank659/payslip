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
from typing import Dict, List, Optional
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

# WhatsApp integration (optional - requires Twilio)
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("Warning: Twilio not installed. WhatsApp feature will be disabled.")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('payslip_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PayslipGenerator:
    """Main class for generating and distributing payslips"""
    
    def __init__(self, config_file: str = 'config.json'):
        """Initialize payslip generator with configuration"""
        self.config = self._load_config(config_file)
        self.output_dir = Path(self.config.get('output_directory', 'payslips'))
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize counters
        self.success_count = 0
        self.error_count = 0
        self.email_success = 0
        self.email_failed = 0
        self.whatsapp_success = 0
        self.whatsapp_failed = 0
        
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {config_file} not found")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in configuration file {config_file}")
            raise
    
    def load_employee_data(self, csv_file: str) -> pd.DataFrame:
        """Load and validate employee data from CSV"""
        try:
            df = pd.read_csv(csv_file)
            logger.info(f"Loaded {len(df)} employee records from {csv_file}")
            
            # Validate required columns
            required_columns = ['EMP_ID', 'Name', 'Email']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Log data quality
            null_emails = df['Email'].isnull().sum()
            if null_emails > 0:
                logger.warning(f"{null_emails} employees have missing email addresses")
            
            return df
        except Exception as e:
            logger.error(f"Error loading CSV file: {str(e)}")
            raise
    
    def number_to_words(self, num: float) -> str:
        """Convert number to words (Indian numbering system)"""
        ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
        teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
        
        def convert_less_than_thousand(n):
            if n == 0:
                return ''
            elif n < 10:
                return ones[n]
            elif n < 20:
                return teens[n - 10]
            elif n < 100:
                return tens[n // 10] + (' ' + ones[n % 10] if n % 10 != 0 else '')
            else:
                return ones[n // 100] + ' Hundred' + (' ' + convert_less_than_thousand(n % 100) if n % 100 != 0 else '')
        
        if num == 0:
            return 'Zero Rupees Only'
        
        num = int(num)
        
        if num < 1000:
            result = convert_less_than_thousand(num)
        elif num < 100000:
            thousands = num // 1000
            remainder = num % 1000
            result = convert_less_than_thousand(thousands) + ' Thousand'
            if remainder > 0:
                result += ' ' + convert_less_than_thousand(remainder)
        elif num < 10000000:
            lakhs = num // 100000
            remainder = num % 100000
            result = convert_less_than_thousand(lakhs) + ' Lakh'
            if remainder >= 1000:
                result += ' ' + convert_less_than_thousand(remainder // 1000) + ' Thousand'
            if remainder % 1000 > 0:
                result += ' ' + convert_less_than_thousand(remainder % 1000)
        else:
            crores = num // 10000000
            remainder = num % 10000000
            result = convert_less_than_thousand(crores) + ' Crore'
            if remainder >= 100000:
                result += ' ' + convert_less_than_thousand(remainder // 100000) + ' Lakh'
                remainder = remainder % 100000
            if remainder >= 1000:
                result += ' ' + convert_less_than_thousand(remainder // 1000) + ' Thousand'
            if remainder % 1000 > 0:
                result += ' ' + convert_less_than_thousand(remainder % 1000)
        
        return result.strip() + ' Rupees Only'
    
    def generate_payslip_pdf(self, employee_data: Dict, output_path: str) -> bool:
        """Generate PDF payslip for a single employee"""
        try:
            # Create PDF
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            
            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4
            
            # Company header
            y_position = height - 50
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(width/2, y_position, "Contract Labour (Regulation & Abolition)")
            
            y_position -= 20
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(width/2, y_position, "FORM XIX (See Rules 78(1)(b) Wage Slip)")
            
            y_position -= 25
            c.setFont("Helvetica", 9)
            c.drawCentredString(width/2, y_position, "Name & Address of Contractor")
            
            y_position -= 20
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(width/2, y_position, "RS MAN-TECH")
            
            y_position -= 18
            c.setFont("Helvetica", 8)
            c.drawCentredString(width/2, y_position, "# 14, 3rd Cross, Parappana Agrahara")
            y_position -= 12
            c.drawCentredString(width/2, y_position, "Bangalore-100")
            
            y_position -= 30
            
            # Employee details section (Left and Right columns)
            left_x = 70
            right_x = 320
            
            c.setFont("Helvetica-Bold", 9)
            c.drawString(left_x, y_position, "EMP Code:")
            c.setFont("Helvetica", 9)
            c.drawString(left_x + 100, y_position, str(employee_data.get('EMP_ID', 'N/A')))
            
            c.setFont("Helvetica-Bold", 9)
            c.drawString(right_x, y_position, "Designation:")
            c.setFont("Helvetica", 9)
            c.drawString(right_x + 80, y_position, str(employee_data.get('Designation', 'N/A')))
            
            y_position -= 18
            c.setFont("Helvetica-Bold", 9)
            c.drawString(left_x, y_position, "EMP Name:")
            c.setFont("Helvetica", 9)
            c.drawString(left_x + 100, y_position, str(employee_data.get('Name', 'N/A')))
            
            c.setFont("Helvetica-Bold", 9)
            c.drawString(right_x, y_position, "Unit Name:")
            c.setFont("Helvetica", 9)
            c.drawString(right_x + 80, y_position, str(employee_data.get('Unit_Name', 'N/A')))
            
            y_position -= 18
            c.setFont("Helvetica-Bold", 9)
            c.drawString(left_x, y_position, "UAN No:")
            c.setFont("Helvetica", 9)
            c.drawString(left_x + 100, y_position, str(employee_data.get('UAN_No', 'N/A')))
            
            c.setFont("Helvetica-Bold", 9)
            c.drawString(right_x, y_position, "Bank A/c No:")
            c.setFont("Helvetica", 9)
            c.drawString(right_x + 80, y_position, str(employee_data.get('Bank_AC', 'N/A')))
            
            y_position -= 18
            c.setFont("Helvetica-Bold", 9)
            c.drawString(left_x, y_position, "ESI No:")
            c.setFont("Helvetica", 9)
            c.drawString(left_x + 100, y_position, str(employee_data.get('ESI_No', 'N/A')))
            
            c.setFont("Helvetica-Bold", 9)
            c.drawString(right_x, y_position, "DOJ:")
            c.setFont("Helvetica", 9)
            c.drawString(right_x + 80, y_position, str(employee_data.get('DOJ', 'N/A')))
            
            y_position -= 18
            c.setFont("Helvetica-Bold", 9)
            c.drawString(left_x, y_position, "No of working days:")
            c.setFont("Helvetica", 9)
            c.drawString(left_x + 120, y_position, str(employee_data.get('Basic_Days', 'N/A')))
            
            c.setFont("Helvetica-Bold", 9)
            c.drawString(right_x, y_position, "No of days worked:")
            c.setFont("Helvetica", 9)
            c.drawString(right_x + 110, y_position, str(employee_data.get('Actual_Days', 'N/A')))
            
            y_position -= 30
            
            # Earnings and Deductions Table
            earnings_data = [
                ['Earnings', '', '', 'Deductions', ''],
                ['Description', 'Fixed', 'Earned', 'Description', 'Amount'],
                ['Basic', f"{employee_data.get('Fixed_Basic', 0):.2f}", f"{employee_data.get('Earned_Basic', 0):.2f}", 
                 'Provident Fund', f"{employee_data.get('PF', 0):.2f}"],
                ['DA', f"{employee_data.get('Fixed_DA', 0) or 0:.2f}", f"{employee_data.get('Earned_DA', 0) or 0:.2f}", 
                 'ESI', f"{employee_data.get('ESI', 0):.2f}"],
                ['HRA', f"{employee_data.get('Fixed_HRA', 0):.2f}", f"{employee_data.get('Earned_HRA', 0):.2f}", 
                 'Professional Tax', f"{employee_data.get('PT', 0):.2f}"],
                ['Conveyance', '0.00', '0.00', 'ADV', '0.00'],
                ['Others', f"{employee_data.get('Other_Allowance', 0) or 0:.2f}", 
                 f"{employee_data.get('Other_Allowance', 0) or 0:.2f}", '', ''],
                ['Bonus', f"{employee_data.get('Fixed_Bonus', 0):.2f}", f"{employee_data.get('Earned_Bonus', 0):.2f}", '', ''],
                ['Gross Earning', f"{employee_data.get('Fixed_Total', 0):.2f}", f"{employee_data.get('Earned_Total', 0):.2f}", 
                 'Gross Deductions', f"{employee_data.get('Total_Deduction', 0):.2f}"],
            ]
            
            # Draw table manually for better control
            table_x = 50
            table_y = y_position
            col_widths = [100, 70, 70, 120, 80]
            row_height = 20
            
            c.setLineWidth(0.5)
            
            for row_idx, row in enumerate(earnings_data):
                current_y = table_y - (row_idx * row_height)
                
                # Draw row background for header
                if row_idx == 0:
                    c.setFillColorRGB(0.9, 0.9, 0.9)
                    c.rect(table_x, current_y - row_height, sum(col_widths[:3]), row_height, fill=1, stroke=0)
                    c.rect(table_x + sum(col_widths[:3]), current_y - row_height, sum(col_widths[3:]), row_height, fill=1, stroke=0)
                    c.setFillColorRGB(0, 0, 0)
                elif row_idx == 1:
                    c.setFillColorRGB(0.95, 0.95, 0.95)
                    c.rect(table_x, current_y - row_height, sum(col_widths), row_height, fill=1, stroke=0)
                    c.setFillColorRGB(0, 0, 0)
                
                # Draw cell borders
                x_pos = table_x
                for col_idx, (cell, width) in enumerate(zip(row, col_widths)):
                    c.rect(x_pos, current_y - row_height, width, row_height, stroke=1, fill=0)
                    
                    # Draw text
                    if row_idx in [0, 1, 8]:
                        c.setFont("Helvetica-Bold", 8)
                    else:
                        c.setFont("Helvetica", 8)
                    
                    # Center align for earnings/deductions header
                    if row_idx == 0:
                        if col_idx < 3:
                            c.drawCentredString(x_pos + (sum(col_widths[:3])/2), current_y - 14, "Earnings" if col_idx == 1 else "")
                        elif col_idx >= 3:
                            c.drawCentredString(x_pos + width/2, current_y - 14, "Deductions" if col_idx == 3 else "")
                    else:
                        # Right align numbers, left align text
                        if col_idx in [1, 2, 4] and row_idx > 0:
                            c.drawRightString(x_pos + width - 5, current_y - 14, str(cell))
                        else:
                            c.drawString(x_pos + 5, current_y - 14, str(cell))
                    
                    x_pos += width
            
            # Net Pay section
            y_position = table_y - (len(earnings_data) * row_height) - 20
            c.setFont("Helvetica-Bold", 10)
            c.drawString(left_x, y_position, "Net Pay:")
            c.setFont("Helvetica", 10)
            c.drawString(left_x + 70, y_position, f"₹ {employee_data.get('Net_Pay', 0):.2f}")
            
            y_position -= 20
            c.setFont("Helvetica-Bold", 9)
            c.drawString(left_x, y_position, "In Words:")
            c.setFont("Helvetica", 8)
            
            # Convert to words
            words = self.number_to_words(employee_data.get('Net_Pay', 0))
            c.drawString(left_x + 60, y_position, words)
            
            y_position -= 30
            c.setFont("Helvetica-Oblique", 7)
            c.drawCentredString(width/2, y_position, 
                              "**This is a system generated salary slip; hence signature is not required.")
            
            c.save()
            logger.info(f"Generated payslip PDF: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating PDF for {employee_data.get('Name', 'Unknown')}: {str(e)}")
            return False
    
    def send_email(self, to_email: str, employee_name: str, payslip_path: str, month: str) -> bool:
        """Send payslip via email"""
        try:
            email_config = self.config.get('email', {})
            
            if not email_config.get('enabled', False):
                logger.info("Email sending is disabled in config")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = to_email
            msg['Subject'] = f"Payslip for {month}"
            
            # Email body
            body = f"""Dear {employee_name},

Please find attached your payslip for {month}.

If you have any questions regarding your salary, please contact the HR department.

Best Regards,
HR Department
RS MAN-TECH

---
This is an automated email. Please do not reply to this message.
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach PDF
            with open(payslip_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(payslip_path)}')
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['sender_email'], email_config['password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_whatsapp(self, phone_number: str, employee_name: str, net_pay: float, month: str, 
                     payslip_path: Optional[str] = None) -> bool:
        """Send WhatsApp notification"""
        try:
            if not TWILIO_AVAILABLE:
                logger.warning("Twilio not available. WhatsApp feature disabled.")
                return False
            
            whatsapp_config = self.config.get('whatsapp', {})
            
            if not whatsapp_config.get('enabled', False):
                logger.info("WhatsApp sending is disabled in config")
                return False
            
            client = Client(whatsapp_config['account_sid'], whatsapp_config['auth_token'])
            
            # Format phone number (must include country code)
            if not phone_number.startswith('+'):
                phone_number = f"+91{phone_number}"  # Default to India
            
            # Message body
            message_body = f"""Hello {employee_name},

Your salary for {month} has been processed.

Net Salary: ₹{net_pay:,.2f}

Your payslip has been sent to your registered email address.

- RS MAN-TECH HR"""
            
            # Send message
            message = client.messages.create(
                from_=f"whatsapp:{whatsapp_config['from_number']}",
                body=message_body,
                to=f"whatsapp:{phone_number}"
            )
            
            logger.info(f"WhatsApp sent successfully to {phone_number} (SID: {message.sid})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp to {phone_number}: {str(e)}")
            return False
    
    def process_payslips(self, csv_file: str):
        """Main processing function"""
        logger.info("=" * 80)
        logger.info("Starting Payslip Generation Process")
        logger.info("=" * 80)
        
        try:
            # Load employee data
            df = self.load_employee_data(csv_file)
            total_employees = len(df)
            
            logger.info(f"Processing {total_employees} employee payslips...")
            
            # Process each employee
            for idx, row in df.iterrows():
                try:
                    employee_data = row.to_dict()
                    emp_id = employee_data.get('EMP_ID', f'EMP_{idx}')
                    name = employee_data.get('Name', 'Unknown')
                    month = employee_data.get('Month', datetime.now().strftime('%B-%Y'))
                    
                    logger.info(f"\nProcessing {idx + 1}/{total_employees}: {name} ({emp_id})")
                    
                    # Generate filename
                    month_clean = month.replace('Salary Slip for the Month of ', '').strip()
                    filename = f"{emp_id}_{month_clean.replace(' ', '_')}_Payslip.pdf"
                    output_path = self.output_dir / filename
                    
                    # Generate PDF
                    if self.generate_payslip_pdf(employee_data, str(output_path)):
                        self.success_count += 1
                        
                        # Send email
                        email = employee_data.get('Email')
                        if email and pd.notna(email):
                            if self.send_email(email, name, str(output_path), month_clean):
                                self.email_success += 1
                            else:
                                self.email_failed += 1
                        else:
                            logger.warning(f"No email address for {name}")
                        
                        # Send WhatsApp
                        phone = employee_data.get('Mobile')
                        net_pay = employee_data.get('Net_Pay', 0)
                        if phone and pd.notna(phone):
                            if self.send_whatsapp(str(phone), name, net_pay, month_clean, str(output_path)):
                                self.whatsapp_success += 1
                            else:
                                self.whatsapp_failed += 1
                        else:
                            logger.warning(f"No mobile number for {name}")
                    else:
                        self.error_count += 1
                        
                except Exception as e:
                    logger.error(f"Error processing employee {name}: {str(e)}")
                    self.error_count += 1
                    continue
            
            # Summary report
            self._print_summary(total_employees)
            
        except Exception as e:
            logger.error(f"Critical error in payslip processing: {str(e)}")
            raise
    
    def _print_summary(self, total_employees: int):
        """Print processing summary"""
        logger.info("\n" + "=" * 80)
        logger.info("PAYSLIP GENERATION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total Employees Processed: {total_employees}")
        logger.info(f"Payslips Generated Successfully: {self.success_count}")
        logger.info(f"Payslip Generation Errors: {self.error_count}")
        logger.info(f"\nEmail Delivery:")
        logger.info(f"  - Sent Successfully: {self.email_success}")
        logger.info(f"  - Failed: {self.email_failed}")
        logger.info(f"\nWhatsApp Delivery:")
        logger.info(f"  - Sent Successfully: {self.whatsapp_success}")
        logger.info(f"  - Failed: {self.whatsapp_failed}")
        logger.info("=" * 80)
        logger.info(f"Output Directory: {self.output_dir.absolute()}")
        logger.info(f"Log File: payslip_generator.log")
        logger.info("=" * 80)


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python payslip_generator.py <csv_file>")
        print("Example: python payslip_generator.py employee_data.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found")
        sys.exit(1)
    
    try:
        generator = PayslipGenerator('config.json')
        generator.process_payslips(csv_file)
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
