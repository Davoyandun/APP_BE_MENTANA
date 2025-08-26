import boto3
from typing import List, Optional
from uuid import UUID
import json
from datetime import datetime, timezone

from domain.src.entities.user import User
from domain.src.repositories.user_repository import UserRepository
from config import get_aws_config


class AWSDynamoDBUserRepository(UserRepository):
    """User repository implementation using AWS DynamoDB"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb', **get_aws_config())
        self.table = self.dynamodb.Table(table_name)
    
    async def save(self, user: User) -> User:
        """Saves a user to DynamoDB"""
        try:
            item = {
                'id': str(user.id),
                'email': user.email,
                'name': user.name,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat(),
                'updated_at': user.updated_at.isoformat()
            }
            
            self.table.put_item(Item=item)
            return user
            
        except Exception as e:
            raise Exception(f"Error saving user to DynamoDB: {str(e)}")
    
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Finds a user by ID in DynamoDB"""
        try:
            response = self.table.get_item(Key={'id': str(user_id)})
            
            if 'Item' not in response:
                return None
            
            item = response['Item']
            return self._item_to_user(item)
            
        except Exception as e:
            raise Exception(f"Error finding user by ID in DynamoDB: {str(e)}")
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Finds a user by email in DynamoDB"""
        try:
            # Assuming you have a GSI on email
            response = self.table.query(
                IndexName='email-index',
                KeyConditionExpression='email = :email',
                ExpressionAttributeValues={':email': email}
            )
            
            if not response['Items']:
                return None
            
            item = response['Items'][0]
            return self._item_to_user(item)
            
        except Exception as e:
            raise Exception(f"Error finding user by email in DynamoDB: {str(e)}")
    
    async def find_all(self) -> List[User]:
        """Gets all users from DynamoDB"""
        try:
            response = self.table.scan()
            users = []
            
            for item in response['Items']:
                users.append(self._item_to_user(item))
            
            return users
            
        except Exception as e:
            raise Exception(f"Error finding all users in DynamoDB: {str(e)}")
    
    async def find_active_users(self) -> List[User]:
        """Gets all active users from DynamoDB"""
        try:
            response = self.table.scan(
                FilterExpression='is_active = :is_active',
                ExpressionAttributeValues={':is_active': True}
            )
            
            users = []
            for item in response['Items']:
                users.append(self._item_to_user(item))
            
            return users
            
        except Exception as e:
            raise Exception(f"Error finding active users in DynamoDB: {str(e)}")
    
    async def delete(self, user_id: UUID) -> bool:
        """Deletes a user from DynamoDB"""
        try:
            response = self.table.delete_item(Key={'id': str(user_id)})
            return 'Attributes' in response
            
        except Exception as e:
            raise Exception(f"Error deleting user from DynamoDB: {str(e)}")
    
    async def update(self, user: User) -> User:
        """Updates a user in DynamoDB"""
        try:
            update_expression = "SET #name = :name, is_active = :is_active, updated_at = :updated_at"
            expression_attribute_names = {"#name": "name"}
            expression_attribute_values = {
                ':name': user.name,
                ':is_active': user.is_active,
                ':updated_at': user.updated_at.isoformat()
            }
            
            self.table.update_item(
                Key={'id': str(user.id)},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values
            )
            
            return user
            
        except Exception as e:
            raise Exception(f"Error updating user in DynamoDB: {str(e)}")
    
    def _item_to_user(self, item: dict) -> User:
        """Converts a DynamoDB item to a User entity"""
        # Parse datetime strings and ensure timezone awareness
        created_at = datetime.fromisoformat(item['created_at'])
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
            
        updated_at = datetime.fromisoformat(item['updated_at'])
        if updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=timezone.utc)
        
        return User(
            id=UUID(item['id']),
            email=item['email'],
            name=item['name'],
            is_active=item['is_active'],
            created_at=created_at,
            updated_at=updated_at
        ) 