# CSV Template Guide for Payslip Generator

## Column Descriptions

| Column Name | Data Type | Required | Description | Example |
|------------|-----------|----------|-------------|---------|
| EMP_ID | Text | Yes | Unique employee identifier | RSIDH0002 |
| Name | Text | Yes | Employee full name | ASHIK |
| Designation | Text | Yes | Job title/position | Picker |
| Unit_Name | Text | Yes | Department or unit | Idemtisu |
| UAN_No | Text | Yes | Universal Account Number | 101639324844 |
| ESI_No | Text | Yes | ESI Number (use "NON ESIC" if not applicable) | 5221374446 |
| DOJ | Text | Yes | Date of joining | 26.08.2024 |
| Bank_AC | Text | Yes | Bank account number | 923010044047831 |
| IFSC_Code | Text | Yes | Bank IFSC code | UTIB0002592 |
| Month | Text | Yes | Salary month | December-2025 |
| Basic_Days | Number | Yes | Working days in month | 31 |
| Actual_Days | Number | Yes | Days actually worked | 18 |
| Fixed_Basic | Number | Yes | Fixed basic salary | 12847 |
| Fixed_DA | Number | No | Fixed dearness allowance (use 0 if none) | 0 |
| Fixed_HRA | Number | Yes | Fixed house rent allowance | 3693 |
| Fixed_Bonus | Number | Yes | Fixed bonus | 1070 |
| Fixed_Total | Number | Yes | Total fixed salary | 17610 |
| Earned_Basic | Number | Yes | Earned basic salary | 7460 |
| Earned_DA | Number | No | Earned dearness allowance | 0 |
| Earned_HRA | Number | Yes | Earned house rent allowance | 2144 |
| Other_Allowance | Number | No | Other allowances | 0 |
| Earned_Bonus | Number | Yes | Earned bonus | 621 |
| Earned_Total | Number | Yes | Total earned salary | 10225 |
| PF | Number | Yes | Provident fund deduction | 895 |
| ESI | Number | Yes | ESI deduction | 77 |
| PT | Number | Yes | Professional tax | 0 |
| LWF | Number | Yes | Labour welfare fund | 2 |
| Total_Deduction | Number | Yes | Total deductions | 974 |
| Net_Pay | Number | Yes | Net salary (take-home) | 9251 |
| Email | Text | Yes | Employee email address | ashik@example.com |
| Mobile | Text | Yes | Mobile number (10 digits) | 9876543210 |

## Important Notes

### 1. Number Formatting
- Use plain numbers without currency symbols
- Use decimal point for decimals (e.g., 1234.56)
- Do not use commas in numbers (e.g., use 12345 not 12,345)

### 2. Text Fields
- Keep names and designations consistent
- Avoid special characters that might cause issues
- Use consistent date format (DD.MM.YYYY)

### 3. Email Addresses
- Must be valid email addresses
- One email per employee
- Check for typos before processing

### 4. Phone Numbers
- Use 10-digit format for Indian numbers
- Will be auto-prefixed with +91 for WhatsApp
- For international numbers, include country code

### 5. Optional Fields
These can be left as 0 or empty:
- Fixed_DA
- Earned_DA
- Other_Allowance
- PT (if not applicable)

### 6. Calculated Fields
Ensure these calculations are correct:
- Fixed_Total = Fixed_Basic + Fixed_DA + Fixed_HRA + Fixed_Bonus
- Earned_Total = Earned_Basic + Earned_DA + Earned_HRA + Other_Allowance + Earned_Bonus
- Total_Deduction = PF + ESI + PT + LWF
- Net_Pay = Earned_Total - Total_Deduction

## Example Rows

```csv
EMP_ID,Name,Designation,Unit_Name,UAN_No,ESI_No,DOJ,Bank_AC,IFSC_Code,Month,Basic_Days,Actual_Days,Fixed_Basic,Fixed_DA,Fixed_HRA,Fixed_Bonus,Fixed_Total,Earned_Basic,Earned_DA,Earned_HRA,Other_Allowance,Earned_Bonus,Earned_Total,PF,ESI,PT,LWF,Total_Deduction,Net_Pay,Email,Mobile
RSIDH0002,ASHIK,Picker,Idemtisu,101639324844,5221374446,26.08.2024,923010044047831,UTIB0002592,December-2025,31,18,12847,0,3693,1070,17610,7460,0,2144,0,621,10225,895,77,0,2,974,9251,ashik@example.com,9876543210
```

## Common Mistakes to Avoid

❌ **Don't:**
- Include currency symbols (₹, $)
- Use commas in numbers (1,234)
- Mix different date formats
- Leave required fields empty
- Use special characters in emails

✅ **Do:**
- Use plain numbers (1234)
- Keep date format consistent
- Verify email addresses
- Check calculations
- Test with sample data first

## Exporting from Excel

If you're creating the CSV from Excel:

1. Enter all data in Excel
2. Go to File → Save As
3. Choose "CSV (Comma delimited) (*.csv)" or "CSV UTF-8"
4. Click Save
5. If warned about features, click "Yes" to keep CSV format

## Validation Checklist

Before running the generator, verify:
- [ ] All required columns are present
- [ ] Column names match exactly (case-sensitive)
- [ ] Email addresses are valid
- [ ] Phone numbers are 10 digits
- [ ] Numbers don't have commas or currency symbols
- [ ] Net_Pay calculations are correct
- [ ] File is saved as CSV (not Excel)

## Need Help?

If you encounter CSV-related errors:
1. Check the log file for specific error messages
2. Verify column names match exactly
3. Ensure no extra spaces in column headers
4. Test with sample_employee_data.csv first
5. Use Excel's "Text to Columns" to check formatting
