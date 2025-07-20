import { ApiError } from '../../types';

interface RequestConfig {
  headers?: Record<string, string>;
  signal?: AbortSignal;
}

class FetchApiClient {
  private baseURL: string;
  private timeout: number;
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  constructor() {
    this.baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    this.timeout = 10000; // 10 seconds
    
    // Restore tokens from localStorage on initialization
    this.restoreTokensFromStorage();
  }

  private restoreTokensFromStorage() {
    try {
      const authStorage = localStorage.getItem('auth-storage');
      if (authStorage) {
        const parsed = JSON.parse(authStorage);
        if (parsed.state?.access_token && parsed.state?.refresh_token) {
          this.accessToken = parsed.state.access_token;
          this.refreshToken = parsed.state.refresh_token;
        }
      }
    } catch (error) {
      console.warn('Failed to restore tokens from localStorage:', error);
    }
  }

  private async makeRequest<T = any>(
    url: string,
    options: RequestInit = {},
    config: RequestConfig = {}
  ): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    // Use the provided signal or the timeout signal
    const signal = config.signal || controller.signal;

    try {
      const fullUrl = `${this.baseURL}${url}`;
      
      // Prepare headers
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...config.headers,
        ...options.headers as Record<string, string>,
      };

      // Add auth token if available
      if (this.accessToken) {
        headers.Authorization = `Bearer ${this.accessToken}`;
      }

      // Log request for debugging (similar to axios version)
      if (options.method !== 'GET') {
        console.log('API Request:', {
          url: fullUrl,
          method: options.method,
          data: options.body ? JSON.parse(options.body as string) : undefined,
          headers
        });
      }

      const response = await fetch(fullUrl, {
        ...options,
        headers,
        signal,
      });

      clearTimeout(timeoutId);

      // Handle token refresh for 401 errors
      if (response.status === 401 && this.refreshToken && !url.includes('/auth/refresh')) {
        try {
          const newTokenData = await this.refreshAccessToken();
          this.setTokens(newTokenData.access_token, this.refreshToken);
          
          // Retry the original request with new token
          headers.Authorization = `Bearer ${newTokenData.access_token}`;
          const retryResponse = await fetch(fullUrl, {
            ...options,
            headers,
          });

          return this.handleResponse<T>(retryResponse);
        } catch (refreshError) {
          // Refresh failed, clear tokens and redirect to login
          this.clearTokens();
          window.location.href = '/auth/login';
          throw refreshError;
        }
      }

      return this.handleResponse<T>(response);

    } catch (error) {
      clearTimeout(timeoutId);
      throw this.formatError(error);
    }
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    const contentType = response.headers.get('content-type');
    const isJson = contentType?.includes('application/json');

    if (!response.ok) {
      const errorData = isJson ? await response.json() : await response.text();
      
      throw {
        response: {
          status: response.status,
          statusText: response.statusText,
          data: isJson ? errorData : { detail: errorData }
        }
      };
    }

    if (response.status === 204) {
      // No content
      return {} as T;
    }

    const data = isJson ? await response.json() : await response.text();

    // Log response for debugging (similar to axios version)
    if (isJson) {
      console.log('API Response:', data);
    }

    return data;
  }

  private formatError(error: any): ApiError {
    console.error('API Error:', error);

    if (error.name === 'AbortError') {
      return {
        detail: 'Request timeout - please try again',
        status: 0,
      };
    }

    if (error.response) {
      console.error('Error Response:', error.response.data);
      // Server responded with error status
      return {
        detail: error.response.data?.detail || error.response.data?.message || 'An error occurred',
        error_code: error.response.data?.error_code,
        status: error.response.status,
      };
    } else if (error instanceof TypeError && error.message.includes('fetch')) {
      console.error('Network Error - No response received');
      // Network error (fetch failed)
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
    
    // Update localStorage to keep tokens in sync
    this.updateTokensInStorage(accessToken, refreshToken);
  }

  clearTokens() {
    this.accessToken = null;
    this.refreshToken = null;
    
    // Clear tokens from localStorage
    this.updateTokensInStorage(null, null);
  }

  private updateTokensInStorage(accessToken: string | null, refreshToken: string | null) {
    try {
      const authStorage = localStorage.getItem('auth-storage');
      if (authStorage) {
        const parsed = JSON.parse(authStorage);
        if (parsed.state) {
          parsed.state.access_token = accessToken;
          parsed.state.refresh_token = refreshToken;
          localStorage.setItem('auth-storage', JSON.stringify(parsed));
        }
      }
    } catch (error) {
      console.warn('Failed to update tokens in localStorage:', error);
    }
  }

  private async refreshAccessToken(): Promise<{ access_token: string }> {
    const response = await fetch(`${this.baseURL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh_token: this.refreshToken }),
    });

    if (!response.ok) {
      throw new Error('Token refresh failed');
    }

    return response.json();
  }

  // HTTP methods - same interface as axios client
  async get<T = any>(url: string, config?: RequestConfig): Promise<T> {
    return this.makeRequest<T>(url, { method: 'GET' }, config);
  }

  async post<T = any>(url: string, data?: any, config?: RequestConfig): Promise<T> {
    return this.makeRequest<T>(
      url,
      {
        method: 'POST',
        body: data ? JSON.stringify(data) : undefined,
      },
      config
    );
  }

  async put<T = any>(url: string, data?: any, config?: RequestConfig): Promise<T> {
    return this.makeRequest<T>(
      url,
      {
        method: 'PUT',
        body: data ? JSON.stringify(data) : undefined,
      },
      config
    );
  }

  async patch<T = any>(url: string, data?: any, config?: RequestConfig): Promise<T> {
    return this.makeRequest<T>(
      url,
      {
        method: 'PATCH',
        body: data ? JSON.stringify(data) : undefined,
      },
      config
    );
  }

  async delete<T = any>(url: string, config?: RequestConfig): Promise<T> {
    return this.makeRequest<T>(url, { method: 'DELETE' }, config);
  }
}

// Create singleton instance
export const apiClient = new FetchApiClient();