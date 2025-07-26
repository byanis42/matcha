import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, Image as ImageIcon, AlertCircle, Edit } from 'lucide-react';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { ImageEditor } from './ImageEditor';


interface ImageUploaderProps {
  images: string[];
  onImagesChange: (images: string[]) => void;
  onUpload: (file: File) => Promise<string>;
  onDelete: (imageUrl: string) => Promise<void>;
  onReorder?: (imageUrls: string[]) => Promise<void>;
  maxImages?: number;
  disabled?: boolean;
}

export function ImageUploader({
  images,
  onImagesChange,
  onUpload,
  onDelete,
  onReorder,
  maxImages = 5,
  disabled = false,
}: ImageUploaderProps) {
  const [uploading, setUploading] = useState(false);
  const [draggedIndex, setDraggedIndex] = useState<number | null>(null);
  const [dragOverIndex, setDragOverIndex] = useState<number | null>(null);
  const [touchStartIndex, setTouchStartIndex] = useState<number | null>(null);
  const [editingImageUrl, setEditingImageUrl] = useState<string | null>(null);
  const { toast } = useToast();

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (disabled || images.length >= maxImages) {
        toast({
          title: 'Upload limit reached',
          description: `Maximum ${maxImages} images allowed`,
          variant: 'destructive',
        });
        return;
      }

      const filesToUpload = acceptedFiles.slice(0, maxImages - images.length);

      setUploading(true);
      try {
        const uploadPromises = filesToUpload.map(async (file) => {
          return await onUpload(file);
        });

        const uploadedUrls = await Promise.all(uploadPromises);
        const newImages = [...images, ...uploadedUrls];
        onImagesChange(newImages);

        toast({
          title: 'Images uploaded',
          description: `Successfully uploaded ${uploadedUrls.length} image(s)`,
        });
      } catch (error) {
        console.error('Upload failed:', error);
        toast({
          title: 'Upload failed',
          description: 'Failed to upload one or more images',
          variant: 'destructive',
        });
      } finally {
        setUploading(false);
      }
    },
    [images, maxImages, onUpload, onImagesChange, disabled, toast]
  );

  const { getRootProps, getInputProps, isDragActive, isDragAccept, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp'],
    },
    maxFiles: maxImages - images.length,
    disabled: disabled || uploading || images.length >= maxImages,
  });

  const handleDelete = async (imageUrl: string, index: number) => {
    if (disabled) return;

    try {
      await onDelete(imageUrl);
      const newImages = images.filter((_, i) => i !== index);
      onImagesChange(newImages);

      toast({
        title: 'Image deleted',
        description: 'Image has been removed from your profile',
      });
    } catch (error) {
      console.error('Delete failed:', error);
      toast({
        title: 'Delete failed',
        description: 'Failed to delete image',
        variant: 'destructive',
      });
    }
  };

  const handleDragStart = (e: React.DragEvent, index: number) => {
    if (disabled) return;
    setDraggedIndex(index);
    e.dataTransfer.effectAllowed = 'move';
    
    // Create a custom drag image with opacity
    const dragImage = e.currentTarget.cloneNode(true) as HTMLElement;
    dragImage.style.transform = 'rotate(5deg)';
    dragImage.style.opacity = '0.8';
    document.body.appendChild(dragImage);
    e.dataTransfer.setDragImage(dragImage, 50, 50);
    
    // Clean up after a short delay
    setTimeout(() => {
      if (document.body.contains(dragImage)) {
        document.body.removeChild(dragImage);
      }
    }, 0);
  };

  const handleDragOver = (e: React.DragEvent, index: number) => {
    if (disabled) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    setDragOverIndex(index);
  };

  const handleDragLeave = () => {
    setDragOverIndex(null);
  };

  const handleDrop = async (e: React.DragEvent, dropIndex: number) => {
    if (disabled || draggedIndex === null) return;
    
    e.preventDefault();
    
    if (draggedIndex === dropIndex) {
      setDraggedIndex(null);
      return;
    }

    const newImages = [...images];
    const draggedImage = newImages[draggedIndex];
    
    // Remove the dragged item
    newImages.splice(draggedIndex, 1);
    // Insert it at the new position
    newImages.splice(dropIndex, 0, draggedImage);

    onImagesChange(newImages);
    setDraggedIndex(null);
    setDragOverIndex(null);

    // Update order on server if callback provided
    if (onReorder) {
      try {
        await onReorder(newImages);
        toast({
          title: 'Images reordered',
          description: 'Image order has been updated',
        });
      } catch (error) {
        console.error('Reorder failed:', error);
        toast({
          title: 'Reorder failed',
          description: 'Failed to update image order',
          variant: 'destructive',
        });
      }
    }
  };

  // Touch event handlers for mobile support
  const handleTouchStart = (_e: React.TouchEvent, index: number) => {
    if (disabled) return;
    setTouchStartIndex(index);
    setDraggedIndex(index);
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    e.preventDefault(); // Prevent scrolling while dragging
  };

  const handleTouchEnd = (_e: React.TouchEvent, index: number) => {
    if (disabled || touchStartIndex === null) return;
    
    if (touchStartIndex !== index) {
      // Reorder logic for touch
      const newImages = [...images];
      const draggedImage = newImages[touchStartIndex];
      newImages.splice(touchStartIndex, 1);
      newImages.splice(index, 0, draggedImage);
      
      onImagesChange(newImages);
      
      if (onReorder) {
        onReorder(newImages).catch(console.error);
      }
    }
    
    setTouchStartIndex(null);
    setDraggedIndex(null);
    setDragOverIndex(null);
  };

  const handleEditImage = async (imageUrl: string, editedBlob: Blob) => {
    if (disabled) return;

    try {
      // Convert blob to file
      const editedFile = new File([editedBlob], 'edited-image.jpg', { type: 'image/jpeg' });
      
      // Upload the edited image
      const newImageUrl = await onUpload(editedFile);
      
      // Replace the old image with the new one
      const imageIndex = images.indexOf(imageUrl);
      if (imageIndex !== -1) {
        const newImages = [...images];
        newImages[imageIndex] = newImageUrl;
        onImagesChange(newImages);
        
        // Delete the old image
        await onDelete(imageUrl);
        
        toast({
          title: 'Image updated',
          description: 'Your edited image has been saved',
        });
      }
    } catch (error) {
      console.error('Edit image failed:', error);
      toast({
        title: 'Edit failed',
        description: 'Failed to save edited image',
        variant: 'destructive',
      });
    }
  };

  const dropzoneClasses = cn(
    'border-2 border-dashed rounded-lg p-6 text-center transition-colors cursor-pointer',
    'hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary',
    {
      'border-green-400 bg-green-50': isDragAccept,
      'border-red-400 bg-red-50': isDragReject,
      'border-gray-300': !isDragActive,
      'border-primary bg-primary/5': isDragActive && !isDragReject,
      'opacity-50 cursor-not-allowed': disabled || uploading || images.length >= maxImages,
    }
  );

  return (
    <div className="space-y-4">
      {/* Image Grid */}
      {images.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {images.map((imageUrl, index) => (
            <div key={imageUrl} className="relative">
              {/* Drop indicator */}
              {dragOverIndex === index && draggedIndex !== null && draggedIndex !== index && (
                <div className="absolute -top-1 left-0 right-0 h-1 bg-blue-500 rounded z-10"></div>
              )}
              <Card
              className={cn(
                'relative group overflow-hidden aspect-square cursor-move transition-all duration-200',
                {
                  'ring-2 ring-primary scale-105 shadow-lg': draggedIndex === index,
                  'ring-2 ring-blue-400 bg-blue-50': dragOverIndex === index && draggedIndex !== index,
                  'opacity-50': draggedIndex === index,
                  'transform scale-95': dragOverIndex === index && draggedIndex !== null && draggedIndex !== index,
                }
              )}
              draggable={!disabled}
              onDragStart={(e) => handleDragStart(e, index)}
              onDragOver={(e) => handleDragOver(e, index)}
              onDragLeave={handleDragLeave}
              onDrop={(e) => handleDrop(e, index)}
              onTouchStart={(e) => handleTouchStart(e, index)}
              onTouchMove={handleTouchMove}
              onTouchEnd={(e) => handleTouchEnd(e, index)}
            >
              <img
                src={imageUrl}
                alt={`Profile image ${index + 1}`}
                className="w-full h-full object-cover"
              />
              
              {/* Action Buttons */}
              {!disabled && (
                <div className="absolute top-2 right-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <Button
                    variant="secondary"
                    size="icon"
                    className="h-6 w-6 bg-black/50 hover:bg-black/70 text-white border-none"
                    onClick={() => setEditingImageUrl(imageUrl)}
                  >
                    <Edit className="h-3 w-3" />
                  </Button>
                  <Button
                    variant="destructive"
                    size="icon"
                    className="h-6 w-6"
                    onClick={() => handleDelete(imageUrl, index)}
                  >
                    <X className="h-3 w-3" />
                  </Button>
                </div>
              )}

              {/* First Image Badge */}
              {index === 0 && (
                <div className="absolute bottom-2 left-2 bg-primary text-primary-foreground text-xs px-2 py-1 rounded">
                  Main
                </div>
              )}
            </Card>
            </div>
          ))}
        </div>
      )}

      {/* Upload Dropzone */}
      {images.length < maxImages && !disabled && (
        <div {...getRootProps({ className: dropzoneClasses })}>
          <input {...getInputProps()} />
          
          <div className="flex flex-col items-center justify-center space-y-3">
            {uploading ? (
              <>
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
                <p className="text-sm text-gray-600">Uploading images...</p>
              </>
            ) : isDragAccept ? (
              <>
                <Upload className="h-8 w-8 text-green-600" />
                <p className="text-sm text-green-600">Drop images here</p>
              </>
            ) : isDragReject ? (
              <>
                <AlertCircle className="h-8 w-8 text-red-600" />
                <p className="text-sm text-red-600">Only image files are allowed</p>
              </>
            ) : (
              <>
                <ImageIcon className="h-8 w-8 text-gray-400" />
                <div className="space-y-1">
                  <p className="text-sm text-gray-600">
                    Drag & drop images here, or click to select
                  </p>
                  <p className="text-xs text-gray-400">
                    PNG, JPG, WEBP up to 10MB each • {images.length}/{maxImages} images
                  </p>
                </div>
              </>
            )}
          </div>
        </div>
      )}

      {/* Upload Instructions */}
      {images.length === 0 && (
        <div className="text-center text-sm text-gray-500">
          <p>Upload up to {maxImages} photos to make your profile stand out!</p>
          <p className="mt-1">The first image will be your main profile photo.</p>
        </div>
      )}

      {/* Reorder Instructions */}
      {images.length > 1 && !disabled && (
        <div className="text-center text-sm text-gray-500">
          <p>Drag and drop images to reorder them</p>
        </div>
      )}

      {/* Image Editor Modal */}
      {editingImageUrl && (
        <ImageEditor
          open={!!editingImageUrl}
          onOpenChange={(open) => {
            if (!open) setEditingImageUrl(null);
          }}
          imageUrl={editingImageUrl}
          onSave={async (editedBlob) => {
            await handleEditImage(editingImageUrl, editedBlob);
            setEditingImageUrl(null);
          }}
        />
      )}
    </div>
  );
}