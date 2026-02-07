@echo off
REM Payslip Generator - Windows Launcher
echo ============================================================
echo              PAYSLIP GENERATOR
echo ============================================================
echo.

REM Check if CSV file is provided
if "%1"=="" (
    echo Usage: run_payslip.bat employee_data.csv
    echo.
    echo Example: run_payslip.bat sample_employee_data.csv
    echo.
    pause
    exit /b 1
)

REM Check if file exists
if not exist "%1" (
    echo Error: File '%1' not found!
    echo.
    pause
    exit /b 1
)

echo Processing: %1
echo.

REM Run the application
python payslip_generator.py "%1"

echo.
echo ============================================================
echo Check 'payslips' folder for generated PDFs
echo Check 'payslip_generator.log' for detailed logs
echo ============================================================
echo.
pause
