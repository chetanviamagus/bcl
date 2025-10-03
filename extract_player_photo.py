#!/usr/bin/env python3
"""
Extract player photo from page_004.png by removing white background and text.
Keeps only the player photo on the left side of the page.
"""

import os
from PIL import Image, ImageOps
import numpy as np

def extract_player_photo(input_path, output_path, player_name="afthab"):
    """
    Extract player photo from a page image by cropping the left side and removing white background.
    
    Args:
        input_path (str): Path to the input page image
        output_path (str): Path to save the extracted player photo
        player_name (str): Name of the player for filename
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
        # Based on the description, the photo takes up roughly the left half
        crop_width = width // 2
        left_crop = img.crop((0, 0, crop_width, height))
        
        print(f"Cropped image size: {left_crop.size}")
        
        # Convert to numpy array for processing
        img_array = np.array(left_crop)
        
        # Create a mask for non-white pixels
        # White pixels are typically [255, 255, 255] or close to it
        # We'll use a threshold to identify non-white areas
        white_threshold = 240  # Pixels with RGB values above this are considered white
        mask = np.any(img_array < white_threshold, axis=2)
        
        # Find bounding box of non-white pixels
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            print("No non-white content found in the cropped area")
            return False
        
        # Get the bounding box coordinates
        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]
        
        print(f"Content bounding box: x({x_min}, {x_max}), y({y_min}, {y_max})")
        
        # Add some padding around the content
        padding = 20
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(crop_width, x_max + padding)
        y_max = min(height, y_max + padding)
        
        # Crop to the bounding box
        player_photo = left_crop.crop((x_min, y_min, x_max, y_max))
        
        print(f"Final player photo size: {player_photo.size}")
        
        # Save the extracted player photo
        player_photo.save(output_path, 'PNG', quality=95)
        
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
    output_path = os.path.join(output_dir, f"{player_name}.png")
    
    # Check if input image exists
    if not os.path.exists(input_path):
        print(f"Error: Input image not found at {input_path}")
        return
    
    print(f"Extracting player photo from: {input_path}")
    print(f"Saving to: {output_path}")
    print("-" * 50)
    
    # Extract player photo
    success = extract_player_photo(input_path, output_path, player_name)
    
    if success:
        print("\n✅ Player photo extraction completed successfully!")
    else:
        print("\n❌ Player photo extraction failed!")

if __name__ == "__main__":
    main()
