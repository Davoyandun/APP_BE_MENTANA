#!/usr/bin/env python3
"""
Virtual Environment Setup Script for APP_BE_MENTANA

This script automates the creation and configuration of a virtual environment
for the APP_BE_MENTANA project.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command, check=True, capture_output=False):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e}")
        return None


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def create_virtual_environment(venv_path="venv"):
    """Create a virtual environment."""
    if os.path.exists(venv_path):
        print(f"⚠️  Virtual environment already exists at {venv_path}")
        response = input("Do you want to recreate it? (y/N): ").lower()
        if response != 'y':
            print("Using existing virtual environment")
            return True
        else:
            print(f"Removing existing virtual environment: {venv_path}")
            run_command(f"rm -rf {venv_path}")
    
    print(f"Creating virtual environment: {venv_path}")
    result = run_command(f"python -m venv {venv_path}")
    
    if result and result.returncode == 0:
        print(f"✅ Virtual environment created: {venv_path}")
        return True
    else:
        print("❌ Failed to create virtual environment")
        return False


def get_activate_command(venv_path="venv"):
    """Get the activation command based on the operating system."""
    system = platform.system().lower()
    
    if system == "windows":
        return f"{venv_path}\\Scripts\\activate"
    else:
        return f"source {venv_path}/bin/activate"


def install_dependencies(venv_path="venv"):
    """Install project dependencies."""
    system = platform.system().lower()
    
    if system == "windows":
        pip_path = f"{venv_path}\\Scripts\\pip"
    else:
        pip_path = f"{venv_path}/bin/pip"
    
    print("Installing dependencies...")
    
    # Upgrade pip first
    print("Upgrading pip...")
    run_command(f"{pip_path} install --upgrade pip")
    
    # Install requirements
    print("Installing requirements...")
    result = run_command(f"{pip_path} install -r requirements.txt")
    
    if result and result.returncode == 0:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print("❌ Failed to install dependencies")
        return False


def setup_environment_file():
    """Setup environment file from example."""
    if not os.path.exists("env.example"):
        print("⚠️  env.example file not found")
        return False
    
    if os.path.exists(".env"):
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print("Using existing .env file")
            return True
    
    print("Creating .env file from env.example...")
    run_command("cp env.example .env")
    print("✅ .env file created")
    print("⚠️  Remember to edit .env with your AWS credentials")
    return True


def main():
    """Main setup function."""
    print("🚀 APP_BE_MENTANA - Virtual Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment file
    setup_environment_file()
    
    # Get activation command
    activate_cmd = get_activate_command()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print(f"1. Activate virtual environment:")
    print(f"   {activate_cmd}")
    print("2. Edit .env file with your AWS credentials")
    print("3. Run the application:")
    print("   python run.py dev")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main() 