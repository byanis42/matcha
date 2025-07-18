import { apiClient } from '../api/client';
import {
  LoginCredentials,
  RegisterData,
  LoginResponse,
  RegisterResponse,
  VerificationResponse,
  PasswordResetResponse,
  MessageResponse,
  EmailVerificationData,
  PasswordResetRequestData,
  PasswordResetConfirmData,
  User,
} from '../../types';

class AuthService {
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>('/auth/login', credentials);
    
    // Set tokens in API client for future requests
    apiClient.setTokens(response.access_token, response.refresh_token);
    
    return response;
  }

  async register(userData: RegisterData): Promise<RegisterResponse> {
    return apiClient.post<RegisterResponse>('/auth/register', userData);
  }

  async verifyEmail(data: EmailVerificationData): Promise<VerificationResponse> {
    return apiClient.post<VerificationResponse>('/auth/verify-email', data);
  }

  async requestPasswordReset(data: PasswordResetRequestData): Promise<PasswordResetResponse> {
    return apiClient.post<PasswordResetResponse>('/auth/reset-password/request', data);
  }

  async confirmPasswordReset(data: PasswordResetConfirmData): Promise<MessageResponse> {
    return apiClient.post<MessageResponse>('/auth/reset-password/confirm', data);
  }

  async getCurrentUser(): Promise<User> {
    return apiClient.get<User>('/auth/me');
  }

  async logout(): Promise<MessageResponse> {
    const response = await apiClient.post<MessageResponse>('/auth/logout');
    
    // Clear tokens from API client
    apiClient.clearTokens();
    
    return response;
  }

  async refreshToken(refreshToken: string): Promise<{ access_token: string }> {
    const response = await apiClient.post<{ access_token: string }>('/auth/refresh', {
      refresh_token: refreshToken,
    });
    
    return response;
  }

  // Token management helpers
  setTokens(accessToken: string, refreshToken: string): void {
    apiClient.setTokens(accessToken, refreshToken);
  }

  clearTokens(): void {
    apiClient.clearTokens();
  }
}

// Export singleton instance
export const authService = new AuthService();