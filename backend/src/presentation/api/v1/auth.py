from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from ...schemas.auth_schemas import (
    UserRegisterRequest, UserLoginRequest, EmailVerificationRequest,
    PasswordResetRequest, PasswordResetConfirmRequest, TokenRefreshRequest,
    RegisterResponse, TokenResponse, VerificationResponse, 
    PasswordResetResponse, MessageResponse, ErrorResponse
)
from ...api.dependencies import get_user_repository, get_current_user
from ....application.use_cases.auth.register_user import RegisterUserUseCase
from ....application.use_cases.auth.login_user import LoginUserUseCase
from ....application.use_cases.auth.verify_email import VerifyEmailUseCase
from ....application.use_cases.auth.reset_password import ResetPasswordUseCase
from ....core.repositories.user_repository import UserRepository
from ....shared.exceptions import (
    ValidationException, AuthenticationException, 
    DuplicateResourceException, NotFoundException
)
from ....shared.security import refresh_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegisterResponse)
async def register(
    user_data: UserRegisterRequest,
    user_repository: UserRepository = Depends(get_user_repository)
):
    """Register a new user"""
    try:
        use_case = RegisterUserUseCase(user_repository)
        result = await use_case.execute(user_data.dict())
        
        return RegisterResponse(
            message=result["message"],
            user_id=result["user_id"],
            email=result["email"],
            username=result["username"],
            verification_token=result["verification_token"]
        )
    
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except DuplicateResourceException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLoginRequest,
    user_repository: UserRepository = Depends(get_user_repository)
):
    """Login user and return tokens"""
    try:
        use_case = LoginUserUseCase(user_repository)
        result = await use_case.execute(login_data.dict())
        
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            token_type=result["token_type"],
            user=result["user"]
        )
    
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/verify-email", response_model=VerificationResponse)
async def verify_email(
    verification_data: EmailVerificationRequest,
    user_repository: UserRepository = Depends(get_user_repository)
):
    """Verify user email"""
    try:
        use_case = VerifyEmailUseCase(user_repository)
        result = await use_case.execute(verification_data.dict())
        
        return VerificationResponse(
            message=result["message"],
            user_id=result["user_id"],
            status=result["status"],
            email_verified=result["email_verified"]
        )
    
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification failed"
        )


@router.post("/reset-password/request", response_model=PasswordResetResponse)
async def request_password_reset(
    reset_data: PasswordResetRequest,
    user_repository: UserRepository = Depends(get_user_repository)
):
    """Request password reset"""
    try:
        use_case = ResetPasswordUseCase(user_repository)
        result = await use_case.request_reset(reset_data.email)
        
        return PasswordResetResponse(
            message=result["message"],
            email=result["email"],
            reset_token=result.get("reset_token")  # Only for development
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset request failed"
        )


@router.post("/reset-password/confirm", response_model=MessageResponse)
async def confirm_password_reset(
    reset_data: PasswordResetConfirmRequest,
    user_repository: UserRepository = Depends(get_user_repository)
):
    """Confirm password reset"""
    try:
        use_case = ResetPasswordUseCase(user_repository)
        result = await use_case.confirm_reset(reset_data.dict())
        
        return MessageResponse(message=result["message"])
    
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )


@router.post("/refresh", response_model=Dict[str, str])
async def refresh_token(token_data: TokenRefreshRequest):
    """Refresh access token"""
    try:
        new_access_token = refresh_access_token(token_data.refresh_token)
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed"
        )


@router.get("/me", response_model=Dict[str, Any])
async def get_current_user_info(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current user information"""
    return current_user


@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Logout user (invalidate token client-side)"""
    return MessageResponse(message="Logged out successfully")