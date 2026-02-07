# Complete Setup Guide - Payslip Generator

## 📦 What You've Received

Your Payslip Generator package includes:

### Core Application Files
- **payslip_generator.py** - Main application (23 KB)
- **config.json** - Configuration file for email and WhatsApp
- **requirements.txt** - Python package dependencies
- **sample_employee_data.csv** - Sample CSV template with 3 employees

### Execution Scripts
- **run_payslip.bat** - Windows launcher script
- **run_payslip.sh** - Linux/Mac launcher script (chmod +x applied)
- **validate_setup.py** - System validation tool

### Documentation (75 KB total)
- **README.md** - Complete user manual (12 KB)
- **QUICKSTART.md** - 5-minute setup guide (2 KB)
- **TROUBLESHOOTING.md** - Problem-solving guide (11 KB)
- **CSV_TEMPLATE_GUIDE.md** - CSV format reference (5 KB)
- **ADVANCED_FEATURES.md** - Customization guide (16 KB)

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Verify Python Installation
```bash
python --version
# Should show Python 3.8 or higher
```

**Don't have Python?** Download from https://www.python.org/downloads/

### Step 2: Install Dependencies
```bash
# Navigate to the project folder
cd /path/to/PayslipGenerator

# Install required packages
pip install pandas reportlab twilio
```

### Step 3: Configure Email
Edit `config.json` and update:
```json
{
  "email": {
    "enabled": true,
    "sender_email": "your-email@gmail.com",
    "password": "your-app-password"
  }
}
```

**Gmail users:** Generate app password from Google Account → Security → App passwords

### Step 4: Test Run
```bash
python payslip_generator.py sample_employee_data.csv
```

### Step 5: Check Output
- PDFs will be in `payslips/` folder
- Logs in `payslip_generator.log`

---

## 📋 Complete Installation Steps

### For Windows Users

1. **Install Python**
   - Download from https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation
   - Verify: Open Command Prompt → Type `python --version`

2. **Extract Files**
   - Extract all files to a folder (e.g., `C:\PayslipGenerator`)
   - Ensure all 12 files are present

3. **Install Packages**
   ```cmd
   cd C:\PayslipGenerator
   pip install pandas reportlab twilio
   ```

4. **Configure Settings**
   - Open `config.json` in Notepad
   - Update email credentials
   - Save and close

5. **Validate Setup**
   ```cmd
   python validate_setup.py
   ```

6. **Run Application**
   ```cmd
   # Method 1: Using batch file
   run_payslip.bat sample_employee_data.csv

   # Method 2: Direct command
   python payslip_generator.py sample_employee_data.csv
   ```

### For Mac/Linux Users

1. **Install Python** (if not already installed)
   ```bash
   # Mac (using Homebrew)
   brew install python3

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3 python3-pip

   # Fedora/RHEL
   sudo dnf install python3 python3-pip
   ```

2. **Extract Files**
   ```bash
   cd ~/Downloads
   # Extract to desired location
   cp -r PayslipGenerator ~/
   cd ~/PayslipGenerator
   ```

3. **Install Packages**
   ```bash
   pip3 install pandas reportlab twilio
   # or
   pip3 install -r requirements.txt
   ```

4. **Make Script Executable**
   ```bash
   chmod +x run_payslip.sh
   ```

5. **Configure Settings**
   ```bash
   nano config.json
   # or
   vim config.json
   ```

6. **Validate Setup**
   ```bash
   python3 validate_setup.py
   ```

7. **Run Application**
   ```bash
   # Method 1: Using shell script
   ./run_payslip.sh sample_employee_data.csv

   # Method 2: Direct command
   python3 payslip_generator.py sample_employee_data.csv
   ```

---

## ⚙️ Configuration Details

### Email Configuration

#### Gmail Setup
1. Enable 2-Factor Authentication
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. Generate App Password
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy 16-character password

3. Update config.json
   ```json
   "email": {
     "enabled": true,
     "smtp_server": "smtp.gmail.com",
     "smtp_port": 587,
     "sender_email": "youremail@gmail.com",
     "password": "abcd efgh ijkl mnop"
   }
   ```

#### Outlook/Office 365 Setup
```json
"email": {
  "enabled": true,
  "smtp_server": "smtp.office365.com",
  "smtp_port": 587,
  "sender_email": "youremail@outlook.com",
  "password": "your-password"
}
```

### WhatsApp Configuration (Optional)

1. **Sign up for Twilio**
   - Visit https://www.twilio.com/try-twilio
   - Get free $15 credit

2. **Get WhatsApp Sandbox**
   - Twilio Console → Messaging → Try it out → WhatsApp
   - Connect your WhatsApp number

3. **Get Credentials**
   - Account SID: From Twilio Console Dashboard
   - Auth Token: From Twilio Console Dashboard

4. **Update config.json**
   ```json
   "whatsapp": {
     "enabled": true,
     "account_sid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
     "auth_token": "your-auth-token",
     "from_number": "+14155238886"
   }
   ```

**Note:** For trial accounts, verify recipient numbers in Twilio Console

---

## 📄 Preparing Your Employee Data

### Required CSV Columns
Your CSV must have these columns (case-sensitive):

```
EMP_ID, Name, Designation, Unit_Name, UAN_No, ESI_No, DOJ, Bank_AC, 
IFSC_Code, Month, Basic_Days, Actual_Days, Fixed_Basic, Fixed_DA, 
Fixed_HRA, Fixed_Bonus, Fixed_Total, Earned_Basic, Earned_DA, 
Earned_HRA, Other_Allowance, Earned_Bonus, Earned_Total, PF, ESI, 
PT, LWF, Total_Deduction, Net_Pay, Email, Mobile
```

### Creating CSV from Excel
1. Open `sample_employee_data.csv` in Excel as reference
2. Enter your employee data
3. File → Save As → Choose "CSV UTF-8"
4. Save with a descriptive name (e.g., `january_2025_payroll.csv`)

### Data Validation Checklist
- [ ] All required columns present
- [ ] Column names match exactly (case-sensitive)
- [ ] Email addresses are valid
- [ ] Phone numbers are 10 digits
- [ ] No currency symbols in numbers
- [ ] No commas in numbers (use 12345 not 12,345)
- [ ] All calculations are correct:
  - Fixed_Total = sum of all fixed components
  - Earned_Total = sum of all earned components
  - Total_Deduction = PF + ESI + PT + LWF
  - Net_Pay = Earned_Total - Total_Deduction

---

## 🔍 Validation and Testing

### Run System Validation
```bash
python validate_setup.py
```

This checks:
- ✅ Python version (3.8+)
- ✅ Required packages installed
- ✅ Configuration file valid
- ✅ Sample data available
- ✅ Output directory ready

### Test with Sample Data
```bash
python payslip_generator.py sample_employee_data.csv
```

Expected output:
- 3 PDF files in `payslips/` folder
- 3 emails sent (if configured)
- 3 WhatsApp messages (if configured)
- Processing log in `payslip_generator.log`

### Verify Generated PDFs
Check that PDFs contain:
- ✅ Company header
- ✅ Employee details
- ✅ Earnings breakdown
- ✅ Deductions breakdown
- ✅ Net pay in numbers and words
- ✅ Proper formatting

---

## 📊 Usage Examples

### Basic Usage
```bash
python payslip_generator.py employee_data.csv
```

### Using Windows Batch File
```cmd
run_payslip.bat employee_data.csv
```

### Using Linux/Mac Shell Script
```bash
./run_payslip.sh employee_data.csv
```

### Process Multiple Files
```bash
# Process January payroll
python payslip_generator.py january_2025.csv

# Process February payroll
python payslip_generator.py february_2025.csv
```

---

## 📁 Project Structure

```
PayslipGenerator/
├── payslip_generator.py          # Main application
├── config.json                    # Configuration
├── requirements.txt               # Dependencies
├── sample_employee_data.csv       # Sample data
├── validate_setup.py              # Validation tool
├── run_payslip.bat               # Windows launcher
├── run_payslip.sh                # Linux/Mac launcher
├── README.md                     # Full documentation
├── QUICKSTART.md                 # Quick setup guide
├── TROUBLESHOOTING.md            # Problem solving
├── CSV_TEMPLATE_GUIDE.md         # CSV format help
├── ADVANCED_FEATURES.md          # Customization guide
├── payslips/                     # Output folder (created automatically)
│   ├── EMP001_December-2025_Payslip.pdf
│   ├── EMP002_December-2025_Payslip.pdf
│   └── ...
└── payslip_generator.log         # Processing log
```

---

## 🎯 Expected Results

### After Successful Run

**Console Output:**
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

**Generated Files:**
- PDF payslips in `payslips/` folder
- One PDF per employee
- Naming: `{EMP_ID}_{Month}_Payslip.pdf`

**Emails Sent:**
- Subject: "Payslip for {Month}"
- Body: Professional salary notification
- Attachment: PDF payslip

**WhatsApp Messages:**
- Greeting with employee name
- Salary month and net pay amount
- Reference to email for PDF

---

## 🛠️ Common Issues and Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| "Module not found" | `pip install pandas reportlab` |
| "Python not recognized" | Add Python to PATH, restart terminal |
| Email authentication failed | Use app password, not regular password |
| CSV errors | Check column names match exactly |
| Permission denied | Run as administrator / use sudo |
| No PDFs generated | Check `payslip_generator.log` for errors |

**For detailed troubleshooting:** See `TROUBLESHOOTING.md`

---

## 📈 Production Deployment

### Email Sending Limits
- **Gmail Free:** ~500 emails/day
- **Outlook Free:** ~300 emails/day
- **Business accounts:** Higher limits

### Recommendations for Large Scale
1. **Use dedicated SMTP service** (SendGrid, AWS SES)
2. **Process in batches** (50-100 employees at a time)
3. **Schedule during off-peak hours**
4. **Monitor logs regularly**
5. **Keep backups of CSV files**

### Automation
Set up monthly automation:
- **Windows:** Task Scheduler
- **Linux/Mac:** Cron jobs
- See `ADVANCED_FEATURES.md` for details

---

## 📞 Getting Help

### Self-Service Resources
1. Check `TROUBLESHOOTING.md` for common issues
2. Review `payslip_generator.log` for errors
3. Run `python validate_setup.py` to check system
4. Test with `sample_employee_data.csv` first

### Documentation Files
- **README.md** - Complete manual
- **QUICKSTART.md** - Fast setup
- **TROUBLESHOOTING.md** - Problem solving
- **CSV_TEMPLATE_GUIDE.md** - CSV help
- **ADVANCED_FEATURES.md** - Customization

---

## ✅ Final Checklist

Before first production run:
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] config.json updated with credentials
- [ ] Email tested with sample data
- [ ] WhatsApp tested (if using)
- [ ] CSV file prepared and validated
- [ ] Backup of original CSV created
- [ ] validate_setup.py run successfully
- [ ] Test run completed with sample_employee_data.csv

---

## 🎉 You're Ready!

Everything is set up and ready to use. To generate payslips:

```bash
python payslip_generator.py your_employee_data.csv
```

Check the `payslips/` folder for your generated PDF payslips!

For questions or issues, refer to the documentation files included in this package.

---

**Version:** 1.0  
**Last Updated:** February 2025  
**System Requirements:** Python 3.8+, Internet connection  
**Package Size:** ~78 KB total
