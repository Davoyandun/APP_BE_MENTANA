#!/usr/bin/env python3
"""
DynamoDB Local Setup Script for APP_BE_MENTANA

This script sets up DynamoDB local for development purposes.
"""

import boto3
import json
import sys
from botocore.exceptions import ClientError, NoCredentialsError
from config import settings


def create_dynamodb_table():
    """Creates the DynamoDB table for users"""
    try:
        # Create DynamoDB client
        dynamodb = boto3.resource('dynamodb', **settings.get_aws_config())
        
        # Table name
        table_name = settings.aws_dynamodb_table or 'users'
        
        # Check if table already exists
        try:
            table = dynamodb.Table(table_name)
            table.load()
            print(f"✅ Table '{table_name}' already exists")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                pass  # Table doesn't exist, we'll create it
            else:
                raise e
        
        # Create table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'email-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'email',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Wait for table to be created
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        
        print(f"✅ Table '{table_name}' created successfully")
        return True
        
    except NoCredentialsError:
        print("❌ AWS credentials not found")
        print("Please configure AWS credentials using:")
        print("  aws configure")
        print("  or set environment variables:")
        print("  AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        return False
        
    except ClientError as e:
        print(f"❌ Error creating table: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """Main function"""
    print("🚀 Setting up DynamoDB Local for APP_BE_MENTANA")
    print("=" * 50)
    
    if create_dynamodb_table():
        print("\n✅ DynamoDB setup completed successfully!")
        print(f"Table name: {settings.aws_dynamodb_table or 'users'}")
        print("\nYou can now run the application with:")
        print("  python run.py dev")
    else:
        print("\n❌ DynamoDB setup failed")
        sys.exit(1)


if __name__ == "__main__":
    main() 