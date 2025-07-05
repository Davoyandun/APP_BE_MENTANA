#!/usr/bin/env python3
"""
Execution script for APP_BE_MENTANA
Facilitates development and testing of the application
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command: str, description: str = None):
    """Executes a command and handles errors"""
    if description:
        print(f"🔄 {description}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing: {command}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def check_dependencies():
    """Verifies that dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        return False
    
    # Check pip
    if not run_command("pip --version", "Checking pip"):
        return False
    
    # Check AWS CLI (optional)
    if run_command("aws --version", "Checking AWS CLI"):
        print("✅ AWS CLI found")
    else:
        print("⚠️  AWS CLI not found (optional)")
    
    return True


def install_dependencies():
    """Installs project dependencies"""
    print("📦 Installing dependencies...")
    
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    print("✅ Dependencies installed successfully")
    return True


def run_tests():
    """Runs project tests"""
    print("🧪 Running tests...")
    
    if not run_command("pytest", "Running tests"):
        return False
    
    print("✅ Tests executed successfully")
    return True


def run_development_server():
    """Runs the development server"""
    print("🚀 Starting development server...")
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("⚠️  .env file not found. Copying env.example...")
        run_command("cp env.example .env", "Copying configuration file")
    
    # Run server
    if not run_command("uvicorn main:app --reload --host 0.0.0.0 --port 8000", "Starting server"):
        return False
    
    return True


def run_aws_check():
    """Checks AWS configuration"""
    print("☁️  Checking AWS configuration...")
    
    if not run_command("aws sts get-caller-identity", "Checking AWS credentials"):
        print("⚠️  AWS not configured correctly")
        return False
    
    print("✅ AWS configured correctly")
    return True


def setup_dynamodb():
    """Sets up DynamoDB table"""
    print("🗄️  Setting up DynamoDB table...")
    
    if not run_command("python scripts/setup_dynamodb_local.py", "Setting up DynamoDB"):
        return False
    
    print("✅ DynamoDB setup completed")
    return True


def setup_venv():
    """Sets up virtual environment"""
    print("🐍 Setting up virtual environment...")
    
    if not run_command("python scripts/setup_venv.py", "Running virtual environment setup"):
        return False
    
    print("✅ Virtual environment setup completed")
    return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Execution script for APP_BE_MENTANA")
    parser.add_argument("command", choices=[
        "check", "install", "test", "dev", "aws", "venv", "test-api", "dynamodb", "all"
    ], help="Command to execute")
    
    args = parser.parse_args()
    
    print("🎯 APP_BE_MENTANA - Execution Script")
    print("=" * 50)
    
    if args.command == "check":
        check_dependencies()
    
    elif args.command == "install":
        if check_dependencies():
            install_dependencies()
    
    elif args.command == "test":
        if check_dependencies():
            run_tests()
    
    elif args.command == "dev":
        if check_dependencies():
            run_development_server()
    
    elif args.command == "aws":
        run_aws_check()
    
    elif args.command == "venv":
        setup_venv()
    
    elif args.command == "test-api":
        print("🧪 Testing API endpoints...")
        run_command("python scripts/test_endpoints.py", "Running API endpoint tests")
    
    elif args.command == "dynamodb":
        setup_dynamodb()
    
    elif args.command == "all":
        if check_dependencies():
            setup_venv()
            install_dependencies()
            setup_dynamodb()
            run_tests()
            print("\n🎉 Setup completed!")
            print("To start the development server:")
            print("  python run.py dev")
            print("To check AWS:")
            print("  python run.py aws")
            print("To test API endpoints:")
            print("  python run.py test-api")


if __name__ == "__main__":
    main() 