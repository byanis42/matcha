#!/usr/bin/env python3
"""Debug script for login issue"""

import asyncio
import sys
import os

# Add backend to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.infrastructure.database.session import async_session_factory
from backend.src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from backend.src.application.use_cases.auth.login_user import LoginUserUseCase


async def test_login():
    """Test the login flow directly"""
    print("🔍 Testing login flow...")
    
    login_data = {
        "identifier": "test@example.com",
        "password": "TestPassword123"
    }
    
    try:
        async with async_session_factory() as session:
            # Create repository
            user_repository = UserRepositoryImpl(session)
            
            # Create use case
            login_use_case = LoginUserUseCase(user_repository)
            
            # Execute login
            result = await login_use_case.execute(login_data)
            
            print("✅ Login successful!")
            print(f"   Access token: {result['access_token'][:20]}...")
            print(f"   Token type: {result['token_type']}")
            print(f"   User: {result['user']}")
            
    except Exception as e:
        print(f"❌ Login failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_login())