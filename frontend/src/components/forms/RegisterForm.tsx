import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link } from 'react-router-dom';
import { Eye, EyeOff, Check } from 'lucide-react';
import { Button, Input } from '../ui';
import { useAuth } from '../../hooks/useAuth';
import { registerSchema, RegisterFormData } from '../../utils/validationSchemas';
import toast from 'react-hot-toast';

interface RegisterFormProps {
  onSuccess?: (data: { message: string; emailSent: boolean }) => void;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({ onSuccess }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [acceptTerms, setAcceptTerms] = useState(false);
  const { register: registerUser, isLoading } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setError,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      first_name: '',
      last_name: '',
    },
  });

  const password = watch('password');

  const passwordRequirements = [
    { met: password?.length >= 8, text: 'At least 8 characters' },
    { met: /(?=.*[a-z])/.test(password || ''), text: 'One lowercase letter' },
    { met: /(?=.*[A-Z])/.test(password || ''), text: 'One uppercase letter' },
    { met: /(?=.*\d)/.test(password || ''), text: 'One number' },
  ];

  const onSubmit = async (data: RegisterFormData) => {
    if (!acceptTerms) {
      toast.error('Please accept the terms and conditions');
      return;
    }

    try {
      // Remove confirmPassword from the data sent to API
      const { confirmPassword, ...registerData } = data;
      
      const result = await registerUser(registerData);
      
      if (result.success) {
        toast.success('Account created successfully! Please check your email.');
        onSuccess?.({
          message: result.message || 'Account created successfully',
          emailSent: result.emailSent || false
        });
      } else {
        toast.error(result.error || 'Registration failed');
        
        // Handle specific error cases
        if (result.error?.includes('email')) {
          setError('email', { message: result.error });
        } else if (result.error?.includes('username')) {
          setError('username', { message: result.error });
        }
      }
    } catch (error: any) {
      toast.error(error.message || 'An unexpected error occurred');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <Input
          {...register('first_name')}
          label="First Name"
          placeholder="John"
          error={errors.first_name?.message}
          autoComplete="given-name"
        />
        
        <Input
          {...register('last_name')}
          label="Last Name"
          placeholder="Doe"
          error={errors.last_name?.message}
          autoComplete="family-name"
        />
      </div>

      <Input
        {...register('username')}
        label="Username"
        placeholder="johndoe"
        error={errors.username?.message}
        autoComplete="username"
        helperText="Only letters, numbers, underscores, and hyphens allowed"
      />

      <Input
        {...register('email')}
        type="email"
        label="Email"
        placeholder="john@example.com"
        error={errors.email?.message}
        autoComplete="email"
      />

      <div className="relative">
        <Input
          {...register('password')}
          type={showPassword ? 'text' : 'password'}
          label="Password"
          placeholder="Create a strong password"
          error={errors.password?.message}
          autoComplete="new-password"
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

      {/* Password Requirements */}
      {password && (
        <div className="p-3 bg-gray-50 rounded-md">
          <p className="text-sm font-medium text-gray-700 mb-2">Password Requirements:</p>
          <ul className="space-y-1">
            {passwordRequirements.map((req, index) => (
              <li key={index} className="flex items-center text-sm">
                <Check
                  className={`h-3 w-3 mr-2 ${
                    req.met ? 'text-green-500' : 'text-gray-300'
                  }`}
                />
                <span className={req.met ? 'text-green-700' : 'text-gray-500'}>
                  {req.text}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="relative">
        <Input
          {...register('confirmPassword')}
          type={showConfirmPassword ? 'text' : 'password'}
          label="Confirm Password"
          placeholder="Confirm your password"
          error={errors.confirmPassword?.message}
          autoComplete="new-password"
        />
        <button
          type="button"
          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
          className="absolute right-3 top-8 text-gray-400 hover:text-gray-600"
        >
          {showConfirmPassword ? (
            <EyeOff className="h-4 w-4" />
          ) : (
            <Eye className="h-4 w-4" />
          )}
        </button>
      </div>

      <div className="flex items-start">
        <input
          type="checkbox"
          id="terms"
          checked={acceptTerms}
          onChange={(e) => setAcceptTerms(e.target.checked)}
          className="mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
        />
        <label htmlFor="terms" className="ml-2 text-sm text-gray-600">
          I agree to the{' '}
          <Link to="/terms" className="text-blue-600 hover:text-blue-500">
            Terms of Service
          </Link>{' '}
          and{' '}
          <Link to="/privacy" className="text-blue-600 hover:text-blue-500">
            Privacy Policy
          </Link>
        </label>
      </div>

      <Button
        type="submit"
        className="w-full"
        isLoading={isLoading}
        disabled={isLoading || !acceptTerms}
      >
        Create Account
      </Button>

      <div className="text-center">
        <span className="text-sm text-gray-600">
          Already have an account?{' '}
          <Link
            to="/auth/login"
            className="text-blue-600 hover:text-blue-500 font-medium"
          >
            Sign in
          </Link>
        </span>
      </div>
    </form>
  );
};