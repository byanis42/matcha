import { useEffect } from 'react';
import { useAuthStore } from '../stores/authStore';
import {
  LoginCredentials,
  RegisterData,
  EmailVerificationData,
  PasswordResetRequestData,
  PasswordResetConfirmData,
} from '../types';

export const useAuth = () => {
  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    verifyEmail,
    requestPasswordReset,
    confirmPasswordReset,
    getCurrentUser,
    clearError,
    initialize,
  } = useAuthStore();

  // Initialize auth store on mount
  useEffect(() => {
    initialize();
  }, []); // Remove initialize dependency to prevent loops

  // Auth helpers
  const isEmailVerified = user?.email_verified ?? false;
  const isActive = user?.status === 'active';
  const isPendingVerification = user?.status === 'pending_verification';
  const isLoggedIn = isAuthenticated && !!user;

  // Wrapper functions with better error handling and type safety
  const handleLogin = async (credentials: LoginCredentials) => {
    try {
      await login(credentials);
      return { success: true };
    } catch (error: any) {
      return { 
        success: false, 
        error: error.detail || 'Login failed' 
      };
    }
  };

  const handleRegister = async (userData: RegisterData) => {
    try {
      const result = await register(userData);
      return { 
        success: true, 
        message: result.message,
        emailSent: result.emailSent 
      };
    } catch (error: any) {
      return { 
        success: false, 
        error: error.detail || 'Registration failed' 
      };
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      return { success: true };
    } catch (error: any) {
      return { 
        success: false, 
        error: error.detail || 'Logout failed' 
      };
    }
  };

  const handleVerifyEmail = async (data: EmailVerificationData) => {
    try {
      const result = await verifyEmail(data);
      return { 
        success: true, 
        message: result.message 
      };
    } catch (error: any) {
      return { 
        success: false, 
        error: error.detail || 'Email verification failed' 
      };
    }
  };

  const handleRequestPasswordReset = async (data: PasswordResetRequestData) => {
    try {
      const result = await requestPasswordReset(data);
      return { 
        success: true, 
        message: result.message 
      };
    } catch (error: any) {
      return { 
        success: false, 
        error: error.detail || 'Password reset request failed' 
      };
    }
  };

  const handleConfirmPasswordReset = async (data: PasswordResetConfirmData) => {
    try {
      const result = await confirmPasswordReset(data);
      return { 
        success: true, 
        message: result.message 
      };
    } catch (error: any) {
      return { 
        success: false, 
        error: error.detail || 'Password reset failed' 
      };
    }
  };

  const refreshUserData = async () => {
    try {
      await getCurrentUser();
      return { success: true };
    } catch (error: any) {
      return { 
        success: false, 
        error: error.detail || 'Failed to refresh user data' 
      };
    }
  };

  return {
    // State
    user,
    isAuthenticated,
    isLoading,
    error,
    isEmailVerified,
    isActive,
    isPendingVerification,
    isLoggedIn,

    // Actions
    login: handleLogin,
    register: handleRegister,
    logout: handleLogout,
    verifyEmail: handleVerifyEmail,
    requestPasswordReset: handleRequestPasswordReset,
    confirmPasswordReset: handleConfirmPasswordReset,
    refreshUserData,
    clearError,
  };
};