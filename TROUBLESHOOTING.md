# Troubleshooting Guide

## Quick Diagnostics

### Run System Validation
```bash
python validate_setup.py
```
This will check:
- Python version
- Required packages
- Configuration file
- Sample data
- Output directory

## Common Errors and Solutions

### 1. Installation Errors

#### Error: "python is not recognized"
**Cause:** Python not installed or not in system PATH

**Solution (Windows):**
1. Reinstall Python from python.org
2. During installation, check "Add Python to PATH"
3. Restart Command Prompt
4. Test: `python --version`

**Solution (Mac/Linux):**
```bash
# Check if python3 is available
python3 --version

# Use python3 instead of python
python3 payslip_generator.py employee_data.csv
```

#### Error: "No module named 'pandas'"
**Cause:** Required packages not installed

**Solution:**
```bash
pip install pandas reportlab twilio openpyxl
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

**If pip is not found:**
```bash
python -m pip install pandas reportlab
```

#### Error: "Could not install packages due to an EnvironmentError: [Errno 13]"
**Cause:** Permission denied

**Solution (Windows):**
```bash
# Run Command Prompt as Administrator
pip install pandas reportlab
```

**Solution (Mac/Linux):**
```bash
# Use --user flag
pip install --user pandas reportlab

# Or use sudo (not recommended)
sudo pip install pandas reportlab
```

### 2. Configuration Errors

#### Error: "Configuration file config.json not found"
**Cause:** config.json missing or in wrong directory

**Solution:**
1. Ensure config.json is in the same folder as payslip_generator.py
2. Check file name is exactly "config.json" (case-sensitive)
3. Verify you're running the script from the correct directory

#### Error: "Invalid JSON in configuration file"
**Cause:** JSON syntax error in config.json

**Solution:**
1. Use a JSON validator (jsonlint.com)
2. Check for:
   - Missing commas
   - Extra commas
   - Unmatched brackets
   - Missing quotes
   - Smart quotes instead of straight quotes

**Common JSON mistakes:**
```json
❌ Wrong:
{
  "email": {
    "enabled": true    # Missing comma
    "sender_email": "test@gmail.com"
  }
}

✅ Correct:
{
  "email": {
    "enabled": true,
    "sender_email": "test@gmail.com"
  }
}
```

### 3. Email Errors

#### Error: "SMTPAuthenticationError: Username and Password not accepted"
**Cause:** Incorrect credentials or app password not used

**Solution for Gmail:**
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Go to https://myaccount.google.com/security
   - Click "App passwords"
   - Generate new password
   - Copy 16-character password (no spaces)
3. Update config.json with app password
4. DO NOT use your regular Gmail password

**Solution for Outlook:**
1. Ensure account allows SMTP access
2. Use full email and password in config.json
3. Try smtp-mail.outlook.com if smtp.office365.com doesn't work

#### Error: "SMTPServerDisconnected: Connection unexpectedly closed"
**Cause:** Firewall blocking port or wrong SMTP server

**Solution:**
1. Check firewall settings
2. Allow outbound connections on port 587
3. Try port 465 with SSL:
```json
"email": {
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 465,
  "use_ssl": true
}
```

#### Error: "Email sent successfully but not received"
**Cause:** Email in spam or wrong recipient

**Solution:**
1. Check spam/junk folder
2. Verify email address in CSV is correct
3. Check sender reputation
4. Try sending to a different email first

#### Error: "Failed to send email: [SSL: CERTIFICATE_VERIFY_FAILED]"
**Cause:** SSL certificate verification issue

**Solution:**
```python
# Quick fix (not recommended for production)
# In payslip_generator.py, modify send_email function:
server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
server.starttls()
# Add this line:
# context = ssl.create_default_context()
# context.check_hostname = False
# context.verify_mode = ssl.CERT_NONE
```

### 4. CSV Data Errors

#### Error: "Missing required columns"
**Cause:** CSV doesn't have required column names

**Solution:**
1. Open CSV in Excel
2. Check first row has exact column names
3. Compare with sample_employee_data.csv
4. Column names are case-sensitive:
   - ✅ `EMP_ID`
   - ❌ `emp_id` or `Emp_Id`

#### Error: "could not convert string to float"
**Cause:** Non-numeric data in number columns

**Solution:**
1. Check these columns contain only numbers:
   - Basic_Days, Actual_Days
   - All Fixed_* and Earned_* columns
   - All deduction columns
   - Net_Pay
2. Remove any:
   - Currency symbols (₹, $)
   - Commas (1,234 → 1234)
   - Text or special characters
3. Use 0 for empty values, not blank cells

#### Error: "UnicodeDecodeError"
**Cause:** CSV encoding issue

**Solution:**
Save CSV as "UTF-8" encoding:
1. In Excel: File → Save As → CSV UTF-8 (Comma delimited)
2. In Notepad: File → Save As → Encoding: UTF-8
3. Or use this in code:
```python
df = pd.read_csv(csv_file, encoding='utf-8-sig')
```

### 5. PDF Generation Errors

#### Error: "Permission denied" when saving PDF
**Cause:** Output directory not writable or file in use

**Solution:**
1. Close any open PDF files
2. Check folder permissions
3. Run as administrator (Windows)
4. Change output directory in config.json

#### Error: "Failed to generate PDF: invalid literal for int()"
**Cause:** Invalid number in employee data

**Solution:**
1. Check all numeric columns in CSV
2. Ensure no blank cells in required number fields
3. Replace blanks with 0
4. Check for hidden characters

#### Error: PDF generated but text is garbled
**Cause:** Font or encoding issue

**Solution:**
Modify in payslip_generator.py:
```python
# Register fonts with proper encoding
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Use specific fonts if needed
```

### 6. WhatsApp Errors

#### Error: "No module named 'twilio'"
**Cause:** Twilio package not installed

**Solution:**
```bash
pip install twilio
```

Or disable WhatsApp in config.json:
```json
"whatsapp": {
  "enabled": false
}
```

#### Error: "Unable to create record: Invalid parameter"
**Cause:** Phone number format incorrect or not verified

**Solution:**
1. For Twilio trial: Verify recipient numbers in Twilio console
2. Ensure phone format: +919876543210 (country code + number)
3. Check Twilio sandbox is active
4. Verify 'from' number in config is correct

#### Error: "Authenticate: Unable to authenticate"
**Cause:** Wrong Twilio credentials

**Solution:**
1. Go to Twilio Console (twilio.com/console)
2. Copy Account SID and Auth Token
3. Update config.json with exact values
4. No extra spaces or quotes

### 7. File and Path Errors

#### Error: "FileNotFoundError: employee_data.csv"
**Cause:** CSV file not in correct location

**Solution:**
1. Put CSV file in same folder as payslip_generator.py
2. Or provide full path:
```bash
python payslip_generator.py C:/Users/YourName/Documents/employee_data.csv
```

#### Error: "PermissionError: [Errno 13]"
**Cause:** File is open or locked

**Solution:**
1. Close Excel/CSV file
2. Close any PDF viewers
3. Run as administrator
4. Check antivirus isn't blocking

### 8. Runtime Errors

#### Error: Program runs but no output
**Cause:** Email/WhatsApp disabled or failed silently

**Solution:**
1. Check log file: `payslip_generator.log`
2. Look in `payslips/` folder
3. Enable debug logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

#### Error: "KeyError: 'Name'"
**Cause:** Column name mismatch in CSV

**Solution:**
1. Check CSV column headers exactly match required names
2. No extra spaces in headers
3. Case-sensitive matching

#### Error: Out of memory
**Cause:** Processing too many records at once

**Solution:**
1. Process in smaller batches
2. Split CSV into multiple files
3. Increase system memory
4. Close other applications

## Performance Issues

### Slow Processing
**Causes and Solutions:**

1. **Large CSV file:**
   - Process in batches of 50-100 employees
   - Remove unnecessary columns from CSV

2. **Slow email sending:**
   - Normal: ~1-2 seconds per email
   - Check internet connection
   - Reduce attachment size

3. **Network timeouts:**
   - Increase timeout in code
   - Check firewall settings
   - Verify SMTP server is accessible

### High Memory Usage
**Solutions:**
1. Process smaller batches
2. Clear output directory of old PDFs
3. Restart Python between large batches

## Debugging Tips

### Enable Detailed Logging
In `payslip_generator.py`, change:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components

**Test PDF Only:**
```json
// In config.json
"email": {"enabled": false},
"whatsapp": {"enabled": false}
```

**Test Email Only:**
```json
"whatsapp": {"enabled": false}
```

**Test with One Employee:**
Create CSV with just one employee record

### Check Log Files
```bash
# View recent logs
tail -f payslip_generator.log  # Linux/Mac

# On Windows, open in Notepad
notepad payslip_generator.log
```

### Verify Output
```bash
# Check if PDFs were created
ls payslips/  # Linux/Mac
dir payslips  # Windows
```

## Getting More Help

### Information to Provide
When seeking help, include:
1. Error message (full text)
2. Log file contents
3. Python version: `python --version`
4. Operating system
5. Steps you've already tried

### Useful Commands for Diagnostics
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check package version
pip show pandas

# Test Python imports
python -c "import pandas; print(pandas.__version__)"

# Validate JSON
python -m json.tool config.json
```

## Still Having Issues?

1. **Re-run validation:**
   ```bash
   python validate_setup.py
   ```

2. **Test with sample data:**
   ```bash
   python payslip_generator.py sample_employee_data.csv
   ```

3. **Check the log file:**
   - All operations are logged
   - Error messages show exact problem
   - Look for stack traces

4. **Start fresh:**
   - Reinstall Python packages
   - Use default config.json
   - Test with sample_employee_data.csv

5. **Verify prerequisites:**
   - Python 3.8+
   - All packages installed
   - Valid email credentials
   - Correct CSV format

---

**Remember:** Most issues are related to:
- Configuration (70%)
- CSV format (20%)
- Missing dependencies (10%)

Always start with validation and sample data testing!
