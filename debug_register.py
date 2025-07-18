#!/usr/bin/env python3
"""Debug script for registration issue"""

import asyncio
import sys
import os

# Add backend to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.infrastructure.database.session import async_session_factory
from backend.src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from backend.src.application.use_cases.auth.register_user import RegisterUserUseCase


async def test_registration():
    """Test the registration flow directly"""
    print("🔍 Testing registration flow...")
    
    user_data = {
        "username": "testuser_debug",
        "email": "test_debug@example.com",
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        async with async_session_factory() as session:
            # Create repository
            user_repository = UserRepositoryImpl(session)
            
            # Create use case
            register_use_case = RegisterUserUseCase(user_repository)
            
            # Execute registration
            result = await register_use_case.execute(user_data)
            
            print("✅ Registration successful!")
            print(f"   User ID: {result['user_id']}")
            print(f"   Email: {result['email']}")
            print(f"   Username: {result['username']}")
            print(f"   Message: {result['message']}")
            
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_registration())