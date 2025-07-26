import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Label } from '../ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '../ui/form';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../ui/select';
import { Textarea } from '../ui/textarea';
import { Badge } from '../ui/badge';
import { X } from 'lucide-react';
import { GENDER_OPTIONS, SEXUAL_PREFERENCE_OPTIONS, COMMON_INTERESTS, ProfileFormData } from '../../types';

const profileSchema = z.object({
  age: z.number().min(18, 'Must be at least 18 years old').max(100, 'Must be at most 100 years old'),
  gender: z.enum(['male', 'female', 'non_binary', 'other'], {
    required_error: 'Please select your gender',
  }),
  sexual_preference: z.enum(['heterosexual', 'homosexual', 'bisexual', 'pansexual', 'asexual'], {
    required_error: 'Please select your sexual preference',
  }),
  biography: z.string().min(10, 'Biography must be at least 10 characters').max(500, 'Biography cannot exceed 500 characters'),
  latitude: z.number().optional(),
  longitude: z.number().optional(),
  city: z.string().optional(),
  country: z.string().optional(),
  interests: z.array(z.string()).max(10, 'Maximum 10 interests allowed'),
});

interface ProfileFormProps {
  initialData?: Partial<ProfileFormData>;
  onSubmit: (data: ProfileFormData) => Promise<void>;
  isLoading?: boolean;
  submitLabel?: string;
}

export function ProfileForm({
  initialData,
  onSubmit,
  isLoading = false,
  submitLabel = 'Save Profile',
}: ProfileFormProps) {
  const [customInterest, setCustomInterest] = React.useState('');
  const [isGettingLocation, setIsGettingLocation] = React.useState(false);

  const form = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      age: initialData?.age || 18,
      gender: initialData?.gender || undefined,
      sexual_preference: initialData?.sexual_preference || undefined,
      biography: initialData?.biography || '',
      latitude: initialData?.latitude,
      longitude: initialData?.longitude,
      city: initialData?.city || '',
      country: initialData?.country || '',
      interests: initialData?.interests || [],
    },
  });

  const watchedInterests = form.watch('interests');

  const handleSubmit = async (data: ProfileFormData) => {
    try {
      await onSubmit(data);
    } catch (error) {
      // Error handling is done in the parent component
      console.error('Form submission error:', error);
    }
  };

  const addInterest = (interest: string) => {
    const currentInterests = form.getValues('interests');
    if (!currentInterests.includes(interest) && currentInterests.length < 10) {
      form.setValue('interests', [...currentInterests, interest], { shouldValidate: true });
    }
  };

  const removeInterest = (interest: string) => {
    const currentInterests = form.getValues('interests');
    form.setValue(
      'interests',
      currentInterests.filter((i) => i !== interest),
      { shouldValidate: true }
    );
  };

  const addCustomInterest = () => {
    const trimmedInterest = customInterest.trim();
    if (trimmedInterest && !watchedInterests.includes(trimmedInterest)) {
      addInterest(trimmedInterest);
      setCustomInterest('');
    }
  };

  const getLocation = async () => {
    if (!navigator.geolocation) {
      alert('Geolocation is not supported by this browser.');
      return;
    }

    setIsGettingLocation(true);
    
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        form.setValue('latitude', latitude);
        form.setValue('longitude', longitude);

        // Try to get city/country from reverse geocoding
        try {
          const response = await fetch(
            `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`
          );
          const data = await response.json();
          
          if (data.city) form.setValue('city', data.city);
          if (data.countryName) form.setValue('country', data.countryName);
        } catch (error) {
          console.error('Reverse geocoding failed:', error);
        }

        setIsGettingLocation(false);
      },
      (error) => {
        console.error('Geolocation error:', error);
        alert('Unable to get your location. Please try again or enter manually.');
        setIsGettingLocation(false);
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 }
    );
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Profile Information</CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
            {/* Basic Information */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium">Basic Information</h3>
              
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
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) => field.onChange(parseInt(e.target.value, 10))}
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
                    <Select onValueChange={field.onChange} value={field.value}>
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
                    <Select onValueChange={field.onChange} value={field.value}>
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

              <FormField
                control={form.control}
                name="biography"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Biography</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Tell others about yourself..."
                        rows={4}
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      {field.value?.length || 0}/500 characters
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            {/* Location */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium">Location</h3>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={getLocation}
                  disabled={isGettingLocation}
                >
                  {isGettingLocation ? 'Getting location...' : 'Use current location'}
                </Button>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="city"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>City</FormLabel>
                      <FormControl>
                        <Input placeholder="Your city" {...field} />
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
                      <FormLabel>Country</FormLabel>
                      <FormControl>
                        <Input placeholder="Your country" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              {form.watch('latitude') && form.watch('longitude') && (
                <p className="text-sm text-muted-foreground">
                  Coordinates: {form.watch('latitude')?.toFixed(4)}, {form.watch('longitude')?.toFixed(4)}
                </p>
              )}
            </div>

            {/* Interests */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium">Interests</h3>
              
              {/* Selected Interests */}
              {watchedInterests.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {watchedInterests.map((interest) => (
                    <Badge key={interest} variant="secondary" className="px-3 py-1">
                      {interest}
                      <X
                        className="ml-1 h-3 w-3 cursor-pointer hover:text-destructive"
                        onClick={() => removeInterest(interest)}
                      />
                    </Badge>
                  ))}
                </div>
              )}

              {/* Common Interests */}
              <div>
                <Label className="text-sm font-medium">Popular interests</Label>
                <div className="flex flex-wrap gap-2 mt-2">
                  {COMMON_INTERESTS.filter((interest) => !watchedInterests.includes(interest))
                    .slice(0, 12)
                    .map((interest) => (
                      <Badge
                        key={interest}
                        variant="outline"
                        className="cursor-pointer hover:bg-primary hover:text-primary-foreground"
                        onClick={() => addInterest(interest)}
                      >
                        {interest}
                      </Badge>
                    ))}
                </div>
              </div>

              {/* Custom Interest */}
              <div className="flex gap-2">
                <Input
                  placeholder="Add custom interest"
                  value={customInterest}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setCustomInterest(e.target.value)}
                  onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      addCustomInterest();
                    }
                  }}
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={addCustomInterest}
                  disabled={!customInterest.trim() || watchedInterests.length >= 10}
                >
                  Add
                </Button>
              </div>

              <p className="text-sm text-muted-foreground">
                {watchedInterests.length}/10 interests selected
              </p>
            </div>

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Saving...' : submitLabel}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}