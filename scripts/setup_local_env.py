#!/usr/bin/env python3
"""
Setup local environment for development
"""

import os
from pathlib import Path


def setup_local_env():
    """Setup local environment configuration"""
    print("🔧 Setting up local environment...")
    
    # Read env.example
    env_example_path = Path("env.example")
    env_path = Path(".env")
    
    if not env_example_path.exists():
        print("❌ env.example not found")
        return False
    
    # Copy env.example to .env if it doesn't exist
    if not env_path.exists():
        print("📋 Creating .env from env.example...")
        with open(env_example_path, 'r') as f:
            content = f.read()
        
        # Add local development settings
        content += "\n# Local Development Settings\n"
        content += "AWS_ENDPOINT_URL=http://localhost:8000\n"
        content += "AWS_DYNAMODB_TABLE=users\n"
        content += "AWS_S3_BUCKET=test-bucket\n"
        content += "DEBUG=true\n"
        
        with open(env_path, 'w') as f:
            f.write(content)
        
        print("✅ .env file created with local settings")
    else:
        print("✅ .env file already exists")
    
    return True


if __name__ == "__main__":
    setup_local_env() 