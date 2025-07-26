import { apiClient } from '../api/fetchClient';

export interface ProfileCreateData {
  age: number;
  gender: 'male' | 'female' | 'non_binary' | 'other';
  sexual_preference: 'heterosexual' | 'homosexual' | 'bisexual' | 'pansexual' | 'asexual';
  biography: string;
  latitude?: number;
  longitude?: number;
  city?: string;
  country?: string;
  interests?: string[];
}

export interface ProfileUpdateData extends Partial<ProfileCreateData> {}

export interface LocationData {
  latitude: number;
  longitude: number;
  city?: string;
  country?: string;
}

export interface ProfileData {
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

export interface ImageUploadResponse {
  image_url: string;
}

class ProfileService {
  async createProfile(data: ProfileCreateData): Promise<ProfileData> {
    return apiClient.post('/profile', data);
  }

  async getMyProfile(): Promise<ProfileData> {
    return apiClient.get('/profile/me');
  }

  async updateProfile(data: ProfileUpdateData): Promise<ProfileData> {
    return apiClient.put('/profile/me', data);
  }

  async getUserProfile(userId: number): Promise<ProfileData> {
    return apiClient.get(`/profile/${userId}`);
  }

  async uploadImage(file: File): Promise<ImageUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    return apiClient.post('/profile/images', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }

  async deleteImage(imageUrl: string): Promise<void> {
    const params = new URLSearchParams({ image_url: imageUrl });
    return apiClient.delete(`/profile/images?${params}`);
  }

  async reorderImages(imageUrls: string[]): Promise<void> {
    return apiClient.put('/profile/images/order', { image_urls: imageUrls });
  }
}

export const profileService = new ProfileService();