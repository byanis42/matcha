// Auth types
export type {
  User,
  LoginCredentials,
  RegisterData,
  LoginResponse,
  RegisterResponse,
  VerificationResponse,
  PasswordResetResponse,
  MessageResponse,
  ErrorResponse,
  AuthState,
  AuthError,
  LoginFormData,
  RegisterFormData,
  EmailVerificationData,
  PasswordResetRequestData,
  PasswordResetConfirmData,
} from './auth';

// API types
export type {
  ApiResponse,
  ApiError,
  PaginatedResponse,
  ApiConfig,
  HttpMethod,
  RequestConfig,
} from './api';

// Profile types
export type {
  ProfileFormData,
  LocationData,
  UserProfile,
} from './profile';

export {
  GENDER_OPTIONS,
  SEXUAL_PREFERENCE_OPTIONS,
  COMMON_INTERESTS,
} from './profile';