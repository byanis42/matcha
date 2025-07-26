import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

interface ProfileCompletionGuardProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export const ProfileCompletionGuard: React.FC<ProfileCompletionGuardProps> = ({
  children,
  fallback,
}) => {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  // Show loading state while checking
  if (isLoading) {
    return (
      fallback || (
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )
    );
  }

  // If user hasn't completed their profile, redirect to profile setup
  if (user && !user.has_completed_profile) {
    return <Navigate to="/profile/setup" state={{ from: location }} replace />;
  }

  // User has completed their profile
  return <>{children}</>;
};

// Higher-order component version for easier usage
export const withProfileCompletionGuard = <P extends object>(
  Component: React.ComponentType<P>,
  options?: Omit<ProfileCompletionGuardProps, 'children'>
) => {
  return (props: P) => (
    <ProfileCompletionGuard {...options}>
      <Component {...props} />
    </ProfileCompletionGuard>
  );
};