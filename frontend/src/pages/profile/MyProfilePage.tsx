import { useEffect, useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { Edit, MapPin, Heart, Star, Calendar } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Badge } from '../../components/ui/badge';
import { useProfileStore } from '../../stores/profileStore';
import { useAuthStore } from '../../stores/authStore';
// import { useToast } from '../../hooks/use-toast'; // Uncomment when needed
import { ImageUploader } from '../../components/profile/ImageUploader';
import { GENDER_OPTIONS, SEXUAL_PREFERENCE_OPTIONS } from '../../types';

export default function MyProfilePage() {
  const { profile, isLoading, error, getProfile, uploadImage, deleteImage, reorderImages } = useProfileStore();
  const { isAuthenticated } = useAuthStore();
  // const { toast } = useToast(); // Uncomment when needed
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      getProfile();
    }
  }, [isAuthenticated, getProfile]);

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }

  const handleImageUpload = async (file: File): Promise<string> => {
    setIsUploading(true);
    try {
      const imageUrl = await uploadImage(file);
      return imageUrl;
    } finally {
      setIsUploading(false);
    }
  };

  const handleImageDelete = async (imageUrl: string): Promise<void> => {
    await deleteImage(imageUrl);
  };

  const handleImageReorder = async (imageUrls: string[]): Promise<void> => {
    await reorderImages(imageUrls);
  };

  const handleImagesChange = (newImages: string[]) => {
    // This is handled by the store optimistically
    console.log('Images changed:', newImages);
  };

  const getGenderLabel = (gender: string) => {
    return GENDER_OPTIONS.find(g => g.value === gender)?.label || gender;
  };

  const getPreferenceLabel = (preference: string) => {
    return SEXUAL_PREFERENCE_OPTIONS.find(p => p.value === preference)?.label || preference;
  };

  const getFameRatingLevel = (rating: number) => {
    if (rating >= 4.5) return { label: 'Legendary', color: 'bg-purple-500' };
    if (rating >= 3.5) return { label: 'Popular', color: 'bg-blue-500' };
    if (rating >= 2.5) return { label: 'Rising', color: 'bg-green-500' };
    if (rating >= 1.5) return { label: 'Known', color: 'bg-yellow-500' };
    return { label: 'Newcomer', color: 'bg-gray-500' };
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

  if (error && !profile) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-destructive mb-4">{error}</p>
            <Link to="/profile/create">
              <Button>Create Your Profile</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Complete Your Profile</CardTitle>
          </CardHeader>
          <CardContent className="text-center py-8">
            <p className="mb-4">You haven't created your profile yet. Let's get started!</p>
            <Link to="/profile/create">
              <Button size="lg">Create Profile</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  const fameRating = getFameRatingLevel(profile.fame_rating);

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">My Profile</h1>
          <p className="text-muted-foreground">Manage your dating profile</p>
        </div>
        <Link to="/profile/edit">
          <Button>
            <Edit className="mr-2 h-4 w-4" />
            Edit Profile
          </Button>
        </Link>
      </div>

      {/* Profile Completion Warning */}
      {!profile.profile_completed && (
        <Card className="border-yellow-200 bg-yellow-50">
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse" />
              <p className="text-yellow-700">
                Your profile is incomplete. Complete it to start matching!
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Profile Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Photos */}
          <Card>
            <CardHeader>
              <CardTitle>Photos</CardTitle>
            </CardHeader>
            <CardContent>
              <ImageUploader
                images={profile.pictures}
                onImagesChange={handleImagesChange}
                onUpload={handleImageUpload}
                onDelete={handleImageDelete}
                onReorder={handleImageReorder}
                maxImages={5}
                disabled={isUploading}
              />
            </CardContent>
          </Card>

          {/* Biography */}
          <Card>
            <CardHeader>
              <CardTitle>About Me</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 leading-relaxed">
                {profile.biography || 'No biography provided yet.'}
              </p>
            </CardContent>
          </Card>

          {/* Interests */}
          {profile.interests.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>My Interests</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {profile.interests.map((interest) => (
                    <Badge key={interest} variant="secondary">
                      {interest}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Basic Info */}
          <Card>
            <CardHeader>
              <CardTitle>Profile Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-2">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <span>{profile.age} years old</span>
              </div>

              <div className="flex items-center space-x-2">
                <Heart className="h-4 w-4 text-muted-foreground" />
                <span>{getGenderLabel(profile.gender)}</span>
              </div>

              <div className="flex items-center space-x-2">
                <Heart className="h-4 w-4 text-muted-foreground" />
                <span>Looking for {getPreferenceLabel(profile.sexual_preference)}</span>
              </div>

              {profile.location && (
                <div className="flex items-center space-x-2">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <span>
                    {profile.location.city && profile.location.country
                      ? `${profile.location.city}, ${profile.location.country}`
                      : profile.location.city || profile.location.country || 'Location set'}
                  </span>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Fame Rating */}
          <Card>
            <CardHeader>
              <CardTitle>Fame Rating</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${fameRating.color}`} />
                  <span className="font-medium">{fameRating.label}</span>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Star className="h-4 w-4 text-yellow-500" />
                  <span className="text-2xl font-bold">{profile.fame_rating.toFixed(1)}</span>
                  <span className="text-muted-foreground">/ 5.0</span>
                </div>

                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(profile.fame_rating / 5) * 100}%` }}
                  />
                </div>
                
                <p className="text-sm text-muted-foreground">
                  Your popularity score based on profile views, likes, and activity
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Profile Status */}
          <Card>
            <CardHeader>
              <CardTitle>Profile Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Profile Complete</span>
                  {profile.profile_completed ? (
                    <Badge variant="default">Complete</Badge>
                  ) : (
                    <Badge variant="secondary">Incomplete</Badge>
                  )}
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm">Photos</span>
                  <span className="text-sm text-muted-foreground">
                    {profile.pictures.length}/5
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm">Interests</span>
                  <span className="text-sm text-muted-foreground">
                    {profile.interests.length}/10
                  </span>
                </div>

                {profile.created_at && (
                  <div className="pt-3 border-t">
                    <p className="text-xs text-muted-foreground">
                      Profile created {new Date(profile.created_at).toLocaleDateString()}
                    </p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}