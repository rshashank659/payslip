# Payslip Generator - Setup and Usage Guide

## Overview
This Python application automatically generates employee payslips from CSV data and distributes them via Email and WhatsApp.

## Features
✅ Generate professional PDF payslips matching your format
✅ Automatic email distribution with PDF attachments
✅ WhatsApp notifications (optional)
✅ Batch processing from CSV files
✅ Comprehensive error handling and logging
✅ Detailed processing reports

## System Requirements

- Python 3.8 or higher
- Windows, macOS, or Linux
- Internet connection (for email and WhatsApp)

## Installation Steps

### Step 1: Install Python
Download and install Python from https://www.python.org/downloads/

**Important for Windows users:**
- During installation, check "Add Python to PATH"
- Verify installation: Open Command Prompt and type `python --version`

### Step 2: Download the Application Files
Extract all files to a folder, e.g., `C:\PayslipGenerator` or `~/PayslipGenerator`

Your folder should contain:
```
PayslipGenerator/
├── payslip_generator.py      # Main application
├── config.json                # Configuration file
├── sample_employee_data.csv   # Sample CSV template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Step 3: Install Required Python Packages

Open Terminal/Command Prompt in your project folder and run:

```bash
pip install -r requirements.txt
```

This installs:
- pandas (for CSV processing)
- reportlab (for PDF generation)
- twilio (for WhatsApp - optional)

**Alternative installation (if requirements.txt is not available):**
```bash
pip install pandas reportlab twilio
```

## Configuration

### Email Setup (Gmail)

1. **Enable 2-Factor Authentication** on your Gmail account
   - Go to Google Account → Security → 2-Step Verification

2. **Generate App Password**
   - Go to Google Account → Security → App passwords
   - Select "Mail" and your device
   - Copy the 16-character password

3. **Update config.json**
   ```json
   "email": {
     "enabled": true,
     "smtp_server": "smtp.gmail.com",
     "smtp_port": 587,
     "sender_email": "your-email@gmail.com",
     "password": "your-16-char-app-password",
     "use_tls": true
   }
   ```

### Email Setup (Outlook/Office 365)

```json
"email": {
  "enabled": true,
  "smtp_server": "smtp.office365.com",
  "smtp_port": 587,
  "sender_email": "your-email@outlook.com",
  "password": "your-password",
  "use_tls": true
}
```

### WhatsApp Setup (Optional - Using Twilio)

1. **Sign up for Twilio**
   - Go to https://www.twilio.com/
   - Create a free trial account
   - Get $15 free credit

2. **Get WhatsApp Sandbox Access**
   - Go to Twilio Console → Messaging → Try it out → Send a WhatsApp message
   - Follow instructions to connect your WhatsApp

3. **Get Credentials**
   - Account SID: Found in Twilio Console Dashboard
   - Auth Token: Found in Twilio Console Dashboard
   - WhatsApp Number: Found in WhatsApp Sandbox settings

4. **Update config.json**
   ```json
   "whatsapp": {
     "enabled": true,
     "account_sid": "AC********************************",
     "auth_token": "********************************",
     "from_number": "+14155238886"
   }
   ```

**Note:** Twilio trial accounts can only send to verified numbers. For production, you'll need a paid Twilio account or WhatsApp Business API.

### Disable Email or WhatsApp

If you don't want to use email or WhatsApp, set `"enabled": false` in config.json:

```json
"email": {
  "enabled": false,
  ...
}
```

## Preparing Employee Data CSV

### Required Columns

Your CSV file must contain these columns:

| Column Name | Description | Example |
|------------|-------------|---------|
| EMP_ID | Employee ID | RSIDH0002 |
| Name | Full Name | ASHIK |
| Email | Email address | ashik@example.com |
| Mobile | Phone number (with country code) | 9876543210 |
| Designation | Job title | Picker |
| Unit_Name | Department/Unit | Idemtisu |
| UAN_No | UAN Number | 101639324844 |
| ESI_No | ESI Number | 5221374446 |
| DOJ | Date of Joining | 26.08.2024 |
| Bank_AC | Bank Account Number | 923010044047831 |
| IFSC_Code | IFSC Code | UTIB0002592 |
| Month | Salary Month | December-2025 |
| Basic_Days | Working days in month | 31 |
| Actual_Days | Days worked | 18 |
| Fixed_Basic | Fixed Basic Salary | 12847 |
| Fixed_DA | Fixed DA | 0 |
| Fixed_HRA | Fixed HRA | 3693 |
| Fixed_Bonus | Fixed Bonus | 1070 |
| Fixed_Total | Fixed Total | 17610 |
| Earned_Basic | Earned Basic | 7460 |
| Earned_DA | Earned DA | 0 |
| Earned_HRA | Earned HRA | 2144 |
| Other_Allowance | Other Allowances | 0 |
| Earned_Bonus | Earned Bonus | 621 |
| Earned_Total | Earned Total | 10225 |
| PF | Provident Fund | 895 |
| ESI | ESI Deduction | 77 |
| PT | Professional Tax | 0 |
| LWF | Labour Welfare Fund | 2 |
| Total_Deduction | Total Deductions | 974 |
| Net_Pay | Net Salary | 9251 |

### Creating Your CSV File

**Option 1: Use Excel**
1. Open `sample_employee_data.csv` in Excel
2. Add your employee data
3. Save as CSV (CSV UTF-8 recommended)

**Option 2: Export from your Payroll System**
- Most payroll systems can export to CSV
- Ensure column names match exactly as listed above
- Remove any extra columns not needed

## Running the Application

### Basic Usage

```bash
python payslip_generator.py employee_data.csv
```

### Step-by-Step Process

1. **Open Terminal/Command Prompt**
   - Windows: Press Win+R, type `cmd`, press Enter
   - Mac: Press Cmd+Space, type `terminal`, press Enter
   - Linux: Press Ctrl+Alt+T

2. **Navigate to project folder**
   ```bash
   cd C:\PayslipGenerator
   # or
   cd ~/PayslipGenerator
   ```

3. **Run the application**
   ```bash
   python payslip_generator.py employee_data.csv
   ```

4. **Monitor progress**
   - The application will show real-time progress
   - Check the log file for detailed information

### Example Output

```
================================================================================
Starting Payslip Generation Process
================================================================================
Loaded 15 employee records from employee_data.csv
Processing 15 employee payslips...

Processing 1/15: ASHIK (RSIDH0002)
Generated payslip PDF: payslips/RSIDH0002_December-2025_Payslip.pdf
Email sent successfully to ashik@example.com
WhatsApp sent successfully to +919876543210

Processing 2/15: RAJESH PATEL (RSIDH0003)
...

================================================================================
PAYSLIP GENERATION SUMMARY
================================================================================
Total Employees Processed: 15
Payslips Generated Successfully: 15
Payslip Generation Errors: 0

Email Delivery:
  - Sent Successfully: 15
  - Failed: 0

WhatsApp Delivery:
  - Sent Successfully: 15
  - Failed: 0
================================================================================
```

## Output Files

### Generated Payslips
Location: `payslips/` folder

Naming format: `{EMP_ID}_{Month}_{Year}_Payslip.pdf`

Example: `RSIDH0002_December-2025_Payslip.pdf`

### Log File
Location: `payslip_generator.log`

Contains:
- Processing timestamps
- Success/failure messages
- Error details
- Complete audit trail

## Troubleshooting

### Common Issues

**1. "Module not found" error**
```
Solution: Install required packages
pip install pandas reportlab twilio
```

**2. Email not sending**
```
Possible causes:
- Incorrect email/password in config.json
- App password not generated (Gmail)
- Firewall blocking port 587
- "Less secure app access" disabled (for older Gmail accounts)

Solution:
- Verify credentials in config.json
- Generate app password for Gmail
- Check firewall settings
```

**3. PDF not generating**
```
Possible causes:
- Missing data in CSV
- Invalid number format

Solution:
- Check CSV file has all required columns
- Ensure numeric columns contain valid numbers
- Review log file for specific errors
```

**4. WhatsApp not sending**
```
Possible causes:
- Twilio not installed (pip install twilio)
- Invalid credentials
- Phone number not verified (trial account)

Solution:
- Install Twilio: pip install twilio
- Verify credentials in config.json
- Add recipient numbers to Twilio verified numbers
```

**5. "Permission denied" error**
```
Solution:
- Run Command Prompt/Terminal as Administrator
- Check folder permissions
- Ensure output directory is writable
```

## Testing

### Test with Sample Data

```bash
python payslip_generator.py sample_employee_data.csv
```

This will process 3 sample employees and help you verify:
- PDF generation works correctly
- Email sending is configured properly
- WhatsApp integration functions (if enabled)

### Test Email Only

1. Set `"enabled": false` for WhatsApp in config.json
2. Run with sample data
3. Check your email inbox

### Test PDF Generation Only

1. Set `"enabled": false` for both email and WhatsApp
2. Run the application
3. Check `payslips/` folder for generated PDFs

## Best Practices

### Data Security
- Keep config.json secure (contains passwords)
- Don't share config.json or commit to version control
- Use app passwords instead of main account passwords
- Regularly rotate passwords

### CSV File Management
- Always keep a backup of your CSV file
- Validate data before processing
- Use consistent date formats
- Remove special characters from names if causing issues

### Batch Processing
- Process in smaller batches if dealing with large employee counts
- Review log files after each batch
- Keep failed records for retry

### Email Limits
- Gmail: ~500 emails/day for free accounts
- Outlook: ~300 emails/day for free accounts
- For large organizations, consider paid SMTP services

## Advanced Configuration

### Custom SMTP Server

```json
"email": {
  "enabled": true,
  "smtp_server": "smtp.yourcompany.com",
  "smtp_port": 587,
  "sender_email": "payroll@yourcompany.com",
  "password": "your-password",
  "use_tls": true
}
```

### Custom Output Directory

```json
{
  "output_directory": "C:/Payslips/December2025"
}
```

### Logging Level

Modify in `payslip_generator.py`:
```python
logging.basicConfig(level=logging.DEBUG)  # For more detailed logs
logging.basicConfig(level=logging.WARNING)  # For fewer logs
```

## Automation

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., monthly on 1st)
4. Action: Start a program
   - Program: `python`
   - Arguments: `C:\PayslipGenerator\payslip_generator.py employee_data.csv`
   - Start in: `C:\PayslipGenerator`

### Linux/Mac Cron

```bash
# Edit crontab
crontab -e

# Add line (runs on 1st of every month at 9 AM)
0 9 1 * * cd /home/user/PayslipGenerator && python3 payslip_generator.py employee_data.csv
```

## Support and Customization

### Customizing Payslip Format

The PDF layout can be customized by modifying the `generate_payslip_pdf()` function in `payslip_generator.py`.

Key areas to modify:
- Company logo (add image)
- Font sizes and styles
- Table layouts
- Colors and formatting

### Adding New Features

Common customizations:
- Add company logo
- Include digital signature
- Add QR code for verification
- Generate Excel format payslips
- Send SMS notifications
- Upload to cloud storage (Google Drive, Dropbox)

### Getting Help

If you encounter issues:
1. Check the log file (`payslip_generator.log`)
2. Verify CSV format matches requirements
3. Test with sample data first
4. Review error messages carefully

## License

This software is provided as-is for payroll processing purposes.

## Contact

For support or custom development:
- Review documentation carefully
- Check log files for error details
- Ensure all configuration is correct

---

**Version:** 1.0  
**Last Updated:** February 2025  
**Python Version:** 3.8+
