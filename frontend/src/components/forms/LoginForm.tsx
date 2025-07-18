import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link } from 'react-router-dom';
import { Eye, EyeOff } from 'lucide-react';
import { Button, Input } from '../ui';
import { useAuth } from '../../hooks/useAuth';
import { loginSchema, LoginFormData } from '../../utils/validationSchemas';
import toast from 'react-hot-toast';

interface LoginFormProps {
  onSuccess?: () => void;
  redirectTo?: string;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSuccess, redirectTo }) => {
  const [showPassword, setShowPassword] = useState(false);
  const { login, isLoading } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      identifier: '',
      password: '',
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      const result = await login(data);
      
      if (result.success) {
        toast.success('Welcome back!');
        onSuccess?.();
        
        // Redirect if specified
        if (redirectTo) {
          window.location.href = redirectTo;
        }
      } else {
        toast.error(result.error || 'Login failed');
        
        // Handle specific error cases
        if (result.error?.includes('password')) {
          setError('password', { message: result.error });
        } else if (result.error?.includes('email') || result.error?.includes('username')) {
          setError('identifier', { message: result.error });
        }
      }
    } catch (error: any) {
      toast.error(error.message || 'An unexpected error occurred');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Input
          {...register('identifier')}
          label="Email or Username"
          placeholder="Enter your email or username"
          error={errors.identifier?.message}
          autoComplete="username"
        />
      </div>

      <div className="relative">
        <Input
          {...register('password')}
          type={showPassword ? 'text' : 'password'}
          label="Password"
          placeholder="Enter your password"
          error={errors.password?.message}
          autoComplete="current-password"
        />
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="absolute right-3 top-8 text-gray-400 hover:text-gray-600"
        >
          {showPassword ? (
            <EyeOff className="h-4 w-4" />
          ) : (
            <Eye className="h-4 w-4" />
          )}
        </button>
      </div>

      <div className="flex items-center justify-between">
        <Link
          to="/auth/forgot-password"
          className="text-sm text-blue-600 hover:text-blue-500"
        >
          Forgot your password?
        </Link>
      </div>

      <Button
        type="submit"
        className="w-full"
        isLoading={isLoading}
        disabled={isLoading}
      >
        Sign In
      </Button>

      <div className="text-center">
        <span className="text-sm text-gray-600">
          Don't have an account?{' '}
          <Link
            to="/auth/register"
            className="text-blue-600 hover:text-blue-500 font-medium"
          >
            Sign up
          </Link>
        </span>
      </div>
    </form>
  );
};