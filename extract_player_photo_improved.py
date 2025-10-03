#!/usr/bin/env python3
"""
Improved player photo extraction with better white background removal.
Uses more aggressive techniques to remove white areas and keep only the player.
"""

import os
from PIL import Image, ImageOps, ImageFilter
import numpy as np
from scipy import ndimage

def remove_white_background_advanced(img, white_threshold=200, blur_radius=2):
    """
    Advanced white background removal using multiple techniques.
    
    Args:
        img: PIL Image
        white_threshold: Threshold for white detection (lower = more aggressive)
        blur_radius: Radius for edge detection blur
    
    Returns:
        PIL Image with white background removed
    """
    # Convert to numpy array
    img_array = np.array(img)
    
    # Method 1: Simple white threshold
    white_mask = np.all(img_array >= white_threshold, axis=2)
    
    # Method 2: Edge detection to find content boundaries
    gray = np.mean(img_array, axis=2)
    edges = ndimage.sobel(gray)
    edge_mask = edges > np.percentile(edges, 85)  # Keep top 15% of edges
    
    # Method 3: Color variance detection (white areas have low variance)
    color_variance = np.var(img_array, axis=2)
    variance_mask = color_variance > np.percentile(color_variance, 20)  # Keep areas with higher color variance
    
    # Combine masks - keep areas that are NOT white AND have edges OR color variance
    content_mask = (~white_mask) | (edge_mask) | (variance_mask)
    
    # Apply morphological operations to clean up the mask
    from scipy.ndimage import binary_fill_holes, binary_erosion, binary_dilation
    
    # Fill holes in the mask
    content_mask = binary_fill_holes(content_mask)
    
    # Erode to remove small noise
    content_mask = binary_erosion(content_mask, iterations=2)
    
    # Dilate to restore content
    content_mask = binary_dilation(content_mask, iterations=3)
    
    # Find the largest connected component (the main content)
    labeled_array, num_features = ndimage.label(content_mask)
    if num_features > 0:
        # Get sizes of each component
        component_sizes = ndimage.sum(content_mask, labeled_array, range(1, num_features + 1))
        # Keep only the largest component
        largest_component = np.argmax(component_sizes) + 1
        content_mask = (labeled_array == largest_component)
    
    # Create a new image with transparent background
    result = img.convert('RGBA')
    result_array = np.array(result)
    
    # Set alpha channel based on content mask
    result_array[:, :, 3] = np.where(content_mask, 255, 0)
    
    return Image.fromarray(result_array, 'RGBA')

def extract_player_photo_improved(input_path, output_path, player_name="afthab"):
    """
    Improved player photo extraction with better white background removal.
    """
    try:
        # Open the image
        img = Image.open(input_path)
        print(f"Original image size: {img.size}")
        
        # Convert to RGB if not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get image dimensions
        width, height = img.size
        
        # Crop the left half of the image (where the player photo is)
        crop_width = width // 2
        left_crop = img.crop((0, 0, crop_width, height))
        
        print(f"Cropped image size: {left_crop.size}")
        
        # Apply advanced white background removal
        print("Applying advanced white background removal...")
        processed_img = remove_white_background_advanced(left_crop, white_threshold=180, blur_radius=2)
        
        # Convert back to RGB for saving
        if processed_img.mode == 'RGBA':
            # Create a white background
            white_bg = Image.new('RGB', processed_img.size, (255, 255, 255))
            white_bg.paste(processed_img, mask=processed_img.split()[-1])  # Use alpha channel as mask
            processed_img = white_bg
        
        # Find the bounding box of non-white content
        img_array = np.array(processed_img)
        white_threshold = 240
        mask = np.any(img_array < white_threshold, axis=2)
        
        if not np.any(mask):
            print("No content found after processing")
            return False
        
        # Find bounding box
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]
        
        print(f"Content bounding box: x({x_min}, {x_max}), y({y_min}, {y_max})")
        
        # Add padding
        padding = 30
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(crop_width, x_max + padding)
        y_max = min(height, y_max + padding)
        
        # Final crop
        final_photo = processed_img.crop((x_min, y_min, x_max, y_max))
        
        print(f"Final player photo size: {final_photo.size}")
        
        # Save the result
        final_photo.save(output_path, 'PNG', quality=95)
        
        print(f"Player photo saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

def main():
    # File paths
    input_path = "screenshots/page_004.png"
    output_dir = "players"
    player_name = "afthab"
    output_path = os.path.join(output_dir, f"{player_name}_improved.png")
    
    # Check if input image exists
    if not os.path.exists(input_path):
        print(f"Error: Input image not found at {input_path}")
        return
    
    print(f"Extracting player photo with improved background removal...")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print("-" * 50)
    
    # Extract player photo
    success = extract_player_photo_improved(input_path, output_path, player_name)
    
    if success:
        print("\n✅ Improved player photo extraction completed!")
    else:
        print("\n❌ Player photo extraction failed!")

if __name__ == "__main__":
    main()
