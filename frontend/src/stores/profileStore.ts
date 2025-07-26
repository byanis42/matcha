import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { profileService, ProfileData, ProfileCreateData, ProfileUpdateData } from '../services/profile';

interface ProfileState {
  profile: ProfileData | null;
  isLoading: boolean;
  error: string | null;
}

interface ProfileActions {
  createProfile: (data: ProfileCreateData) => Promise<void>;
  getProfile: () => Promise<void>;
  updateProfile: (data: ProfileUpdateData) => Promise<void>;
  getUserProfile: (userId: number) => Promise<ProfileData>;
  uploadImage: (file: File) => Promise<string>;
  deleteImage: (imageUrl: string) => Promise<void>;
  reorderImages: (imageUrls: string[]) => Promise<void>;
  clearProfile: () => void;
  clearError: () => void;
}

interface ProfileStore extends ProfileState, ProfileActions {}

const initialState: ProfileState = {
  profile: null,
  isLoading: false,
  error: null,
};

export const useProfileStore = create<ProfileStore>()(
  persist(
    (set, get) => ({
      ...initialState,

      createProfile: async (data: ProfileCreateData) => {
        set({ isLoading: true, error: null });
        
        try {
          const profile = await profileService.createProfile(data);
          
          set({
            profile,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Failed to create profile',
          });
          throw error;
        }
      },

      getProfile: async () => {
        set({ isLoading: true, error: null });
        
        try {
          const profile = await profileService.getMyProfile();
          
          set({
            profile,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Failed to get profile',
          });
          throw error;
        }
      },

      updateProfile: async (data: ProfileUpdateData) => {
        set({ isLoading: true, error: null });
        
        try {
          const profile = await profileService.updateProfile(data);
          
          set({
            profile,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Failed to update profile',
          });
          throw error;
        }
      },

      getUserProfile: async (userId: number) => {
        // This doesn't update the store's profile, just returns the data
        return await profileService.getUserProfile(userId);
      },

      uploadImage: async (file: File) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await profileService.uploadImage(file);
          
          // Optimistically update the profile
          const currentProfile = get().profile;
          if (currentProfile) {
            const updatedProfile = {
              ...currentProfile,
              pictures: [...currentProfile.pictures, response.image_url],
            };
            
            set({
              profile: updatedProfile,
              isLoading: false,
              error: null,
            });
          } else {
            set({ isLoading: false });
          }
          
          return response.image_url;
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Failed to upload image',
          });
          throw error;
        }
      },

      deleteImage: async (imageUrl: string) => {
        set({ isLoading: true, error: null });
        
        try {
          await profileService.deleteImage(imageUrl);
          
          // Optimistically update the profile
          const currentProfile = get().profile;
          if (currentProfile) {
            const updatedProfile = {
              ...currentProfile,
              pictures: currentProfile.pictures.filter(url => url !== imageUrl),
            };
            
            set({
              profile: updatedProfile,
              isLoading: false,
              error: null,
            });
          } else {
            set({ isLoading: false });
          }
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Failed to delete image',
          });
          throw error;
        }
      },

      reorderImages: async (imageUrls: string[]) => {
        set({ isLoading: true, error: null });
        
        try {
          await profileService.reorderImages(imageUrls);
          
          // Optimistically update the profile
          const currentProfile = get().profile;
          if (currentProfile) {
            const updatedProfile = {
              ...currentProfile,
              pictures: imageUrls,
            };
            
            set({
              profile: updatedProfile,
              isLoading: false,
              error: null,
            });
          } else {
            set({ isLoading: false });
          }
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Failed to reorder images',
          });
          throw error;
        }
      },

      clearProfile: () => {
        set({
          ...initialState,
        });
      },

      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: 'profile-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        profile: state.profile,
      }),
    }
  )
);