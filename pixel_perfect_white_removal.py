#!/usr/bin/env python3
"""
PIXEL-PERFECT WHITE SPACE REMOVAL
Final comprehensive script for removing white space with maximum precision.
Combines all best techniques for pixel-perfect results.
"""

import os
import sys
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
from scipy import ndimage

class PixelPerfectWhiteRemover:
    """
    Advanced white space removal with pixel-perfect precision.
    """
    
    def __init__(self, white_threshold=240, blue_threshold=50, edge_sensitivity=0.3):
        self.white_threshold = white_threshold
        self.blue_threshold = blue_threshold
        self.edge_sensitivity = edge_sensitivity
        
    def is_white_pixel(self, rgb):
        """Check if pixel is white background."""
        r, g, b = rgb
        return (r >= self.white_threshold and 
                g >= self.white_threshold and 
                b >= self.white_threshold)
    
    def is_blue_text_pixel(self, rgb):
        """Check if pixel is blue text (to ignore)."""
        r, g, b = rgb
        return (b > (r + self.blue_threshold) and 
                b > (g + self.blue_threshold) and 
                b > 100)
    
    def is_subject_pixel(self, rgb):
        """Check if pixel belongs to the subject."""
        return (not self.is_white_pixel(rgb) and 
                not self.is_blue_text_pixel(rgb))
    
    def detect_edges_advanced(self, img_array):
        """Advanced edge detection using multiple methods."""
        gray = np.mean(img_array, axis=2)
        
        # Sobel edge detection
        sobel_x = ndimage.sobel(gray, axis=1)
        sobel_y = ndimage.sobel(gray, axis=0)
        sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        
        # Laplacian edge detection
        laplacian = ndimage.laplace(gray)
        
        # Canny-like edge detection
        gaussian = ndimage.gaussian_filter(gray, sigma=1.0)
        edges = ndimage.sobel(gaussian)
        
        # Combine all edge detection methods
        edge_threshold = np.percentile(sobel_magnitude, 80)
        edge_mask = (sobel_magnitude > edge_threshold) | (np.abs(laplacian) > np.percentile(np.abs(laplacian), 75))
        
        return edge_mask
    
    def detect_skin_tones(self, img_array):
        """Detect skin tone pixels."""
        r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
        
        # Enhanced skin tone detection
        skin_mask = (
            (r > 120) & (r < 240) &  # Red range
            (g > 100) & (g < 220) &  # Green range
            (b > 80) & (b < 200) &   # Blue range
            (r > g) & (g > b) &      # Red > Green > Blue
            (r - g > 15) & (g - b > 10) &  # Color differences
            (np.std(img_array, axis=2) > 15)  # Some color variation
        )
        
        return skin_mask
    
    def detect_hair_and_clothing(self, img_array):
        """Detect hair and clothing pixels."""
        rgb_mean = np.mean(img_array, axis=2)
        rgb_std = np.std(img_array, axis=2)
        
        # Hair detection (dark areas with texture)
        hair_mask = (
            (rgb_mean < 100) &  # Dark
            (rgb_std > 10) &    # Has texture
            (ndimage.sobel(rgb_mean) > np.percentile(ndimage.sobel(rgb_mean), 60))
        )
        
        # Clothing detection (non-white clothing)
        clothing_mask = (
            (rgb_mean < 200) &  # Not too bright
            (rgb_std > 20) &    # Has color variation
            (ndimage.sobel(rgb_mean) > np.percentile(ndimage.sobel(rgb_mean), 50))
        )
        
        return hair_mask | clothing_mask
    
    def create_content_mask(self, img_array):
        """Create comprehensive content mask using all detection methods."""
        height, width = img_array.shape[:2]
        
        # Initialize mask
        content_mask = np.zeros((height, width), dtype=bool)
        
        # Method 1: Direct pixel scanning
        print("  - Scanning pixels for subject content...")
        for y in range(height):
            for x in range(width):
                if self.is_subject_pixel(img_array[y, x]):
                    content_mask[y, x] = True
        
        # Method 2: Edge detection
        print("  - Applying advanced edge detection...")
        edge_mask = self.detect_edges_advanced(img_array)
        content_mask = content_mask | edge_mask
        
        # Method 3: Skin tone detection
        print("  - Detecting skin tones...")
        skin_mask = self.detect_skin_tones(img_array)
        content_mask = content_mask | skin_mask
        
        # Method 4: Hair and clothing detection
        print("  - Detecting hair and clothing...")
        hair_clothing_mask = self.detect_hair_and_clothing(img_array)
        content_mask = content_mask | hair_clothing_mask
        
        # Method 5: Color variance analysis
        print("  - Analyzing color variance...")
        local_variance = ndimage.generic_filter(np.mean(img_array, axis=2), np.var, size=15)
        variance_threshold = np.percentile(local_variance, 30)
        variance_mask = local_variance > variance_threshold
        content_mask = content_mask | variance_mask
        
        return content_mask
    
    def refine_mask(self, mask):
        """Refine the content mask using morphological operations."""
        print("  - Refining mask with morphological operations...")
        
        # Fill holes
        mask = ndimage.binary_fill_holes(mask)
        
        # Remove small noise
        mask = ndimage.binary_erosion(mask, iterations=1)
        
        # Restore content
        mask = ndimage.binary_dilation(mask, iterations=2)
        
        # Find largest connected component
        labeled_array, num_features = ndimage.label(mask)
        if num_features > 0:
            component_sizes = ndimage.sum(mask, labeled_array, range(1, num_features + 1))
            largest_component = np.argmax(component_sizes) + 1
            mask = (labeled_array == largest_component)
        
        return mask
    
    def find_pixel_perfect_bounds(self, mask):
        """Find pixel-perfect bounding box of the content."""
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            return None
        
        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]
        
        return (x_min, y_min), (x_max, y_max)
    
    def create_alpha_channel(self, img_array, content_mask):
        """Create smooth alpha channel for clean edges."""
        alpha = np.where(content_mask, 255, 0).astype(np.uint8)
        
        # Apply Gaussian blur for smooth edges
        alpha_smooth = ndimage.gaussian_filter(alpha.astype(float), sigma=0.8)
        alpha = np.clip(alpha_smooth, 0, 255).astype(np.uint8)
        
        return alpha
    
    def process_image(self, input_path, output_path):
        """Process image with pixel-perfect white space removal."""
        try:
            print(f"Processing: {input_path}")
            
            # Load image
            img = Image.open(input_path)
            print(f"Original size: {img.size}")
            
            # Convert to RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convert to numpy array
            img_array = np.array(img)
            height, width = img_array.shape[:2]
            
            print(f"Image dimensions: {width}x{height}")
            print("Applying pixel-perfect white space removal...")
            
            # Create comprehensive content mask
            content_mask = self.create_content_mask(img_array)
            
            # Refine mask
            content_mask = self.refine_mask(content_mask)
            
            # Count pixels
            subject_pixels = np.sum(content_mask)
            white_pixels = np.sum(~content_mask)
            total_pixels = height * width
            
            print(f"Subject pixels: {subject_pixels:,} ({subject_pixels/total_pixels*100:.1f}%)")
            print(f"White pixels: {white_pixels:,} ({white_pixels/total_pixels*100:.1f}%)")
            
            # Find pixel-perfect bounds
            bounds = self.find_pixel_perfect_bounds(content_mask)
            if bounds is None:
                print("No content found!")
                return False
            
            (x_min, y_min), (x_max, y_max) = bounds
            print(f"Content bounds: x({x_min}, {x_max}), y({y_min}, {y_max})")
            
            # Add minimal padding for pixel-perfect result
            padding = 5
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(width, x_max + padding)
            y_max = min(height, y_max + padding)
            
            # Crop to content bounds
            cropped_img = img.crop((x_min, y_min, x_max, y_max))
            cropped_array = np.array(cropped_img)
            
            # Create alpha channel for the cropped image
            cropped_mask = content_mask[y_min:y_max, x_min:x_max]
            alpha = self.create_alpha_channel(cropped_array, cropped_mask)
            
            # Create RGBA image
            rgba_array = np.dstack([cropped_array, alpha])
            result_img = Image.fromarray(rgba_array, 'RGBA')
            
            # Convert to RGB with white background for final output
            white_bg = Image.new('RGB', result_img.size, (255, 255, 255))
            white_bg.paste(result_img, mask=result_img.split()[-1])
            final_img = white_bg
            
            # Apply final enhancement
            enhancer = ImageEnhance.Contrast(final_img)
            final_img = enhancer.enhance(1.02)
            
            # Save result
            final_img.save(output_path, 'PNG', quality=95)
            
            print(f"Final size: {final_img.size}")
            print(f"Saved to: {output_path}")
            
            # Print bounding box coordinates
            print("\n" + "="*60)
            print("PIXEL-PERFECT BOUNDING BOX COORDINATES:")
            print(f"Top-left corner:     ({x_min}, {y_min})")
            print(f"Bottom-left corner:  ({x_min}, {y_max})")
            print(f"Bottom-right corner: ({x_max}, {y_max})")
            print(f"Top-right corner:    ({x_max}, {y_min})")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return False

def main():
    """Main function for pixel-perfect white space removal."""
    if len(sys.argv) != 3:
        print("Usage: python pixel_perfect_white_removal.py <input_path> <output_path>")
        print("Example: python pixel_perfect_white_removal.py input.png output.png")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Check if input exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        return
    
    print("PIXEL-PERFECT WHITE SPACE REMOVAL")
    print("="*60)
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print("-" * 60)
    
    # Create processor
    processor = PixelPerfectWhiteRemover(
        white_threshold=240,
        blue_threshold=50,
        edge_sensitivity=0.3
    )
    
    # Process image
    success = processor.process_image(input_path, output_path)
    
    if success:
        print("\n✅ Pixel-perfect white space removal completed!")
    else:
        print("\n❌ Processing failed!")

if __name__ == "__main__":
    main()
