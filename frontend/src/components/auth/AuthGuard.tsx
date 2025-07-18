import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

interface AuthGuardProps {
  children: React.ReactNode;
  requireEmailVerification?: boolean;
  fallback?: React.ReactNode;
}

export const AuthGuard: React.FC<AuthGuardProps> = ({ 
  children, 
  requireEmailVerification = false,
  fallback 
}) => {
  const { isAuthenticated, isLoading, user, isEmailVerified } = useAuth();
  const location = useLocation();

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      fallback || (
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated || !user) {
    return <Navigate to="/auth/login" state={{ from: location }} replace />;
  }

  // Redirect to email verification if required and not verified
  if (requireEmailVerification && !isEmailVerified) {
    return <Navigate to="/auth/verify-email" replace />;
  }

  // User is authenticated and meets requirements
  return <>{children}</>;
};

// Higher-order component version for easier usage
export const withAuthGuard = <P extends object>(
  Component: React.ComponentType<P>,
  options?: Omit<AuthGuardProps, 'children'>
) => {
  return (props: P) => (
    <AuthGuard {...options}>
      <Component {...props} />
    </AuthGuard>
  );
};