from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from ....application.use_cases.profile.create_profile import CreateProfileUseCase
from ....application.use_cases.profile.get_profile import (
    GetProfileUseCase,
    GetUserProfileUseCase,
)
from ....application.use_cases.profile.manage_images import (
    DeleteProfileImageUseCase,
    ReorderProfileImagesUseCase,
    UploadProfileImageUseCase,
)
from ....application.use_cases.profile.update_profile import UpdateProfileUseCase
from ....core.entities.user import User
from ....core.repositories.unit_of_work import AbstractUnitOfWork
from ....infrastructure.external.storage.cloudinary_service import CloudinaryService
from ....shared.exceptions import (
    ForbiddenException,
    NotFoundException,
    ValidationException,
)
from ...api.dependencies import get_current_user, get_uow
from ...schemas.profile_schemas import (
    ImageReorderRequest,
    ImageUploadResponse,
    ProfileCreateRequest,
    ProfileResponse,
    ProfileUpdateRequest,
)

router = APIRouter(prefix="/profile", tags=["Profile"])


def get_cloudinary_service() -> CloudinaryService:
    """Get Cloudinary service instance."""
    return CloudinaryService()


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: ProfileCreateRequest,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """Create a new user profile."""
    try:
        use_case = CreateProfileUseCase(uow)
        profile = await use_case.execute(
            user_id=current_user.id,
            age=profile_data.age,
            gender=profile_data.gender,
            sexual_preference=profile_data.sexual_preference,
            biography=profile_data.biography,
            latitude=profile_data.latitude,
            longitude=profile_data.longitude,
            city=profile_data.city,
            country=profile_data.country,
            interests=profile_data.interests,
        )

        return ProfileResponse.from_entity(profile)

    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """Get the current user's profile."""
    try:
        use_case = GetProfileUseCase(uow)
        profile = await use_case.execute(current_user.id)

        return ProfileResponse.from_entity(profile)

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """Update the current user's profile."""
    try:
        use_case = UpdateProfileUseCase(uow)
        profile = await use_case.execute(
            user_id=current_user.id,
            age=profile_data.age,
            gender=profile_data.gender,
            sexual_preference=profile_data.sexual_preference,
            biography=profile_data.biography,
            latitude=profile_data.latitude,
            longitude=profile_data.longitude,
            city=profile_data.city,
            country=profile_data.country,
            interests=profile_data.interests,
        )

        return ProfileResponse.from_entity(profile)

    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForbiddenException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e


@router.get("/{user_id}", response_model=ProfileResponse)
async def get_user_profile(
    user_id: int,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """Get another user's profile."""
    try:
        use_case = GetUserProfileUseCase(uow)
        profile = await use_case.execute(current_user.id, user_id)

        return ProfileResponse.from_entity(profile)

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post("/images", response_model=ImageUploadResponse)
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
    cloudinary_service: CloudinaryService = Depends(get_cloudinary_service),
):
    """Upload a profile image."""
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only image files are allowed",
            )

        # Read file data
        file_data = await file.read()
        filename = file.filename or "upload.jpg"

        use_case = UploadProfileImageUseCase(uow, cloudinary_service)
        image_url = await use_case.execute(current_user.id, file_data, filename)

        return ImageUploadResponse(image_url=image_url)

    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.delete("/images")
async def delete_profile_image(
    image_url: str,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
    cloudinary_service: CloudinaryService = Depends(get_cloudinary_service),
):
    """Delete a profile image."""
    try:
        use_case = DeleteProfileImageUseCase(uow, cloudinary_service)
        success = await use_case.execute(current_user.id, image_url)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete image",
            )

        return {"message": "Image deleted successfully"}

    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForbiddenException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e


@router.put("/images/order")
async def reorder_profile_images(
    reorder_data: ImageReorderRequest,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """Reorder profile images."""
    try:
        use_case = ReorderProfileImagesUseCase(uow)
        success = await use_case.execute(current_user.id, reorder_data.image_urls)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to reorder images",
            )

        return {"message": "Images reordered successfully"}

    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
