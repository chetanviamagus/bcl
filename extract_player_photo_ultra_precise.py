#!/usr/bin/env python3
"""
Ultra-precise player photo extraction with advanced white edge removal.
Focuses on removing white halos and creating clean, sharp edges.
"""

import os
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
from scipy import ndimage

def remove_white_halo_advanced(img, white_threshold=220, edge_sensitivity=0.3):
    """
    Advanced white halo removal using edge detection and alpha channel masking.
    """
    # Convert to numpy array
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    
    # Create alpha channel for transparency
    alpha = np.ones((height, width), dtype=np.uint8) * 255
    
    # Method 1: Detect white/light areas more precisely
    # White areas have high RGB values and low color variance
    rgb_mean = np.mean(img_array, axis=2)
    rgb_std = np.std(img_array, axis=2)
    
    # White detection: high mean RGB and low standard deviation
    white_mask = (rgb_mean > white_threshold) & (rgb_std < 25)
    
    # Method 2: Edge detection to find content boundaries
    gray = np.mean(img_array, axis=2)
    
    # Use multiple edge detection methods
    sobel_x = ndimage.sobel(gray, axis=1)
    sobel_y = ndimage.sobel(gray, axis=0)
    sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    
    # Laplacian for additional edge detection
    laplacian = ndimage.laplace(gray)
    
    # Combine edge detection methods
    edge_threshold = np.percentile(sobel_magnitude, 85)
    edge_mask = (sobel_magnitude > edge_threshold) | (np.abs(laplacian) > np.percentile(np.abs(laplacian), 80))
    
    # Method 3: Color gradient analysis
    # Look for areas where color changes significantly (content vs background)
    color_gradient = np.sqrt(sobel_x**2 + sobel_y**2)
    gradient_mask = color_gradient > np.percentile(color_gradient, 70)
    
    # Method 4: Local color variance (content has more color variation)
    kernel_size = 15
    local_variance = ndimage.generic_filter(gray, np.var, size=kernel_size)
    variance_threshold = np.percentile(local_variance, 40)
    variance_mask = local_variance > variance_threshold
    
    # Method 5: Skin tone and hair detection
    r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
    
    # Skin tone detection (more precise)
    skin_mask = (
        (r > 120) & (r < 240) &
        (g > 100) & (g < 220) &
        (b > 80) & (b < 200) &
        (r > g) & (g > b) &
        (r - g > 15) & (g - b > 10) &
        (rgb_std > 15)  # Some color variation
    )
    
    # Hair detection (dark areas with some texture)
    hair_mask = (
        (rgb_mean < 100) &  # Dark
        (rgb_std > 10) &    # Some texture
        (sobel_magnitude > np.percentile(sobel_magnitude, 60))  # Has edges
    )
    
    # Method 6: Clothing detection (non-white clothing)
    clothing_mask = (
        (rgb_mean < 200) &  # Not too bright
        (rgb_std > 20) &    # Has color variation
        (sobel_magnitude > np.percentile(sobel_magnitude, 50))  # Has texture
    )
    
    # Combine all content detection methods
    content_mask = (
        (~white_mask) &  # Not white
        (edge_mask | gradient_mask | variance_mask | skin_mask | hair_mask | clothing_mask)
    )
    
    # Clean up the mask with morphological operations
    from scipy.ndimage import binary_fill_holes, binary_erosion, binary_dilation
    
    # Fill holes in the content
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
    
    # Create alpha channel based on content mask
    # Use a soft edge for better blending
    alpha = np.where(content_mask, 255, 0).astype(np.uint8)
    
    # Apply edge softening to reduce harsh edges
    alpha_soft = ndimage.gaussian_filter(alpha.astype(float), sigma=1.0)
    alpha = np.clip(alpha_soft, 0, 255).astype(np.uint8)
    
    # Create RGBA image
    rgba_array = np.dstack([img_array, alpha])
    result = Image.fromarray(rgba_array, 'RGBA')
    
    return result

def extract_player_photo_ultra_precise(input_path, output_path, player_name="afthab"):
    """
    Ultra-precise player photo extraction with advanced white edge removal.
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
        
        # Apply ultra-precise white halo removal
        print("Applying ultra-precise white edge removal...")
        processed_img = remove_white_halo_advanced(left_crop, white_threshold=200, edge_sensitivity=0.3)
        
        # Find the bounding box of non-transparent content
        alpha_channel = np.array(processed_img)[:, :, 3]
        non_transparent = alpha_channel > 50  # Pixels with alpha > 50
        
        if not np.any(non_transparent):
            print("No content found after processing")
            return False
        
        # Find bounding box
        rows = np.any(non_transparent, axis=1)
        cols = np.any(non_transparent, axis=0)
        
        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]
        
        print(f"Content bounding box: x({x_min}, {x_max}), y({y_min}, {y_max})")
        
        # Add padding
        padding = 40
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(crop_width, x_max + padding)
        y_max = min(height, y_max + padding)
        
        # Final crop
        final_photo = processed_img.crop((x_min, y_min, x_max, y_max))
        
        # Convert to RGB with white background for final output
        if final_photo.mode == 'RGBA':
            # Create white background
            white_bg = Image.new('RGB', final_photo.size, (255, 255, 255))
            # Paste with alpha blending
            white_bg.paste(final_photo, mask=final_photo.split()[-1])
            final_photo = white_bg
        
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
    output_path = os.path.join(output_dir, f"{player_name}_ultra_precise.png")
    
    # Check if input image exists
    if not os.path.exists(input_path):
        print(f"Error: Input image not found at {input_path}")
        return
    
    print(f"Extracting player photo with ultra-precise white edge removal...")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print("-" * 50)
    
    # Extract player photo
    success = extract_player_photo_ultra_precise(input_path, output_path, player_name)
    
    if success:
        print("\n✅ Ultra-precise player photo extraction completed!")
    else:
        print("\n❌ Player photo extraction failed!")

if __name__ == "__main__":
    main()
