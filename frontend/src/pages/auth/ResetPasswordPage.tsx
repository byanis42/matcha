import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { authService } from '../../services/auth/authService';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';

interface ResetPasswordForm {
  password: string;
  confirmPassword: string;
}

export const ResetPasswordPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [isValid, setIsValid] = useState(true);

  const token = searchParams.get('token');
  const email = searchParams.get('email');

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<ResetPasswordForm>();

  const password = watch('password');

  useEffect(() => {
    if (!token || !email) {
      setIsValid(false);
    }
  }, [token, email]);

  const onSubmit = async (data: ResetPasswordForm) => {
    if (!token || !email) return;

    setIsLoading(true);
    try {
      await authService.confirmPasswordReset({
        email,
        token,
        new_password: data.password,
        confirm_password: data.confirmPassword,
      });

      toast.success('Password reset successfully!');
      navigate('/auth/login', { replace: true });
    } catch (error: any) {
      toast.error(error.detail || 'Failed to reset password');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isValid) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-extrabold text-gray-900">Matcha</h2>
          </div>

          <Card className="py-8 px-6">
            <div className="text-center">
              <div className="rounded-full bg-red-100 p-3 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.996-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Invalid Reset Link
              </h1>
              <p className="text-gray-600 mb-6">
                This password reset link is invalid or has expired.
              </p>
              <Link
                to="/auth/forgot-password"
                className="text-pink-600 hover:text-pink-500 font-medium"
              >
                Request New Reset Link
              </Link>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-extrabold text-gray-900">Matcha</h2>
          <p className="mt-2 text-sm text-gray-600">
            Create your new password
          </p>
        </div>

        <Card className="py-8 px-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                New Password
              </label>
              <Input
                {...register('password', {
                  required: 'Password is required',
                  minLength: {
                    value: 8,
                    message: 'Password must be at least 8 characters',
                  },
                  pattern: {
                    value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
                    message: 'Password must contain uppercase, lowercase, and number',
                  },
                })}
                type="password"
                placeholder="Enter new password"
                error={errors.password?.message}
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
                Confirm Password
              </label>
              <Input
                {...register('confirmPassword', {
                  required: 'Please confirm your password',
                  validate: (value) =>
                    value === password || 'Passwords do not match',
                })}
                type="password"
                placeholder="Confirm new password"
                error={errors.confirmPassword?.message}
              />
            </div>

            <Button
              type="submit"
              className="w-full bg-pink-600 hover:bg-pink-700"
              disabled={isLoading}
            >
              {isLoading ? 'Resetting...' : 'Reset Password'}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm">
            <Link
              to="/auth/login"
              className="text-pink-600 hover:text-pink-500 font-medium"
            >
              Back to Login
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
};