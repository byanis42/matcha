import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { authService } from '../services/auth';
import {
  AuthState,
  LoginCredentials,
  RegisterData,
  EmailVerificationData,
  PasswordResetRequestData,
  PasswordResetConfirmData,
} from '../types';

interface AuthActions {
  // Actions
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (userData: RegisterData) => Promise<{ message: string; emailSent: boolean }>;
  logout: () => Promise<void>;
  verifyEmail: (data: EmailVerificationData) => Promise<{ message: string }>;
  requestPasswordReset: (data: PasswordResetRequestData) => Promise<{ message: string }>;
  confirmPasswordReset: (data: PasswordResetConfirmData) => Promise<{ message: string }>;
  getCurrentUser: () => Promise<void>;
  clearError: () => void;
  initialize: () => Promise<void>;
}

interface AuthStore extends AuthState, AuthActions {}

const initialState: AuthState = {
  user: null,
  access_token: null,
  refresh_token: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      ...initialState,

      login: async (credentials: LoginCredentials) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await authService.login(credentials);
          
          set({
            user: response.user,
            access_token: response.access_token,
            refresh_token: response.refresh_token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Login failed',
          });
          throw error;
        }
      },

      register: async (userData: RegisterData) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await authService.register(userData);
          
          set({
            isLoading: false,
            error: null,
          });
          
          return {
            message: response.message,
            emailSent: response.email_sent,
          };
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Registration failed',
          });
          throw error;
        }
      },

      logout: async () => {
        set({ isLoading: true });
        
        try {
          await authService.logout();
        } catch (error) {
          // Continue with logout even if API call fails
          console.warn('Logout API call failed:', error);
        } finally {
          set({
            ...initialState,
            isLoading: false,
          });
        }
      },

      verifyEmail: async (data: EmailVerificationData) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await authService.verifyEmail(data);
          
          // If user is logged in, update their verification status
          const currentUser = get().user;
          if (currentUser) {
            set({
              user: {
                ...currentUser,
                email_verified: response.email_verified,
                status: response.status as any,
              },
            });
          }
          
          set({
            isLoading: false,
            error: null,
          });
          
          return { message: response.message };
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Email verification failed',
          });
          throw error;
        }
      },

      requestPasswordReset: async (data: PasswordResetRequestData) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await authService.requestPasswordReset(data);
          
          set({
            isLoading: false,
            error: null,
          });
          
          return { message: response.message };
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Password reset request failed',
          });
          throw error;
        }
      },

      confirmPasswordReset: async (data: PasswordResetConfirmData) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await authService.confirmPasswordReset(data);
          
          set({
            isLoading: false,
            error: null,
          });
          
          return { message: response.message };
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Password reset failed',
          });
          throw error;
        }
      },

      getCurrentUser: async () => {
        set({ isLoading: true, error: null });
        
        try {
          const user = await authService.getCurrentUser();
          
          set({
            user,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          // If getting current user fails, clear auth state and tokens
          authService.clearTokens();
          set({
            ...initialState,
            isLoading: false,
            error: error.detail || 'Failed to get user info',
          });
          throw error;
        }
      },

      clearError: () => {
        set({ error: null });
      },

      initialize: async () => {
        set({ isLoading: true, error: null });
        
        const { access_token, refresh_token } = get();
        
        if (access_token && refresh_token) {
          // Set tokens in auth service
          authService.setTokens(access_token, refresh_token);
          
          // Verify tokens are still valid by getting current user
          try {
            await get().getCurrentUser();
          } catch (error) {
            // Tokens invalid, clear auth state and tokens
            authService.clearTokens();
            set({
              ...initialState,
              isLoading: false,
            });
          }
        } else {
          // No tokens, just stop loading
          set({ isLoading: false });
        }
      },
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        access_token: state.access_token,
        refresh_token: state.refresh_token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);