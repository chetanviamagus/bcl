#!/usr/bin/env python3
"""
SAFE MARGIN WHITE SPACE REMOVAL
Final script with 2px safety margin removal from all 4 sides.
Ensures completely clean image with no white space whatsoever.
"""

import os
import sys
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
from scipy import ndimage

class SafeMarginWhiteRemover:
    """
    Safe margin white space removal with 2px buffer from all sides.
    """
    
    def __init__(self, white_threshold=225, blue_threshold=50, safety_margin=2):
        self.white_threshold = white_threshold
        self.blue_threshold = blue_threshold
        self.safety_margin = safety_margin
        
    def is_white_pixel(self, rgb):
        """Very aggressive white detection."""
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
        """Enhanced white clothing detection."""
        r, g, b = rgb
        y, x = position
        height, width = img_array.shape[:2]
        
        # Check larger area around pixel (5x5)
        y_start = max(0, y-2)
        y_end = min(height, y+3)
        x_start = max(0, x-2)
        x_end = min(width, x+3)
        
        surrounding_area = img_array[y_start:y_end, x_start:x_end]
        
        # Count non-white pixels in surrounding area
        non_white_count = 0
        for py in range(surrounding_area.shape[0]):
            for px in range(surrounding_area.shape[1]):
                pr, pg, pb = surrounding_area[py, px]
                if not (pr >= 240 and pg >= 240 and pb >= 240):
                    non_white_count += 1
        
        # If surrounded by significant content, likely white clothing
        return non_white_count > 4
    
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
    
    def detect_content_with_safety_margin(self, img_array):
        """Detect content and apply safety margin."""
        height, width = img_array.shape[:2]
        
        print("  - Detecting content with safety margin...")
        
        # Create content mask
        content_mask = np.zeros((height, width), dtype=bool)
        
        # Scan every pixel
        for y in range(height):
            for x in range(width):
                if self.is_subject_pixel(img_array[y, x], (y, x), img_array):
                    content_mask[y, x] = True
        
        # Apply morphological operations
        content_mask = ndimage.binary_fill_holes(content_mask)
        content_mask = ndimage.binary_erosion(content_mask, iterations=1)
        content_mask = ndimage.binary_dilation(content_mask, iterations=1)
        
        # Find largest connected component
        labeled_array, num_features = ndimage.label(content_mask)
        if num_features > 0:
            component_sizes = ndimage.sum(content_mask, labeled_array, range(1, num_features + 1))
            largest_component = np.argmax(component_sizes) + 1
            content_mask = (labeled_array == largest_component)
        
        return content_mask
    
    def find_content_bounds_with_safety_margin(self, mask):
        """Find content bounds and apply 2px safety margin from all sides."""
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            return None
        
        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]
        
        # Apply safety margin - remove 2px from all sides
        height, width = mask.shape
        
        # Add safety margin
        x_min = max(0, x_min + self.safety_margin)
        y_min = max(0, y_min + self.safety_margin)
        x_max = min(width, x_max - self.safety_margin)
        y_max = min(height, y_max - self.safety_margin)
        
        # Ensure we don't have negative dimensions
        if x_max <= x_min or y_max <= y_min:
            print("Warning: Safety margin too large, using original bounds")
            rows = np.any(mask, axis=1)
            cols = np.any(mask, axis=0)
            y_min, y_max = np.where(rows)[0][[0, -1]]
            x_min, x_max = np.where(cols)[0][[0, -1]]
        
        return (x_min, y_min), (x_max, y_max)
    
    def process_image(self, input_path, output_path):
        """Process image with safe margin white space removal."""
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
            print(f"Applying safe margin white space removal (2px from all sides)...")
            
            # Detect content
            content_mask = self.detect_content_with_safety_margin(img_array)
            
            # Count pixels
            subject_pixels = np.sum(content_mask)
            white_pixels = np.sum(~content_mask)
            total_pixels = height * width
            
            print(f"Subject pixels: {subject_pixels:,} ({subject_pixels/total_pixels*100:.1f}%)")
            print(f"White pixels: {white_pixels:,} ({white_pixels/total_pixels*100:.1f}%)")
            
            # Find content bounds with safety margin
            bounds = self.find_content_bounds_with_safety_margin(content_mask)
            if bounds is None:
                print("No content found!")
                return False
            
            (x_min, y_min), (x_max, y_max) = bounds
            print(f"Content bounds with safety margin: x({x_min}, {x_max}), y({y_min}, {y_max})")
            
            # Crop to bounds with safety margin
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(width, x_max)
            y_max = min(height, y_max)
            
            # Final crop
            final_img = img.crop((x_min, y_min, x_max, y_max))
            
            print(f"Final size: {final_img.size}")
            print(f"Safety margin applied: {self.safety_margin}px from all sides")
            print(f"Saved to: {output_path}")
            
            # Save result
            final_img.save(output_path, 'PNG', quality=95)
            
            # Print safe bounding box coordinates
            print("\n" + "="*60)
            print("SAFE MARGIN BOUNDING BOX COORDINATES:")
            print(f"Safety margin: {self.safety_margin}px from all sides")
            print(f"Top-left corner:     ({x_min}, {y_min})")
            print(f"Bottom-left corner:  ({x_min}, {y_max-1})")
            print(f"Bottom-right corner: ({x_max-1}, {y_max-1})")
            print(f"Top-right corner:    ({x_max-1}, {y_min})")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return False

def main():
    """Main function for safe margin white space removal."""
    if len(sys.argv) != 3:
        print("Usage: python safe_margin_white_removal.py <input_path> <output_path>")
        print("Example: python safe_margin_white_removal.py input.png output.png")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Check if input exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        return
    
    print("SAFE MARGIN WHITE SPACE REMOVAL")
    print("="*60)
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print("-" * 60)
    
    # Create processor with 2px safety margin
    processor = SafeMarginWhiteRemover(
        white_threshold=225,
        blue_threshold=50,
        safety_margin=2  # 2px from all sides
    )
    
    # Process image
    success = processor.process_image(input_path, output_path)
    
    if success:
        print("\n✅ Safe margin white space removal completed!")
        print("✅ 2px safety margin applied from all 4 sides!")
    else:
        print("\n❌ Processing failed!")

if __name__ == "__main__":
    main()
