import { MapPin, Heart, Star, Calendar } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/Button';
import { UserProfile, GENDER_OPTIONS, SEXUAL_PREFERENCE_OPTIONS } from '../../types';

interface UserProfileViewerProps {
  profile: UserProfile;
  onLike?: () => void;
  onSuperLike?: () => void;
  onPass?: () => void;
  showActions?: boolean;
  isLoading?: boolean;
}

export function UserProfileViewer({
  profile,
  onLike,
  onSuperLike,
  onPass,
  showActions = false,
  isLoading = false,
}: UserProfileViewerProps) {
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

  const fameRating = getFameRatingLevel(profile.fame_rating);

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Photos */}
          {profile.pictures.length > 0 && (
            <Card>
              <CardContent className="p-0">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-6">
                  {profile.pictures.map((imageUrl, index) => (
                    <div
                      key={imageUrl}
                      className={`relative overflow-hidden rounded-lg ${
                        index === 0 ? 'md:col-span-2 aspect-[16/9]' : 'aspect-square'
                      }`}
                    >
                      <img
                        src={imageUrl}
                        alt={`Profile photo ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                      {index === 0 && (
                        <div className="absolute bottom-4 left-4 bg-primary text-primary-foreground text-sm px-3 py-1 rounded">
                          Main Photo
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Biography */}
          <Card>
            <CardHeader>
              <CardTitle>About</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                {profile.biography}
              </p>
            </CardContent>
          </Card>

          {/* Interests */}
          {profile.interests.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Interests</CardTitle>
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
                      : profile.location.city || profile.location.country || 'Location available'}
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
              </div>
            </CardContent>
          </Card>

          {/* Actions */}
          {showActions && (
            <Card>
              <CardHeader>
                <CardTitle>Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button
                  onClick={onSuperLike}
                  disabled={isLoading}
                  className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                  size="lg"
                >
                  ⭐ Super Like
                </Button>
                
                <Button
                  onClick={onLike}
                  disabled={isLoading}
                  className="w-full"
                  size="lg"
                  variant="default"
                >
                  ❤️ Like
                </Button>
                
                <Button
                  onClick={onPass}
                  disabled={isLoading}
                  className="w-full"
                  size="lg"
                  variant="outline"
                >
                  👋 Pass
                </Button>
              </CardContent>
            </Card>
          )}

          {/* Profile Stats */}
          <Card>
            <CardHeader>
              <CardTitle>Profile Stats</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Photos</span>
                  <span className="text-sm text-muted-foreground">
                    {profile.pictures.length}/5
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm">Interests</span>
                  <span className="text-sm text-muted-foreground">
                    {profile.interests.length}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm">Profile Status</span>
                  {profile.profile_completed ? (
                    <Badge variant="default" className="text-xs">Complete</Badge>
                  ) : (
                    <Badge variant="secondary" className="text-xs">Incomplete</Badge>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}