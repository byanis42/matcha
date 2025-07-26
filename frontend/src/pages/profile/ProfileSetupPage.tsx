import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Badge } from '../../components/ui/badge';
import { Progress } from '../../components/ui/progress';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '../../components/ui/form';
import { ImageUploader } from '../../components/profile/ImageUploader';
import { useToast } from '../../hooks/use-toast';
import { useAuth } from '../../hooks/useAuth';
import { profileService } from '../../services/profile';
import { GENDER_OPTIONS, SEXUAL_PREFERENCE_OPTIONS, COMMON_INTERESTS } from '../../types/profile';
import { MapPin, User, Heart, FileText, Camera, CheckCircle } from 'lucide-react';

const profileSchema = z.object({
  age: z.number().min(18, 'Must be at least 18 years old').max(100, 'Invalid age'),
  gender: z.string().min(1, 'Gender is required'),
  sexual_preference: z.string().min(1, 'Sexual preference is required'),
  biography: z.string().min(10, 'Biography must be at least 10 characters'),
  latitude: z.number().optional(),
  longitude: z.number().optional(),
  city: z.string().optional(),
  country: z.string().optional(),
  interests: z.array(z.string()).min(1, 'At least one interest is required'),
});

type ProfileFormData = z.infer<typeof profileSchema>;

const STEPS = [
  { id: 1, title: 'Personal Info', icon: User, description: 'Tell us about yourself' },
  { id: 2, title: 'Interests', icon: Heart, description: 'What do you enjoy?' },
  { id: 3, title: 'Biography', icon: FileText, description: 'Share your story' },
  { id: 4, title: 'Photos', icon: Camera, description: 'Add your best photos' },
  { id: 5, title: 'Location', icon: MapPin, description: 'Where are you?' },
  { id: 6, title: 'Complete', icon: CheckCircle, description: 'All done!' },
];

export function ProfileSetupPage() {
  const [currentStep, setCurrentStep] = useState(1);
  const [uploadedImages, setUploadedImages] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();
  const { user } = useAuth();

  const form = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      age: 18,
      gender: '',
      sexual_preference: '',
      biography: '',
      interests: [],
    },
  });

  const { watch, setValue } = form;
  const watchedInterests = watch('interests');
  const watchedBiography = watch('biography');
  const watchedAge = watch('age');
  const watchedGender = watch('gender');
  const watchedSexualPreference = watch('sexual_preference');

  // Get user's location on component mount
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setValue('latitude', position.coords.latitude);
          setValue('longitude', position.coords.longitude);
        },
        (error) => {
          console.warn('Geolocation error:', error);
          // Continue without location - it's optional
        }
      );
    }
  }, [setValue]);

  const progress = (currentStep / STEPS.length) * 100;

  const addInterest = (interest: string) => {
    if (!watchedInterests.includes(interest) && watchedInterests.length < 10) {
      setValue('interests', [...watchedInterests, interest]);
    }
  };

  const removeInterest = (interest: string) => {
    setValue('interests', watchedInterests.filter(i => i !== interest));
  };

  const handleImageUpload = async (file: File): Promise<string> => {
    if (!user) throw new Error('User not authenticated');
    const response = await profileService.uploadImage(file);
    return response.image_url;
  };

  const handleImageDelete = async (imageUrl: string): Promise<void> => {
    await profileService.deleteImage(imageUrl);
  };

  const handleImageReorder = async (imageUrls: string[]): Promise<void> => {
    await profileService.reorderImages(imageUrls);
  };

  const nextStep = () => {
    if (currentStep < STEPS.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const canProceedFromStep = (step: number): boolean => {
    switch (step) {
      case 1:
        return !!watchedAge && watchedAge >= 18 && !!watchedGender && !!watchedSexualPreference;
      case 2:
        return watchedInterests.length > 0;
      case 3:
        return !!watchedBiography && watchedBiography.length >= 10;
      case 4:
        return uploadedImages.length > 0;
      case 5:
        return true; // Location is optional
      default:
        return true;
    }
  };

  const onSubmit = async (data: ProfileFormData) => {
    if (!user) return;

    setIsSubmitting(true);
    try {
      await profileService.createProfile({
        ...data,
        gender: data.gender as 'male' | 'female' | 'non_binary' | 'other',
        sexual_preference: data.sexual_preference as 'heterosexual' | 'homosexual' | 'bisexual' | 'pansexual' | 'asexual',
      });

      toast({
        title: 'Profile created successfully!',
        description: 'Welcome to Matcha! Your profile is now complete.',
      });

      navigate('/dashboard');
    } catch (error: any) {
      toast({
        title: 'Error creating profile',
        description: error.detail || 'Failed to create profile',
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <FormField
              control={form.control}
              name="age"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Age</FormLabel>
                  <FormControl>
                    <Input 
                      type="number" 
                      min="18" 
                      max="100" 
                      {...field}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => field.onChange(parseInt(e.target.value) || 18)}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="gender"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Gender</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select your gender" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {GENDER_OPTIONS.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="sexual_preference"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Sexual Preference</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select your preference" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {SEXUAL_PREFERENCE_OPTIONS.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div>
              <Label className="text-base font-medium">Choose your interests</Label>
              <p className="text-sm text-gray-600 mt-1">Select up to 10 interests that describe you</p>
            </div>
            
            <div className="flex flex-wrap gap-2">
              {COMMON_INTERESTS.map((interest) => (
                <Badge
                  key={interest}
                  variant={watchedInterests.includes(interest) ? "default" : "outline"}
                  className="cursor-pointer hover:bg-primary/80"
                  onClick={() => {
                    if (watchedInterests.includes(interest)) {
                      removeInterest(interest);
                    } else {
                      addInterest(interest);
                    }
                  }}
                >
                  {interest}
                </Badge>
              ))}
            </div>

            <div className="flex flex-wrap gap-2 mt-4">
              {watchedInterests.map((interest) => (
                <Badge
                  key={interest}
                  variant="default"
                  className="cursor-pointer"
                  onClick={() => removeInterest(interest)}
                >
                  {interest} ×
                </Badge>
              ))}
            </div>

            <p className="text-sm text-gray-500">
              Selected: {watchedInterests.length}/10
            </p>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <FormField
              control={form.control}
              name="biography"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Tell us about yourself</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Share something interesting about yourself..."
                      className="min-h-[120px]"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                  <p className="text-sm text-gray-500">
                    {field.value?.length || 0}/500 characters
                  </p>
                </FormItem>
              )}
            />
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <div>
              <Label className="text-base font-medium">Add your photos</Label>
              <p className="text-sm text-gray-600 mt-1">Add at least one photo to continue</p>
            </div>
            
            <ImageUploader
              images={uploadedImages}
              onImagesChange={setUploadedImages}
              onUpload={handleImageUpload}
              onDelete={handleImageDelete}
              onReorder={handleImageReorder}
              maxImages={5}
            />
          </div>
        );

      case 5:
        return (
          <div className="space-y-6">
            <div>
              <Label className="text-base font-medium">Location</Label>
              <p className="text-sm text-gray-600 mt-1">
                We'll use your location to find matches nearby. You can adjust this anytime.
              </p>
            </div>

            <FormField
              control={form.control}
              name="city"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>City (Optional)</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter your city" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="country"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Country (Optional)</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter your country" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
        );

      case 6:
        return (
          <div className="text-center space-y-6">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold">Profile Complete!</h3>
              <p className="text-gray-600 mt-2">
                You're all set! Click below to start exploring Matcha.
              </p>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Complete Your Profile</CardTitle>
                <CardDescription>
                  Step {currentStep} of {STEPS.length}: {STEPS[currentStep - 1]?.description}
                </CardDescription>
              </div>
              <div className="text-sm text-gray-500">
                {Math.round(progress)}% complete
              </div>
            </div>
            <Progress value={progress} className="mt-4" />
          </CardHeader>

          <CardContent>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                {renderStepContent()}

                <div className="flex justify-between pt-6">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={prevStep}
                    disabled={currentStep === 1}
                  >
                    Previous
                  </Button>

                  {currentStep < STEPS.length ? (
                    <Button
                      type="button"
                      onClick={nextStep}
                      disabled={!canProceedFromStep(currentStep)}
                    >
                      Next
                    </Button>
                  ) : (
                    <Button
                      type="submit"
                      disabled={isSubmitting || !canProceedFromStep(currentStep)}
                    >
                      {isSubmitting ? 'Creating Profile...' : 'Complete Profile'}
                    </Button>
                  )}
                </div>
              </form>
            </Form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}