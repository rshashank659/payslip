#!/bin/bash
# Payslip Generator - Linux/Mac Launcher

echo "============================================================"
echo "              PAYSLIP GENERATOR"
echo "============================================================"
echo ""

# Check if CSV file is provided
if [ -z "$1" ]; then
    echo "Usage: ./run_payslip.sh employee_data.csv"
    echo ""
    echo "Example: ./run_payslip.sh sample_employee_data.csv"
    echo ""
    exit 1
fi

# Check if file exists
if [ ! -f "$1" ]; then
    echo "Error: File '$1' not found!"
    echo ""
    exit 1
fi

echo "Processing: $1"
echo ""

# Run the application
python3 payslip_generator.py "$1"

echo ""
echo "============================================================"
echo "Check 'payslips' folder for generated PDFs"
echo "Check 'payslip_generator.log' for detailed logs"
echo "============================================================"
echo ""
