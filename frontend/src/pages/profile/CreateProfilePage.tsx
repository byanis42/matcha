import { useNavigate, Navigate } from 'react-router-dom';
import { useProfileStore } from '../../stores/profileStore';
import { useAuthStore } from '../../stores/authStore';
import { useToast } from '../../hooks/use-toast';
import { ProfileForm } from '../../components/profile/ProfileForm';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import type { ProfileFormData } from '../../types';

export default function CreateProfilePage() {
  const navigate = useNavigate();
  const { createProfile, isLoading } = useProfileStore();
  const { user, isAuthenticated } = useAuthStore();
  const { toast } = useToast();

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }

  const handleSubmit = async (data: ProfileFormData) => {
    try {
      await createProfile(data);
      
      toast({
        title: 'Profile created!',
        description: 'Welcome to Matcha! Your profile has been created successfully.',
      });
      
      navigate('/profile');
    } catch (error: any) {
      toast({
        title: 'Creation failed',
        description: error.detail || 'Failed to create profile. Please try again.',
        variant: 'destructive',
      });
      throw error; // Re-throw to prevent form reset
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4">Welcome to Matcha!</h1>
        <p className="text-xl text-muted-foreground mb-2">
          Let's create your dating profile
        </p>
        <p className="text-muted-foreground">
          Fill out your information to start connecting with people
        </p>
      </div>

      {/* Welcome Card */}
      <Card className="max-w-2xl mx-auto mb-8 bg-gradient-to-r from-primary/10 to-purple-500/10 border-primary/20">
        <CardHeader>
          <CardTitle className="text-center">Hello, {user?.first_name}! 👋</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center space-y-2">
            <p className="text-sm text-muted-foreground">
              Your profile helps others get to know you better. Be authentic and showcase your personality!
            </p>
            <div className="flex justify-center space-x-6 text-sm mt-4">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>Be yourself</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span>Add great photos</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span>Share your interests</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Form */}
      <div className="max-w-2xl mx-auto">
        <ProfileForm
          onSubmit={handleSubmit}
          isLoading={isLoading}
          submitLabel="Create My Profile"
        />
      </div>

      {/* Tips */}
      <div className="max-w-2xl mx-auto mt-8">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Profile Tips 💡</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div>
                <h4 className="font-semibold mb-2">Photos</h4>
                <ul className="space-y-1 text-muted-foreground">
                  <li>• Use recent, clear photos</li>
                  <li>• Show your face and smile</li>
                  <li>• Include full-body shots</li>
                  <li>• Add photos of your hobbies</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-2">Biography</h4>
                <ul className="space-y-1 text-muted-foreground">
                  <li>• Be authentic and honest</li>
                  <li>• Mention your hobbies</li>
                  <li>• Share what you're looking for</li>
                  <li>• Keep it positive and fun</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}