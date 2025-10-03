#!/usr/bin/env python3
"""
Very aggressive player photo extraction focusing on the actual player content.
Uses face detection and color analysis to isolate the player from background.
"""

import os
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
from scipy import ndimage

def detect_player_content(img, face_region_boost=True):
    """
    Detect player content using multiple methods including face detection simulation.
    """
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    
    # Method 1: Very aggressive white removal
    # White pixels are those where all RGB values are high and similar
    rgb_diff = np.std(img_array, axis=2)  # Standard deviation across RGB channels
    white_mask = (img_array[:,:,0] > 200) & (img_array[:,:,1] > 200) & (img_array[:,:,2] > 200) & (rgb_diff < 30)
    
    # Method 2: Edge detection for content boundaries
    gray = np.mean(img_array, axis=2)
    edges = ndimage.sobel(gray)
    edge_threshold = np.percentile(edges, 80)  # More aggressive edge detection
    edge_mask = edges > edge_threshold
    
    # Method 3: Color diversity (player has more diverse colors than white background)
    # Calculate local color variance
    kernel_size = 20
    local_variance = ndimage.generic_filter(gray, np.var, size=kernel_size)
    variance_mask = local_variance > np.percentile(local_variance, 30)
    
    # Method 4: Focus on upper-middle region where face typically is
    face_region_mask = np.zeros_like(gray, dtype=bool)
    if face_region_boost:
        # Focus on the upper 60% and middle 70% of the image (typical face/body area)
        face_y_start = int(height * 0.1)
        face_y_end = int(height * 0.7)
        face_x_start = int(width * 0.1)
        face_x_end = int(width * 0.9)
        face_region_mask[face_y_start:face_y_end, face_x_start:face_x_end] = True
    
    # Method 5: Skin tone detection (approximate)
    # Look for colors that might be skin tones
    r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
    skin_mask = (
        (r > 100) & (r < 250) &  # Red component
        (g > 80) & (g < 200) &   # Green component  
        (b > 60) & (b < 180) &   # Blue component
        (r > g) & (g > b) &      # Red > Green > Blue (typical skin tone)
        (r - g > 20) & (g - b > 10)  # Additional skin tone constraints
    )
    
    # Combine all methods
    content_mask = (
        (~white_mask) &  # Not white
        (edge_mask | variance_mask | skin_mask) &  # Has edges, variance, or skin tones
        (face_region_mask if face_region_boost else True)  # In face region if enabled
    )
    
    # Clean up the mask
    from scipy.ndimage import binary_fill_holes, binary_erosion, binary_dilation
    
    # Fill holes
    content_mask = binary_fill_holes(content_mask)
    
    # Remove small noise
    content_mask = binary_erosion(content_mask, iterations=1)
    
    # Restore content
    content_mask = binary_dilation(content_mask, iterations=2)
    
    # Find the largest connected component
    labeled_array, num_features = ndimage.label(content_mask)
    if num_features > 0:
        component_sizes = ndimage.sum(content_mask, labeled_array, range(1, num_features + 1))
        largest_component = np.argmax(component_sizes) + 1
        content_mask = (labeled_array == largest_component)
    
    return content_mask

def extract_player_photo_aggressive(input_path, output_path, player_name="afthab"):
    """
    Very aggressive player photo extraction.
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
        
        # Crop the left half
        crop_width = width // 2
        left_crop = img.crop((0, 0, crop_width, height))
        
        print(f"Cropped image size: {left_crop.size}")
        
        # Detect player content
        print("Detecting player content with aggressive methods...")
        content_mask = detect_player_content(left_crop, face_region_boost=True)
        
        if not np.any(content_mask):
            print("No player content detected")
            return False
        
        # Find bounding box of detected content
        rows = np.any(content_mask, axis=0)
        cols = np.any(content_mask, axis=1)
        
        if not np.any(rows) or not np.any(cols):
            print("No valid content boundaries found")
            return False
        
        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]
        
        print(f"Detected content bounding box: x({x_min}, {x_max}), y({y_min}, {y_max})")
        
        # Add generous padding
        padding = 50
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(crop_width, x_max + padding)
        y_max = min(height, y_max + padding)
        
        # Crop to the detected content
        player_photo = left_crop.crop((x_min, y_min, x_max, y_max))
        
        # Apply additional processing to enhance the player
        # Increase contrast slightly
        enhancer = ImageEnhance.Contrast(player_photo)
        player_photo = enhancer.enhance(1.1)
        
        # Slight sharpening
        player_photo = player_photo.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
        
        print(f"Final player photo size: {player_photo.size}")
        
        # Save the result
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
    output_path = os.path.join(output_dir, f"{player_name}_aggressive.png")
    
    # Check if input image exists
    if not os.path.exists(input_path):
        print(f"Error: Input image not found at {input_path}")
        return
    
    print(f"Extracting player photo with aggressive background removal...")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print("-" * 50)
    
    # Extract player photo
    success = extract_player_photo_aggressive(input_path, output_path, player_name)
    
    if success:
        print("\n✅ Aggressive player photo extraction completed!")
    else:
        print("\n❌ Player photo extraction failed!")

if __name__ == "__main__":
    main()
