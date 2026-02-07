"""
System Validation Script
Tests if your system is ready to run the payslip generator
"""

import sys
import json
import os

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python 3.8 or higher is required")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print_header("Checking Required Packages")
    
    packages = {
        'pandas': 'Data processing',
        'reportlab': 'PDF generation',
        'twilio': 'WhatsApp (optional)',
        'openpyxl': 'Excel file handling'
    }
    
    all_installed = True
    
    for package, purpose in packages.items():
        try:
            __import__(package)
            print(f"✅ {package:20s} - {purpose}")
        except ImportError:
            if package == 'twilio':
                print(f"⚠️  {package:20s} - {purpose} (Optional - Install if using WhatsApp)")
            else:
                print(f"❌ {package:20s} - {purpose} (REQUIRED)")
                all_installed = False
    
    return all_installed

def check_config():
    """Check configuration file"""
    print_header("Checking Configuration File")
    
    if not os.path.exists('config.json'):
        print("❌ config.json not found")
        return False
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        print("✅ config.json file exists and is valid JSON")
        
        # Check email config
        if 'email' in config:
            email_conf = config['email']
            if email_conf.get('enabled'):
                if 'sender_email' in email_conf and email_conf['sender_email'] != 'your-email@gmail.com':
                    print("✅ Email configuration looks good")
                else:
                    print("⚠️  Email enabled but credentials not configured")
                    print("   Update sender_email and password in config.json")
            else:
                print("ℹ️  Email is disabled")
        
        # Check WhatsApp config
        if 'whatsapp' in config:
            wa_conf = config['whatsapp']
            if wa_conf.get('enabled'):
                if 'account_sid' in wa_conf and wa_conf['account_sid'] != 'your-twilio-account-sid':
                    print("✅ WhatsApp configuration looks good")
                else:
                    print("⚠️  WhatsApp enabled but credentials not configured")
            else:
                print("ℹ️  WhatsApp is disabled")
        
        return True
        
    except json.JSONDecodeError:
        print("❌ config.json contains invalid JSON")
        return False
    except Exception as e:
        print(f"❌ Error reading config: {str(e)}")
        return False

def check_sample_csv():
    """Check if sample CSV exists"""
    print_header("Checking Sample Data")
    
    if os.path.exists('sample_employee_data.csv'):
        print("✅ sample_employee_data.csv found")
        print("   You can test with: python payslip_generator.py sample_employee_data.csv")
        return True
    else:
        print("⚠️  sample_employee_data.csv not found")
        print("   Create your own CSV file or generate sample file")
        return False

def check_output_directory():
    """Check output directory"""
    print_header("Checking Output Directory")
    
    if os.path.exists('payslips'):
        print("✅ Output directory 'payslips' exists")
    else:
        print("ℹ️  Output directory 'payslips' will be created automatically")
    
    return True

def main():
    print("\n" + "█" * 60)
    print(" " * 15 + "PAYSLIP GENERATOR")
    print(" " * 12 + "SYSTEM VALIDATION TEST")
    print("█" * 60)
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Configuration", check_config()))
    results.append(("Sample Data", check_sample_csv()))
    results.append(("Output Directory", check_output_directory()))
    
    # Summary
    print_header("VALIDATION SUMMARY")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:10s} - {test_name}")
        if not passed and test_name not in ["Sample Data"]:
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✅ Your system is ready to run the payslip generator!")
        print("\nNext steps:")
        print("1. Update config.json with your email credentials")
        print("2. Prepare your employee data CSV file")
        print("3. Run: python payslip_generator.py employee_data.csv")
        print("\nOr test with sample data:")
        print("   python payslip_generator.py sample_employee_data.csv")
    else:
        print("❌ Some required components are missing")
        print("\nPlease fix the issues above before running the application")
        print("\nQuick fixes:")
        print("- Install missing packages: pip install pandas reportlab")
        print("- Update config.json with your credentials")
    
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
