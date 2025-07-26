import os
from io import BytesIO

import cloudinary
import cloudinary.uploader
from PIL import Image

from src.shared.exceptions import ValidationException


class CloudinaryService:
    """Service for handling image uploads to Cloudinary."""

    def __init__(self):
        # Configure Cloudinary (these should be environment variables)
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        )

        # Supported image formats
        self.SUPPORTED_FORMATS = {"jpg", "jpeg", "png", "webp"}
        self.MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        self.MAX_RESOLUTION = (2048, 2048)  # Max dimensions

    def validate_image(self, file_data: bytes, filename: str) -> None:
        """Validate image file before upload."""
        # Check file size
        if len(file_data) > self.MAX_FILE_SIZE:
            raise ValidationException("Image file too large (max 10MB)")

        # Check file format by extension
        file_extension = filename.lower().split(".")[-1]
        if file_extension not in self.SUPPORTED_FORMATS:
            raise ValidationException(
                f"Unsupported image format. Supported: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        # Validate image content
        try:
            with Image.open(BytesIO(file_data)) as img:
                # Check if it's actually an image
                img.verify()

                # Check resolution
                if (
                    img.size[0] > self.MAX_RESOLUTION[0]
                    or img.size[1] > self.MAX_RESOLUTION[1]
                ):
                    raise ValidationException(
                        f"Image resolution too large (max {self.MAX_RESOLUTION[0]}x{self.MAX_RESOLUTION[1]})"
                    )

        except Exception as e:
            raise ValidationException(f"Invalid image file: {str(e)}") from e

    async def upload_profile_image(
        self, user_id: int, file_data: bytes, filename: str
    ) -> str:
        """Upload a profile image to Cloudinary."""
        # Validate image first
        self.validate_image(file_data, filename)

        try:
            # Create a BytesIO object from the file data
            file_stream = BytesIO(file_data)

            # Upload to Cloudinary with transformations
            response = cloudinary.uploader.upload(
                file_stream,
                folder=f"matcha/profiles/{user_id}",
                public_id=f"{user_id}_{filename.split('.')[0]}",
                overwrite=True,
                resource_type="image",
                format="jpg",  # Convert all images to JPG
                quality="auto:good",  # Optimize quality automatically
                fetch_format="auto",  # Auto-select best format for browser
                transformation=[
                    {
                        "width": 800,
                        "height": 800,
                        "crop": "limit",
                        "quality": "auto:good",
                    }
                ],
            )

            return response["secure_url"]

        except Exception as e:
            raise ValidationException(f"Failed to upload image: {str(e)}") from e

    async def delete_image(self, image_url: str) -> bool:
        """Delete an image from Cloudinary."""
        try:
            # Extract public_id from URL
            # Cloudinary URLs have format: https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{public_id}.{format}
            url_parts = image_url.split("/")
            if "cloudinary.com" not in image_url:
                return False

            # Find the public_id (after 'upload/' and before the file extension)
            upload_index = url_parts.index("upload")
            public_id_with_version = "/".join(url_parts[upload_index + 1 :])

            # Remove version if present (starts with v followed by numbers)
            if (
                public_id_with_version.startswith("v")
                and len(public_id_with_version.split("/")) > 1
            ):
                public_id_with_version = "/".join(public_id_with_version.split("/")[1:])

            # Remove file extension
            public_id = public_id_with_version.rsplit(".", 1)[0]

            # Delete from Cloudinary
            result = cloudinary.uploader.destroy(public_id, resource_type="image")

            return result.get("result") == "ok"

        except Exception:
            # If deletion fails, log it but don't raise exception
            # The image URL will be removed from database anyway
            return False

    def get_transformed_url(
        self, image_url: str, width: int | None = None, height: int | None = None
    ) -> str:
        """Get a transformed version of an image URL."""
        if "cloudinary.com" not in image_url:
            return image_url

        try:
            transformations = []
            if width or height:
                transform = {"crop": "limit"}
                if width:
                    transform["width"] = width
                if height:
                    transform["height"] = height
                transformations.append(transform)

            if transformations:
                # Use Cloudinary's URL transformation
                from cloudinary import CloudinaryImage

                # Extract public_id from URL
                url_parts = image_url.split("/")
                upload_index = url_parts.index("upload")
                public_id_with_version = "/".join(url_parts[upload_index + 1 :])

                # Remove version if present
                if (
                    public_id_with_version.startswith("v")
                    and len(public_id_with_version.split("/")) > 1
                ):
                    public_id_with_version = "/".join(
                        public_id_with_version.split("/")[1:]
                    )

                # Remove file extension
                public_id = public_id_with_version.rsplit(".", 1)[0]

                # Generate new URL with transformations
                return CloudinaryImage(public_id).build_url(
                    transformation=transformations
                )

            return image_url

        except Exception:
            # If transformation fails, return original URL
            return image_url
