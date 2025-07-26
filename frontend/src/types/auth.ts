export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  status: 'pending_verification' | 'active' | 'inactive' | 'banned';
  email_verified: boolean;
  has_completed_profile: boolean;
  last_seen: string | null;
  created_at: string;
}

export interface LoginCredentials {
  identifier: string; // email or username
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

// API Response Types
export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface RegisterResponse {
  message: string;
  user_id: number;
  email: string;
  username: string;
  verification_token: string;
  email_sent: boolean;
}

export interface VerificationResponse {
  message: string;
  user_id: number;
  status: string;
  email_verified: boolean;
}

export interface PasswordResetResponse {
  message: string;
  email: string;
  reset_token?: string; // Only in development
}

export interface MessageResponse {
  message: string;
}

export interface ErrorResponse {
  detail: string;
  error_code?: string;
}

// Auth State Types
export interface AuthState {
  user: User | null;
  access_token: string | null;
  refresh_token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface AuthError {
  message: string;
  code?: string;
  field?: string;
}

// Form Types
export interface LoginFormData {
  identifier: string;
  password: string;
}

export interface RegisterFormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  first_name: string;
  last_name: string;
}

export interface EmailVerificationData {
  token: string;
}

export interface PasswordResetRequestData {
  email: string;
}

export interface PasswordResetConfirmData {
  email: string;
  token: string;
  new_password: string;
  confirm_password: string;
}