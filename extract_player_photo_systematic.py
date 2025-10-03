#!/usr/bin/env python3
"""
Systematic player photo extraction using pixel-by-pixel scanning.
Implements the user's suggested algorithm for precise bounding box detection.
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

def scan_image_for_subject_bounds(img_array, white_threshold=240, blue_threshold=50):
    """
    Scan image pixel by pixel to find subject bounding box.
    
    Args:
        img_array: numpy array of the image
        white_threshold: threshold for white background detection
        blue_threshold: threshold for blue text detection
    
    Returns:
        tuple: ((x0, y0), (x1, y1)) - bounding box coordinates
    """
    height, width = img_array.shape[:2]
    
    print(f"Scanning image of size {width}x{height} pixels...")
    
    # Initialize bounding box coordinates
    x0, y0 = width, height  # Start with max values
    x1, y1 = 0, 0           # Start with min values
    
    subject_pixels_found = 0
    
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
    
    print(f"Found {subject_pixels_found} subject pixels")
    print(f"Bounding box: x({x0}, {x1}), y({y0}, {y1})")
    
    return (x0, y0), (x1, y1)

def extract_subject_with_precise_bounds(input_path, output_path, player_name="afthab"):
    """
    Extract subject using systematic pixel scanning approach.
    """
    try:
        # Open the image
        img = Image.open(input_path)
        print(f"Original image size: {img.size}")
        
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get image dimensions
        width, height = img.size
        
        # Crop the left half (where the player photo is)
        crop_width = width // 2
        left_crop = img.crop((0, 0, crop_width, height))
        
        print(f"Cropped image size: {left_crop.size}")
        
        # Convert to numpy array for pixel scanning
        img_array = np.array(left_crop)
        
        # Scan for subject bounds
        print("Performing pixel-by-pixel scan...")
        (x0, y0), (x1, y1) = scan_image_for_subject_bounds(
            img_array, 
            white_threshold=240, 
            blue_threshold=50
        )
        
        # Validate bounding box
        if x0 >= x1 or y0 >= y1:
            print("No valid subject found!")
            return False
        
        # Add padding around the subject
        padding = 30
        x0 = max(0, x0 - padding)
        y0 = max(0, y0 - padding)
        x1 = min(crop_width, x1 + padding)
        y1 = min(height, y1 + padding)
        
        print(f"Final bounding box with padding: x({x0}, {x1}), y({y0}, {y1})")
        
        # Extract the subject
        subject_img = left_crop.crop((x0, y0, x1, y1))
        
        print(f"Extracted subject size: {subject_img.size}")
        
        # Apply slight enhancement
        enhancer = ImageEnhance.Contrast(subject_img)
        subject_img = enhancer.enhance(1.05)
        
        # Save the result
        subject_img.save(output_path, 'PNG', quality=95)
        
        print(f"Subject extracted and saved to: {output_path}")
        
        # Print bounding box coordinates as requested
        print("\n" + "="*50)
        print("BOUNDING BOX COORDINATES:")
        print(f"Top-left corner:     ({x0}, {y0})")
        print(f"Bottom-left corner:  ({x0}, {y1})")
        print(f"Bottom-right corner: ({x1}, {y1})")
        print(f"Top-right corner:    ({x1}, {y0})")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

def main():
    # File paths
    input_path = "screenshots/page_004.png"
    output_dir = "players"
    player_name = "afthab"
    output_path = os.path.join(output_dir, f"{player_name}_systematic.png")
    
    # Check if input image exists
    if not os.path.exists(input_path):
        print(f"Error: Input image not found at {input_path}")
        return
    
    print("SYSTEMATIC PLAYER PHOTO EXTRACTION")
    print("Using pixel-by-pixel scanning algorithm")
    print("="*50)
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print("-" * 50)
    
    # Extract subject
    success = extract_subject_with_precise_bounds(input_path, output_path, player_name)
    
    if success:
        print("\n✅ Systematic player photo extraction completed!")
    else:
        print("\n❌ Player photo extraction failed!")

if __name__ == "__main__":
    main()
