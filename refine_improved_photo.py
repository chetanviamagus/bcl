#!/usr/bin/env python3
"""
Apply systematic pixel-by-pixel scanning algorithm to afthab_improved.png
to further refine and remove any remaining white areas.
"""

import os
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np

def is_white_pixel(rgb, threshold=240):
    """
    Check if a pixel is considered white background.
    """
    r, g, b = rgb
    return r >= threshold and g >= threshold and b >= threshold

def is_blue_text_pixel(rgb, threshold=50):
    """
    Check if a pixel is blue text (to be ignored).
    Blue text typically has high blue component and lower red/green.
    """
    r, g, b = rgb
    return b > (r + threshold) and b > (g + threshold) and b > 100

def is_subject_pixel(rgb, white_threshold=240, blue_threshold=50):
    """
    Check if a pixel belongs to the human subject.
    Not white background and not blue text.
    """
    return not is_white_pixel(rgb, white_threshold) and not is_blue_text_pixel(rgb, blue_threshold)

def scan_improved_image_for_refinement(img_array, white_threshold=240, blue_threshold=50):
    """
    Scan the improved image to find and remove any remaining white areas.
    
    Args:
        img_array: numpy array of the improved image
        white_threshold: threshold for white background detection
        blue_threshold: threshold for blue text detection
    
    Returns:
        tuple: ((x0, y0), (x1, y1)) - refined bounding box coordinates
    """
    height, width = img_array.shape[:2]
    
    print(f"Scanning improved image of size {width}x{height} pixels...")
    
    # Initialize bounding box coordinates
    x0, y0 = width, height  # Start with max values
    x1, y1 = 0, 0           # Start with min values
    
    subject_pixels_found = 0
    white_pixels_found = 0
    
    # Scan pixel by pixel
    for y in range(height):
        for x in range(width):
            rgb = img_array[y, x]
            
            if is_subject_pixel(rgb, white_threshold, blue_threshold):
                subject_pixels_found += 1
                
                # Update bounding box
                if x < x0:
                    x0 = x
                if x > x1:
                    x1 = x
                if y < y0:
                    y0 = y
                if y > y1:
                    y1 = y
            elif is_white_pixel(rgb, white_threshold):
                white_pixels_found += 1
    
    print(f"Found {subject_pixels_found} subject pixels")
    print(f"Found {white_pixels_found} white pixels (to be removed)")
    print(f"Refined bounding box: x({x0}, {x1}), y({y0}, {y1})")
    
    return (x0, y0), (x1, y1)

def refine_improved_photo(input_path, output_path, player_name="afthab"):
    """
    Refine the improved photo using systematic pixel scanning.
    """
    try:
        # Open the improved image
        img = Image.open(input_path)
        print(f"Improved image size: {img.size}")
        
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to numpy array for pixel scanning
        img_array = np.array(img)
        
        # Scan for refined subject bounds
        print("Performing pixel-by-pixel scan on improved image...")
        (x0, y0), (x1, y1) = scan_improved_image_for_refinement(
            img_array, 
            white_threshold=240, 
            blue_threshold=50
        )
        
        # Validate bounding box
        if x0 >= x1 or y0 >= y1:
            print("No valid subject found in improved image!")
            return False
        
        # Add minimal padding around the subject (since it's already improved)
        padding = 15
        x0 = max(0, x0 - padding)
        y0 = max(0, y0 - padding)
        x1 = min(img.size[0], x1 + padding)
        y1 = min(img.size[1], y1 + padding)
        
        print(f"Final refined bounding box with padding: x({x0}, {x1}), y({y0}, {y1})")
        
        # Extract the refined subject
        refined_img = img.crop((x0, y0, x1, y1))
        
        print(f"Refined subject size: {refined_img.size}")
        
        # Apply slight enhancement
        enhancer = ImageEnhance.Contrast(refined_img)
        refined_img = enhancer.enhance(1.02)
        
        # Save the result
        refined_img.save(output_path, 'PNG', quality=95)
        
        print(f"Refined subject saved to: {output_path}")
        
        # Print refined bounding box coordinates
        print("\n" + "="*50)
        print("REFINED BOUNDING BOX COORDINATES:")
        print(f"Top-left corner:     ({x0}, {y0})")
        print(f"Bottom-left corner:  ({x0}, {y1})")
        print(f"Bottom-right corner: ({x1}, {y1})")
        print(f"Top-right corner:    ({x1}, {y0})")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"Error processing improved image: {e}")
        return False

def main():
    # File paths
    input_path = "players/afthab_improved.png"
    output_dir = "players"
    player_name = "afthab"
    output_path = os.path.join(output_dir, f"{player_name}_refined.png")
    
    # Check if input image exists
    if not os.path.exists(input_path):
        print(f"Error: Improved image not found at {input_path}")
        return
    
    print("REFINING IMPROVED PLAYER PHOTO")
    print("Applying systematic algorithm to afthab_improved.png")
    print("="*50)
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print("-" * 50)
    
    # Refine the improved photo
    success = refine_improved_photo(input_path, output_path, player_name)
    
    if success:
        print("\n✅ Refined player photo extraction completed!")
    else:
        print("\n❌ Photo refinement failed!")

if __name__ == "__main__":
    main()
