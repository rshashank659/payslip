# QUICK START GUIDE

## Setup in 5 Minutes

### 1. Install Python
Download from https://www.python.org/downloads/ (Python 3.8 or higher)

### 2. Install Dependencies
Open Terminal/Command Prompt in project folder:
```bash
pip install pandas reportlab twilio
```

### 3. Configure Email (Gmail)
Edit `config.json`:
```json
"email": {
  "enabled": true,
  "sender_email": "your-email@gmail.com",
  "password": "your-16-char-app-password"
}
```

**Get Gmail App Password:**
1. Enable 2FA: Google Account → Security → 2-Step Verification
2. Generate: Google Account → Security → App passwords
3. Copy the 16-character password to config.json

### 4. Prepare Your CSV
Use `sample_employee_data.csv` as template. Required columns:
- EMP_ID, Name, Email, Mobile
- Salary details (Basic, HRA, Deductions, etc.)

### 5. Run
```bash
python payslip_generator.py employee_data.csv
```

### 6. Check Output
- PDFs: `payslips/` folder
- Logs: `payslip_generator.log`

## Test First!
```bash
python payslip_generator.py sample_employee_data.csv
```

## Disable Features You Don't Need

**No WhatsApp?** Set in config.json:
```json
"whatsapp": {"enabled": false}
```

**No Email?** Set in config.json:
```json
"email": {"enabled": false}
```

## Common Issues

**"Module not found"**
```bash
pip install pandas reportlab
```

**"Email failed"**
- Check credentials in config.json
- Use app password (not regular password)
- Allow less secure apps (if needed)

**"Permission denied"**
- Run as administrator
- Check folder write permissions

## Need Help?
See full `README.md` for detailed documentation.

---
✅ **Checklist Before Running:**
- [ ] Python installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] config.json updated with email credentials
- [ ] CSV file prepared with employee data
- [ ] Tested with sample_employee_data.csv

**That's it! You're ready to generate payslips.**
