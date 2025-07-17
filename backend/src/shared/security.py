from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt

from ..config.settings import get_settings

settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str) -> Dict[str, Any]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


def get_current_user_from_token(token: str) -> Dict[str, Any]:
    """Extract user information from JWT token"""
    try:
        payload = verify_token(token)
        
        if payload.get("type") != "access":
            raise Exception("Invalid token type")
        
        user_id = payload.get("user_id")
        email = payload.get("email")
        
        if not user_id:
            raise Exception("Invalid token payload")
        
        return {"user_id": user_id, "email": email}
    
    except Exception as e:
        raise Exception(f"Token validation failed: {str(e)}")


def refresh_access_token(refresh_token: str) -> str:
    """Generate new access token from refresh token"""
    try:
        payload = verify_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise Exception("Invalid token type")
        
        user_id = payload.get("user_id")
        if not user_id:
            raise Exception("Invalid token payload")
        
        # Create new access token
        new_token_data = {"user_id": user_id}
        return create_access_token(new_token_data)
    
    except Exception as e:
        raise Exception(f"Token refresh failed: {str(e)}")


def generate_verification_token(user_id: int) -> str:
    """Generate email verification token"""
    data = {
        "user_id": user_id,
        "type": "email_verification",
        "exp": datetime.utcnow() + timedelta(hours=24)  # 24 hours expiry
    }
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_verification_token(token: str) -> Dict[str, Any]:
    """Verify email verification token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        if payload.get("type") != "email_verification":
            raise Exception("Invalid token type")
        
        return payload
    
    except jwt.ExpiredSignatureError:
        raise Exception("Verification token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid verification token")