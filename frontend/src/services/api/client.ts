import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { ApiError } from '../../types';

class ApiClient {
  private client: AxiosInstance;
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        if (this.accessToken && config.headers) {
          config.headers.Authorization = `Bearer ${this.accessToken}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling and token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        // If token expired, try to refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            if (this.refreshToken) {
              const response = await this.refreshAccessToken();
              this.setTokens(response.access_token, this.refreshToken);
              
              // Retry original request with new token
              originalRequest.headers.Authorization = `Bearer ${response.access_token}`;
              return this.client(originalRequest);
            }
          } catch (refreshError) {
            // Refresh failed, clear tokens and redirect to login
            this.clearTokens();
            window.location.href = '/auth/login';
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(this.formatError(error));
      }
    );
  }

  private formatError(error: any): ApiError {
    console.error('API Error:', error);
    if (error.response) {
      console.error('Error Response:', error.response.data);
      // Server responded with error status
      return {
        detail: error.response.data?.detail || error.response.data?.message || 'An error occurred',
        error_code: error.response.data?.error_code,
        status: error.response.status,
      };
    } else if (error.request) {
      console.error('Network Error - No response received');
      // Request made but no response received
      return {
        detail: 'Network error - please check your connection',
        status: 0,
      };
    } else {
      console.error('Request Setup Error:', error.message);
      // Something else happened
      return {
        detail: error.message || 'An unexpected error occurred',
        status: 0,
      };
    }
  }

  // Token management
  setTokens(accessToken: string, refreshToken: string) {
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;
  }

  clearTokens() {
    this.accessToken = null;
    this.refreshToken = null;
  }

  private async refreshAccessToken(): Promise<{ access_token: string }> {
    const response = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}/auth/refresh`,
      { refresh_token: this.refreshToken },
      {
        headers: { 'Content-Type': 'application/json' },
      }
    );
    return response.data;
  }

  // HTTP methods
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    console.log('API POST:', {
      url: `${import.meta.env.VITE_API_BASE_URL}${url}`,
      data,
      headers: config?.headers
    });
    const response = await this.client.post<T>(url, data, config);
    console.log('API Response:', response.data);
    return response.data;
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config);
    return response.data;
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }
}

// Create singleton instance
export const apiClient = new ApiClient();