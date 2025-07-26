import { useState, useCallback } from 'react';
import Cropper from 'react-easy-crop';
import { Button } from '../ui/Button';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '../ui/dialog';
import { Slider } from '../ui/slider';
import { RotateCcw, RotateCw, Download } from 'lucide-react';
import { cn } from '../../lib/utils';

interface Area {
  x: number;
  y: number;
  width: number;
  height: number;
}

interface ImageEditorProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  imageUrl: string;
  onSave: (croppedImageBlob: Blob) => Promise<void>;
}

// Filter options
const FILTERS = [
  { name: 'Original', value: 'none' },
  { name: 'Sepia', value: 'sepia(100%)' },
  { name: 'Grayscale', value: 'grayscale(100%)' },
  { name: 'Vintage', value: 'sepia(50%) contrast(1.2) brightness(1.1)' },
  { name: 'Cool', value: 'hue-rotate(180deg) saturate(1.2)' },
  { name: 'Warm', value: 'hue-rotate(25deg) saturate(1.1) brightness(1.1)' },
];

// Helper function to create image from URL
const createImage = (url: string): Promise<HTMLImageElement> =>
  new Promise((resolve, reject) => {
    const image = new Image();
    image.addEventListener('load', () => resolve(image));
    image.addEventListener('error', (error) => reject(error));
    image.setAttribute('crossOrigin', 'anonymous');
    image.src = url;
  });

// Helper function to get cropped image as blob
const getCroppedImg = async (
  imageSrc: string,
  pixelCrop: Area,
  rotation = 0,
  filter = 'none'
): Promise<Blob> => {
  const image = await createImage(imageSrc);
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');

  if (!ctx) {
    throw new Error('Could not create canvas context');
  }

  const maxSize = Math.max(image.width, image.height);
  const safeArea = 2 * ((maxSize / 2) * Math.sqrt(2));

  // Set canvas size to accommodate rotation
  canvas.width = safeArea;
  canvas.height = safeArea;

  // Translate canvas context to center point
  ctx.translate(safeArea / 2, safeArea / 2);
  ctx.rotate((rotation * Math.PI) / 180);
  ctx.translate(-safeArea / 2, -safeArea / 2);

  // Apply filter
  ctx.filter = filter;

  // Draw rotated image
  ctx.drawImage(
    image,
    safeArea / 2 - image.width * 0.5,
    safeArea / 2 - image.height * 0.5
  );

  const data = ctx.getImageData(0, 0, safeArea, safeArea);

  // Set canvas width/height to final desired crop size
  canvas.width = pixelCrop.width;
  canvas.height = pixelCrop.height;

  // Paste generated rotate image at the top left corner
  ctx.putImageData(
    data,
    0 - safeArea / 2 + image.width * 0.5 - pixelCrop.x,
    0 - safeArea / 2 + image.height * 0.5 - pixelCrop.y
  );

  return new Promise((resolve) => {
    canvas.toBlob(
      (blob) => {
        if (blob) {
          resolve(blob);
        }
      },
      'image/jpeg',
      0.9
    );
  });
};

export function ImageEditor({ open, onOpenChange, imageUrl, onSave }: ImageEditorProps) {
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [rotation, setRotation] = useState(0);
  const [selectedFilter, setSelectedFilter] = useState('none');
  const [croppedAreaPixels, setCroppedAreaPixels] = useState<Area | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const onCropComplete = useCallback((_croppedArea: Area, croppedAreaPixels: Area) => {
    setCroppedAreaPixels(croppedAreaPixels);
  }, []);

  const handleSave = async () => {
    if (!croppedAreaPixels) return;

    setIsProcessing(true);
    try {
      const croppedImageBlob = await getCroppedImg(
        imageUrl,
        croppedAreaPixels,
        rotation,
        selectedFilter
      );
      await onSave(croppedImageBlob);
      onOpenChange(false);
    } catch (error) {
      console.error('Error processing image:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRotateLeft = () => {
    setRotation((prev) => (prev - 90) % 360);
  };

  const handleRotateRight = () => {
    setRotation((prev) => (prev + 90) % 360);
  };

  const resetImage = () => {
    setCrop({ x: 0, y: 0 });
    setZoom(1);
    setRotation(0);
    setSelectedFilter('none');
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl h-[80vh] overflow-hidden">
        <DialogHeader>
          <DialogTitle>Edit Image</DialogTitle>
          <DialogDescription>
            Crop, rotate, and apply filters to your image
          </DialogDescription>
        </DialogHeader>

        <div className="flex flex-1 gap-4 min-h-0">
          {/* Cropper Area */}
          <div className="flex-1 relative bg-gray-100 rounded-lg overflow-hidden">
            <Cropper
              image={imageUrl}
              crop={crop}
              zoom={zoom}
              rotation={rotation}
              aspect={1}
              onCropChange={setCrop}
              onCropComplete={onCropComplete}
              onZoomChange={setZoom}
              style={{
                mediaStyle: {
                  filter: selectedFilter,
                },
              }}
            />
          </div>

          {/* Controls Sidebar */}
          <div className="w-64 space-y-6 p-4 bg-gray-50 rounded-lg">
            {/* Zoom Control */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Zoom</label>
              <Slider
                value={[zoom]}
                onValueChange={(value) => setZoom(value[0])}
                min={1}
                max={3}
                step={0.1}
                className="w-full"
              />
              <div className="text-xs text-gray-500">{Math.round(zoom * 100)}%</div>
            </div>

            {/* Rotation Controls */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Rotation</label>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleRotateLeft}
                  className="flex-1"
                >
                  <RotateCcw className="h-4 w-4" />
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleRotateRight}
                  className="flex-1"
                >
                  <RotateCw className="h-4 w-4" />
                </Button>
              </div>
              <div className="text-xs text-gray-500 text-center">{rotation}°</div>
            </div>

            {/* Filter Selection */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Filters</label>
              <div className="grid grid-cols-2 gap-2">
                {FILTERS.map((filter) => (
                  <button
                    key={filter.name}
                    onClick={() => setSelectedFilter(filter.value)}
                    className={cn(
                      'p-2 text-xs rounded border transition-colors',
                      selectedFilter === filter.value
                        ? 'bg-primary text-primary-foreground border-primary'
                        : 'bg-white hover:bg-gray-50 border-gray-200'
                    )}
                  >
                    {filter.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Reset Button */}
            <Button
              variant="outline"
              onClick={resetImage}
              className="w-full"
            >
              Reset
            </Button>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleSave} 
            disabled={isProcessing || !croppedAreaPixels}
            className="gap-2"
          >
            {isProcessing ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                Processing...
              </>
            ) : (
              <>
                <Download className="h-4 w-4" />
                Save Changes
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}