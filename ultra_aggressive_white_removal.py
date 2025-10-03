#!/usr/bin/env python3
"""
ULTRA-AGGRESSIVE WHITE SPACE REMOVAL
Enhanced script to remove the remaining 14-15 pixel white space around images.
Uses more aggressive techniques while preserving white clothing and accessories.
"""

import os
import sys
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
from scipy import ndimage

class UltraAggressiveWhiteRemover:
    """
    Ultra-aggressive white space removal with edge-based trimming.
    """
    
    def __init__(self, white_threshold=230, blue_threshold=50):
        self.white_threshold = white_threshold
        self.blue_threshold = blue_threshold
        
    def is_white_pixel(self, rgb):
        """More aggressive white detection."""
        r, g, b = rgb
        return (r >= self.white_threshold and 
                g >= self.white_threshold and 
                b >= self.white_threshold)
    
    def is_blue_text_pixel(self, rgb):
        """Check if pixel is blue text."""
        r, g, b = rgb
        return (b > (r + self.blue_threshold) and 
                b > (g + self.blue_threshold) and 
                b > 100)
    
    def is_white_clothing_pixel(self, rgb, position, img_array):
        """Detect white clothing (t-shirt, sunglasses frames) vs background white."""
        r, g, b = rgb
        y, x = position
        
        # White clothing typically has some texture or is near other content
        # Check surrounding area for content
        height, width = img_array.shape[:2]
        
        # Check 3x3 area around pixel
        y_start = max(0, y-1)
        y_end = min(height, y+2)
        x_start = max(0, x-1)
        x_end = min(width, x+2)
        
        surrounding_area = img_array[y_start:y_end, x_start:x_end]
        
        # Count non-white pixels in surrounding area
        non_white_count = 0
        for py in range(surrounding_area.shape[0]):
            for px in range(surrounding_area.shape[1]):
                pr, pg, pb = surrounding_area[py, px]
                if not (pr >= 240 and pg >= 240 and pb >= 240):
                    non_white_count += 1
        
        # If surrounded by content, likely white clothing
        # If surrounded by white, likely background
        return non_white_count > 2
    
    def is_subject_pixel(self, rgb, position, img_array):
        """Enhanced subject pixel detection."""
        # Not white background
        if self.is_white_pixel(rgb):
            # Check if it's white clothing vs background
            return self.is_white_clothing_pixel(rgb, position, img_array)
        
        # Not blue text
        if self.is_blue_text_pixel(rgb):
            return False
            
        # Everything else is subject
        return True
    
    def detect_edges_ultra_precise(self, img_array):
        """Ultra-precise edge detection for white space trimming."""
        gray = np.mean(img_array, axis=2)
        
        # Multiple edge detection methods
        sobel_x = ndimage.sobel(gray, axis=1)
        sobel_y = ndimage.sobel(gray, axis=0)
        sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        
        # Laplacian
        laplacian = ndimage.laplace(gray)
        
        # Prewitt
        prewitt_x = ndimage.prewitt(gray, axis=1)
        prewitt_y = ndimage.prewitt(gray, axis=0)
        prewitt_magnitude = np.sqrt(prewitt_x**2 + prewitt_y**2)
        
        # Combine all methods
        edge_threshold = np.percentile(sobel_magnitude, 70)  # More aggressive
        edge_mask = (
            (sobel_magnitude > edge_threshold) |
            (np.abs(laplacian) > np.percentile(np.abs(laplacian), 60)) |
            (prewitt_magnitude > np.percentile(prewitt_magnitude, 70))
        )
        
        return edge_mask
    
    def trim_white_edges_aggressive(self, img_array, content_mask):
        """Aggressively trim white edges using edge detection."""
        height, width = img_array.shape[:2]
        
        # Find edges
        edge_mask = self.detect_edges_ultra_precise(img_array)
        
        # Combine content mask with edge mask
        combined_mask = content_mask | edge_mask
        
        # Apply morphological operations to clean up
        combined_mask = ndimage.binary_fill_holes(combined_mask)
        combined_mask = ndimage.binary_erosion(combined_mask, iterations=1)
        combined_mask = ndimage.binary_dilation(combined_mask, iterations=1)
        
        return combined_mask
    
    def scan_and_trim_edges(self, img_array):
        """Scan image and aggressively trim white edges."""
        height, width = img_array.shape[:2]
        
        print("  - Performing ultra-aggressive white space removal...")
        
        # Create initial content mask
        content_mask = np.zeros((height, width), dtype=bool)
        
        # Scan every pixel
        for y in range(height):
            for x in range(width):
                if self.is_subject_pixel(img_array[y, x], (y, x), img_array):
                    content_mask[y, x] = True
        
        # Apply edge-based trimming
        content_mask = self.trim_white_edges_aggressive(img_array, content_mask)
        
        # Additional edge trimming from all sides
        print("  - Trimming white edges from all sides...")
        
        # Trim from top
        for y in range(height):
            if np.any(content_mask[y, :]):
                # Find first non-white column
                for x in range(width):
                    if content_mask[y, x]:
                        # Check if this row has mostly white pixels
                        row_white_count = np.sum(~content_mask[y, :])
                        if row_white_count > width * 0.8:  # 80% white
                            content_mask[y, :] = False
                        break
                break
        
        # Trim from bottom
        for y in range(height-1, -1, -1):
            if np.any(content_mask[y, :]):
                row_white_count = np.sum(~content_mask[y, :])
                if row_white_count > width * 0.8:
                    content_mask[y, :] = False
                break
        
        # Trim from left
        for x in range(width):
            if np.any(content_mask[:, x]):
                col_white_count = np.sum(~content_mask[:, x])
                if col_white_count > height * 0.8:
                    content_mask[:, x] = False
                break
        
        # Trim from right
        for x in range(width-1, -1, -1):
            if np.any(content_mask[:, x]):
                col_white_count = np.sum(~content_mask[:, x])
                if col_white_count > height * 0.8:
                    content_mask[:, x] = False
                break
        
        return content_mask
    
    def find_ultra_precise_bounds(self, mask):
        """Find ultra-precise bounding box."""
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            return None
        
        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]
        
        return (x_min, y_min), (x_max, y_max)
    
    def process_image(self, input_path, output_path):
        """Process image with ultra-aggressive white space removal."""
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
            print("Applying ultra-aggressive white space removal...")
            
            # Scan and trim edges
            content_mask = self.scan_and_trim_edges(img_array)
            
            # Count pixels
            subject_pixels = np.sum(content_mask)
            white_pixels = np.sum(~content_mask)
            total_pixels = height * width
            
            print(f"Subject pixels: {subject_pixels:,} ({subject_pixels/total_pixels*100:.1f}%)")
            print(f"White pixels: {white_pixels:,} ({white_pixels/total_pixels*100:.1f}%)")
            
            # Find ultra-precise bounds
            bounds = self.find_ultra_precise_bounds(content_mask)
            if bounds is None:
                print("No content found!")
                return False
            
            (x_min, y_min), (x_max, y_max) = bounds
            print(f"Content bounds: x({x_min}, {x_max}), y({y_min}, {y_max})")
            
            # NO PADDING - pixel perfect cropping
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(width, x_max)
            y_max = min(height, y_max)
            
            # Crop to exact content bounds
            cropped_img = img.crop((x_min, y_min, x_max, y_max))
            
            print(f"Final size: {cropped_img.size}")
            print(f"Saved to: {output_path}")
            
            # Save result
            cropped_img.save(output_path, 'PNG', quality=95)
            
            # Print ultra-precise bounding box coordinates
            print("\n" + "="*60)
            print("ULTRA-PRECISE BOUNDING BOX COORDINATES:")
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
    """Main function for ultra-aggressive white space removal."""
    if len(sys.argv) != 3:
        print("Usage: python ultra_aggressive_white_removal.py <input_path> <output_path>")
        print("Example: python ultra_aggressive_white_removal.py input.png output.png")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Check if input exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        return
    
    print("ULTRA-AGGRESSIVE WHITE SPACE REMOVAL")
    print("="*60)
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print("-" * 60)
    
    # Create processor
    processor = UltraAggressiveWhiteRemover(
        white_threshold=230,  # More aggressive
        blue_threshold=50
    )
    
    # Process image
    success = processor.process_image(input_path, output_path)
    
    if success:
        print("\n✅ Ultra-aggressive white space removal completed!")
    else:
        print("\n❌ Processing failed!")

if __name__ == "__main__":
    main()
