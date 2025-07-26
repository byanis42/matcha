export interface ProfileFormData {
  age: number;
  gender: 'male' | 'female' | 'non_binary' | 'other';
  sexual_preference: 'heterosexual' | 'homosexual' | 'bisexual' | 'pansexual' | 'asexual';
  biography: string;
  latitude?: number;
  longitude?: number;
  city?: string;
  country?: string;
  interests: string[];
}

export interface LocationData {
  latitude: number;
  longitude: number;
  city?: string;
  country?: string;
}

export interface UserProfile {
  id: number;
  user_id: number;
  age: number;
  gender: 'male' | 'female' | 'non_binary' | 'other';
  sexual_preference: 'heterosexual' | 'homosexual' | 'bisexual' | 'pansexual' | 'asexual';
  biography: string;
  location?: LocationData;
  fame_rating: number;
  interests: string[];
  pictures: string[];
  profile_completed: boolean;
  created_at?: string;
  updated_at?: string;
}

export const GENDER_OPTIONS = [
  { value: 'male', label: 'Male' },
  { value: 'female', label: 'Female' },
  { value: 'non_binary', label: 'Non-binary' },
  { value: 'other', label: 'Other' },
] as const;

export const SEXUAL_PREFERENCE_OPTIONS = [
  { value: 'heterosexual', label: 'Heterosexual' },
  { value: 'homosexual', label: 'Homosexual' },
  { value: 'bisexual', label: 'Bisexual' },
  { value: 'pansexual', label: 'Pansexual' },
  { value: 'asexual', label: 'Asexual' },
] as const;

export const COMMON_INTERESTS = [
  'Travel', 'Photography', 'Music', 'Movies', 'Reading', 'Cooking',
  'Fitness', 'Gaming', 'Art', 'Dancing', 'Hiking', 'Swimming',
  'Yoga', 'Technology', 'Fashion', 'Sports', 'Nature', 'Coffee',
  'Wine', 'Pets', 'Languages', 'Writing', 'Design', 'Comedy',
  'Theater', 'Museums', 'Concerts', 'Food', 'Science', 'History'
] as const;