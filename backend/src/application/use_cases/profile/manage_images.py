from src.core.repositories.unit_of_work import AbstractUnitOfWork
from src.infrastructure.external.storage.cloudinary_service import CloudinaryService
from src.shared.exceptions import (
    ForbiddenException,
    NotFoundException,
    ValidationException,
)


class UploadProfileImageUseCase:
    """Use case for uploading profile images."""

    def __init__(self, uow: AbstractUnitOfWork, cloudinary_service: CloudinaryService):
        self.uow = uow
        self.cloudinary_service = cloudinary_service

    async def execute(self, user_id: int, file_data: bytes, filename: str) -> str:
        """Upload a profile image."""
        async with self.uow:
            # Get user profile
            profile = await self.uow.profiles.get_by_user_id(user_id)
            if profile is None:
                raise NotFoundException("Profile not found")

            # Check if user can add more pictures
            if len(profile.pictures) >= 5:
                raise ValidationException("Maximum 5 pictures allowed")

            # Upload to Cloudinary
            image_url = await self.cloudinary_service.upload_profile_image(
                user_id, file_data, filename
            )

            # Add to profile
            success = await self.uow.profiles.add_picture(user_id, image_url)
            if not success:
                # If database update fails, try to delete from Cloudinary
                await self.cloudinary_service.delete_image(image_url)
                raise ValidationException("Failed to save image to profile")

            # Check if profile is now complete and update user completion status
            updated_profile = await self.uow.profiles.get_by_user_id(user_id)
            if updated_profile and updated_profile.is_complete():
                user = await self.uow.users.get_by_id(user_id)
                if user and not user.has_completed_profile:
                    user.mark_profile_completed()
                    await self.uow.users.update(user)

            await self.uow.commit()
            return image_url


class DeleteProfileImageUseCase:
    """Use case for deleting profile images."""

    def __init__(self, uow: AbstractUnitOfWork, cloudinary_service: CloudinaryService):
        self.uow = uow
        self.cloudinary_service = cloudinary_service

    async def execute(self, user_id: int, image_url: str) -> bool:
        """Delete a profile image."""
        async with self.uow:
            # Get user profile
            profile = await self.uow.profiles.get_by_user_id(user_id)
            if profile is None:
                raise NotFoundException("Profile not found")

            # Check if image belongs to user
            if image_url not in profile.pictures:
                raise ForbiddenException("Image not found in user's profile")

            # Remove from database first
            success = await self.uow.profiles.remove_picture(user_id, image_url)
            if not success:
                raise ValidationException("Failed to remove image from profile")

            # Delete from Cloudinary (don't fail if this fails)
            await self.cloudinary_service.delete_image(image_url)

            await self.uow.commit()
            return True


class ReorderProfileImagesUseCase:
    """Use case for reordering profile images."""

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, user_id: int, ordered_image_urls: list[str]) -> bool:
        """Reorder profile images."""
        async with self.uow:
            # Get user profile
            profile = await self.uow.profiles.get_by_user_id(user_id)
            if profile is None:
                raise NotFoundException("Profile not found")

            # Validate that all provided URLs belong to the user
            current_pictures = set(profile.pictures)
            provided_pictures = set(ordered_image_urls)

            if current_pictures != provided_pictures:
                raise ValidationException(
                    "Image URLs don't match user's current pictures"
                )

            # Update the order
            profile.pictures = ordered_image_urls
            await self.uow.profiles.update(profile)
            await self.uow.commit()

            return True
