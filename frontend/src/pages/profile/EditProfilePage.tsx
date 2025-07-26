import { useEffect } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { useProfileStore } from '../../stores/profileStore';
import { useAuthStore } from '../../stores/authStore';
import { useToast } from '../../hooks/use-toast';
import { ProfileForm } from '../../components/profile/ProfileForm';
import type { ProfileFormData } from '../../types';

export default function EditProfilePage() {
  const navigate = useNavigate();
  const { profile, isLoading, getProfile, updateProfile } = useProfileStore();
  const { isAuthenticated } = useAuthStore();
  const { toast } = useToast();

  useEffect(() => {
    if (isAuthenticated) {
      getProfile();
    }
  }, [isAuthenticated, getProfile]);

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }

  const handleSubmit = async (data: ProfileFormData) => {
    try {
      await updateProfile(data);
      
      toast({
        title: 'Profile updated',
        description: 'Your profile has been successfully updated!',
      });
      
      navigate('/profile');
    } catch (error: any) {
      toast({
        title: 'Update failed',
        description: error.detail || 'Failed to update profile. Please try again.',
        variant: 'destructive',
      });
      throw error; // Re-throw to prevent form reset
    }
  };

  const handleCancel = () => {
    navigate('/profile');
  };

  if (isLoading && !profile) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Profile Not Found</h1>
          <p className="text-muted-foreground mb-4">
            You need to create a profile first before editing it.
          </p>
          <Button onClick={() => navigate('/profile/create')}>
            Create Profile
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center space-x-4 mb-8">
        <Button variant="ghost" size="sm" onClick={handleCancel}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Profile
        </Button>
        <div>
          <h1 className="text-3xl font-bold">Edit Profile</h1>
          <p className="text-muted-foreground">Update your profile information</p>
        </div>
      </div>

      {/* Form */}
      <div className="max-w-2xl mx-auto">
        <ProfileForm
          initialData={{
            age: profile.age,
            gender: profile.gender,
            sexual_preference: profile.sexual_preference,
            biography: profile.biography,
            latitude: profile.location?.latitude,
            longitude: profile.location?.longitude,
            city: profile.location?.city || '',
            country: profile.location?.country || '',
            interests: profile.interests,
          }}
          onSubmit={handleSubmit}
          isLoading={isLoading}
          submitLabel="Update Profile"
        />
      </div>
    </div>
  );
}