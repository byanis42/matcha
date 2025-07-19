import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { authService } from '../../services/auth/authService';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';

export const VerifyEmailPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'verifying' | 'success' | 'error' | 'invalid'>('verifying');
  const [message, setMessage] = useState('');

  const token = searchParams.get('token');
  const email = searchParams.get('email');

  useEffect(() => {
    let isCancelled = false;
    
    const verifyEmail = async () => {
      // Check if we have the required parameters
      if (!token || !email) {
        if (!isCancelled) {
          setStatus('invalid');
          setMessage('Invalid verification link. Missing token or email.');
        }
        return;
      }

      try {
        if (!isCancelled) {
          setStatus('verifying');
        }
        
        // Call the verification API
        const response = await authService.verifyEmail({ token });
        
        if (!isCancelled) {
          setStatus('success');
          setMessage(response.message || 'Email verified successfully!');
          
          // Show success toast
          toast.success('Email verified successfully! You can now log in.');
          
          // Redirect to login page after 3 seconds
          setTimeout(() => {
            if (!isCancelled) {
              navigate('/auth/login', { replace: true });
            }
          }, 3000);
        }
        
      } catch (error: any) {
        if (!isCancelled) {
          setStatus('error');
          
          // Handle specific error messages
          if (error.detail?.includes('already been used')) {
            setMessage('This verification link has already been used. Your email is already verified.');
          } else if (error.detail?.includes('Invalid') || error.detail?.includes('expired')) {
            setMessage('This verification link is invalid or has expired. Please request a new verification email.');
          } else {
            setMessage(error.detail || 'Failed to verify email. Please try again.');
          }
          
          toast.error('Email verification failed');
        }
      }
    };

    verifyEmail();
    
    // Cleanup function to prevent state updates if component unmounts
    return () => {
      isCancelled = true;
    };
  }, [token, email, navigate]);

  const renderContent = () => {
    switch (status) {
      case 'verifying':
        return (
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-pink-600 mx-auto mb-4"></div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Verifying Your Email
            </h1>
            <p className="text-gray-600">
              Please wait while we verify your email address...
            </p>
          </div>
        );

      case 'success':
        return (
          <div className="text-center">
            <div className="rounded-full bg-green-100 p-3 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Email Verified!
            </h1>
            <p className="text-gray-600 mb-6">
              {message}
            </p>
            <p className="text-sm text-gray-500 mb-4">
              You will be redirected to the login page in a few seconds...
            </p>
            <Button
              onClick={() => navigate('/auth/login', { replace: true })}
              className="bg-pink-600 hover:bg-pink-700"
            >
              Go to Login
            </Button>
          </div>
        );

      case 'error':
        const isAlreadyUsed = message.includes('already been used');
        return (
          <div className="text-center">
            <div className={`rounded-full p-3 w-16 h-16 mx-auto mb-4 flex items-center justify-center ${
              isAlreadyUsed ? 'bg-green-100' : 'bg-red-100'
            }`}>
              {isAlreadyUsed ? (
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              ) : (
                <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              )}
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              {isAlreadyUsed ? 'Already Verified' : 'Verification Failed'}
            </h1>
            <p className="text-gray-600 mb-6">
              {message}
            </p>
            <div className="space-y-3">
              {isAlreadyUsed ? (
                <Button
                  onClick={() => navigate('/auth/login', { replace: true })}
                  className="bg-pink-600 hover:bg-pink-700"
                >
                  Go to Login
                </Button>
              ) : (
                <>
                  <Button
                    onClick={() => window.location.reload()}
                    variant="outline"
                    className="mr-3"
                  >
                    Try Again
                  </Button>
                  <Link
                    to="/auth/register"
                    className="text-pink-600 hover:text-pink-500 font-medium"
                  >
                    Register Again
                  </Link>
                </>
              )}
            </div>
          </div>
        );

      case 'invalid':
        return (
          <div className="text-center">
            <div className="rounded-full bg-yellow-100 p-3 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <svg className="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.996-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Invalid Verification Link
            </h1>
            <p className="text-gray-600 mb-6">
              {message}
            </p>
            <div className="space-y-3">
              <Link
                to="/auth/register"
                className="inline-block bg-pink-600 text-white px-6 py-2 rounded-lg hover:bg-pink-700"
              >
                Register Again
              </Link>
              <p className="text-sm text-gray-500">
                Already have an account?{' '}
                <Link to="/auth/login" className="text-pink-600 hover:text-pink-500">
                  Sign in
                </Link>
              </p>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-extrabold text-gray-900">
            Matcha
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Email Verification
          </p>
        </div>

        <Card className="py-8 px-6">
          {renderContent()}
        </Card>

        <div className="mt-8 text-center">
          <Link
            to="/auth/login"
            className="text-sm text-pink-600 hover:text-pink-500"
          >
            Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
};