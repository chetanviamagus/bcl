#!/usr/bin/env python3
"""
Improved Player Photo Extraction with Better Cropping
"""

import json
import os
import re
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image, ImageOps
import io
import numpy as np

def improved_extract_player_photos():
    """Extract player photos with improved cropping"""
    
    print("📸 Improved Player Photo Extraction")
    print("=" * 50)
    
    # Paths
    pdf_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/New-2025-BCL-Players.pptx.pdf'
    data_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/complete_pdf_players_data.json'
    output_dir = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/players'
    
    # Backup existing images
    backup_dir = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/players_backup'
    if os.path.exists(output_dir) and not os.path.exists(backup_dir):
        os.rename(output_dir, backup_dir)
        print(f"📁 Backed up existing images to: {backup_dir}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    # Load player data
    with open(data_path, 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print(f"📊 Loaded {len(players_data)} players")
    
    try:
        # Open PDF
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        print(f"📄 PDF has {total_pages} pages")
        
        extracted_count = 0
        failed_count = 0
        
        # Process each player
        for i, player in enumerate(players_data):
            slide_num = player['slide_number']
            page_num = slide_num - 1  # Convert to 0-based index
            
            if page_num >= total_pages:
                print(f"⚠️  Slide {slide_num} beyond PDF range")
                continue
            
            print(f"\\n🔍 Processing slide {slide_num} ({i+1}/{len(players_data)}): {player['name']}")
            
            # Extract image with improved cropping
            success = extract_and_crop_player_photo(doc, page_num, player, output_dir)
            
            if success:
                extracted_count += 1
                print(f"✅ Extracted photo for {player['name']}")
            else:
                failed_count += 1
                print(f"❌ Failed to extract photo for {player['name']}")
        
        doc.close()
        
        print(f"\\n📊 Extraction Summary:")
        print(f"  Total players processed: {len(players_data)}")
        print(f"  Successfully extracted: {extracted_count}")
        print(f"  Failed extractions: {failed_count}")
        print(f"  Images saved to: {output_dir}")
        
        return extracted_count, failed_count
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0, 0

def extract_and_crop_player_photo(doc, page_num, player, output_dir):
    """Extract and intelligently crop player photo"""
    
    try:
        page = doc[page_num]
        
        # Get images on the page
        image_list = page.get_images(full=True)
        
        if not image_list:
            print(f"   No images found on page {page_num + 1}")
            return False
        
        # Process each image on the page
        for img_index, img in enumerate(image_list):
            # Get image data
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            
            # Skip if image is too small
            if pix.width < 50 or pix.height < 50:
                pix = None
                continue
            
            # Convert to PIL Image
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                img_data = pix.tobytes("png")
                pil_image = Image.open(io.BytesIO(img_data))
            else:  # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                img_data = pix1.tobytes("png")
                pil_image = Image.open(io.BytesIO(img_data))
                pix1 = None
            
            pix = None
            
            # Apply intelligent cropping
            cropped_image = intelligent_crop_player_photo(pil_image, page_num)
            
            if cropped_image:
                # Generate filename
                filename = generate_filename(player)
                filepath = os.path.join(output_dir, filename)
                
                # Save image
                cropped_image.save(filepath, 'PNG', quality=95)
                
                print(f"   💾 Saved: {filename} ({cropped_image.size[0]}x{cropped_image.size[1]})")
                return True
        
        return False
    
    except Exception as e:
        print(f"   ❌ Error processing page {page_num + 1}: {e}")
        return False

def intelligent_crop_player_photo(image, page_num):
    """Intelligently crop to find player photo area"""
    
    try:
        width, height = image.size
        
        # Convert to numpy array for analysis
        img_array = np.array(image)
        
        # Strategy 1: Find the largest connected component (likely the player photo)
        best_crop = find_largest_component_crop(image, img_array)
        if best_crop:
            return best_crop
        
        # Strategy 2: Edge detection based cropping
        edge_crop = edge_detection_crop(image, img_array)
        if edge_crop:
            return edge_crop
        
        # Strategy 3: Color variance based cropping
        variance_crop = variance_based_crop(image, img_array)
        if variance_crop:
            return variance_crop
        
        # Strategy 4: Aspect ratio based cropping (common for player photos)
        aspect_crop = aspect_ratio_crop(image)
        if aspect_crop:
            return aspect_crop
        
        # Fallback: Smart center crop
        return smart_center_crop(image)
    
    except Exception as e:
        print(f"   ⚠️  Intelligent crop error: {e}")
        return image

def find_largest_component_crop(image, img_array):
    """Find and crop the largest connected component"""
    
    try:
        # Convert to grayscale
        gray = ImageOps.grayscale(image)
        gray_array = np.array(gray)
        
        # Apply threshold to separate foreground from background
        threshold = np.mean(gray_array) * 0.8
        binary = gray_array > threshold
        
        # Find contours (simplified approach)
        # Look for rectangular regions with high content
        height, width = binary.shape
        
        # Scan for the largest rectangular region with significant content
        best_region = None
        best_score = 0
        
        # Try different crop regions
        for crop_ratio in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
            crop_w = int(width * crop_ratio)
            crop_h = int(height * crop_ratio)
            
            # Try center crop
            left = (width - crop_w) // 2
            top = (height - crop_h) // 2
            right = left + crop_w
            bottom = top + crop_h
            
            if left >= 0 and top >= 0 and right <= width and bottom <= height:
                region = binary[top:bottom, left:right]
                score = np.sum(region) / (crop_w * crop_h)
                
                if score > best_score and score > 0.1:  # At least 10% content
                    best_score = score
                    best_region = (left, top, right, bottom)
        
        if best_region:
            left, top, right, bottom = best_region
            cropped = image.crop((left, top, right, bottom))
            
            # Ensure reasonable size
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  Component crop error: {e}")
        return None

def edge_detection_crop(image, img_array):
    """Crop based on edge detection"""
    
    try:
        # Convert to grayscale
        gray = ImageOps.grayscale(image)
        gray_array = np.array(gray)
        
        # Simple edge detection using gradient
        # Calculate gradients
        grad_x = np.abs(np.gradient(gray_array, axis=1))
        grad_y = np.abs(np.gradient(gray_array, axis=0))
        
        # Combine gradients
        edges = np.sqrt(grad_x**2 + grad_y**2)
        
        # Find regions with high edge density
        height, width = edges.shape
        
        # Look for rectangular regions with high edge content
        best_region = None
        best_score = 0
        
        for crop_ratio in [0.4, 0.5, 0.6, 0.7]:
            crop_w = int(width * crop_ratio)
            crop_h = int(height * crop_ratio)
            
            # Try center crop
            left = (width - crop_w) // 2
            top = (height - crop_h) // 2
            right = left + crop_w
            bottom = top + crop_h
            
            if left >= 0 and top >= 0 and right <= width and bottom <= height:
                region = edges[top:bottom, left:right]
                score = np.mean(region)
                
                if score > best_score:
                    best_score = score
                    best_region = (left, top, right, bottom)
        
        if best_region:
            left, top, right, bottom = best_region
            cropped = image.crop((left, top, right, bottom))
            
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  Edge detection crop error: {e}")
        return None

def variance_based_crop(image, img_array):
    """Crop based on color variance (content richness)"""
    
    try:
        height, width = img_array.shape[:2]
        
        # Calculate local variance
        step = 20
        best_region = None
        best_variance = 0
        
        for y in range(0, height - step, step):
            for x in range(0, width - step, step):
                # Get region
                region = img_array[y:y+step, x:x+step]
                
                # Calculate variance
                if len(region.shape) == 3:  # RGB
                    variance = np.var(region.reshape(-1, 3), axis=0).mean()
                else:  # Grayscale
                    variance = np.var(region)
                
                if variance > best_variance:
                    best_variance = variance
                    # Define crop region around this point
                    crop_size = min(400, width - x, height - y)
                    left = max(0, x - crop_size//2)
                    top = max(0, y - crop_size//2)
                    right = min(width, left + crop_size)
                    bottom = min(height, top + crop_size)
                    
                    if right - left >= 100 and bottom - top >= 100:
                        best_region = (left, top, right, bottom)
        
        if best_region:
            left, top, right, bottom = best_region
            cropped = image.crop((left, top, right, bottom))
            
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  Variance crop error: {e}")
        return None

def aspect_ratio_crop(image):
    """Crop based on common player photo aspect ratios"""
    
    width, height = image.size
    
    # Common player photo aspect ratios: square, 3:4, 4:3
    aspect_ratios = [
        (1, 1),      # Square
        (3, 4),      # Portrait
        (4, 3),      # Landscape
        (2, 3),      # Tall portrait
        (3, 2),      # Wide landscape
    ]
    
    for ratio_w, ratio_h in aspect_ratios:
        # Calculate crop size based on aspect ratio
        if width * ratio_h > height * ratio_w:
            # Height is limiting
            crop_h = height
            crop_w = int(height * ratio_w / ratio_h)
        else:
            # Width is limiting
            crop_w = width
            crop_h = int(width * ratio_h / ratio_w)
        
        # Ensure minimum size
        if crop_w < 200 or crop_h < 200:
            continue
        
        # Center the crop
        left = (width - crop_w) // 2
        top = (height - crop_h) // 2
        right = left + crop_w
        bottom = top + crop_h
        
        if left >= 0 and top >= 0 and right <= width and bottom <= height:
            cropped = image.crop((left, top, right, bottom))
            
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
    
    return None

def smart_center_crop(image):
    """Smart center crop with better sizing"""
    
    width, height = image.size
    
    # Try different crop ratios, prioritizing square and portrait
    crop_ratios = [0.6, 0.7, 0.8]
    
    for ratio in crop_ratios:
        crop_w = int(width * ratio)
        crop_h = int(height * ratio)
        
        # Center the crop
        left = (width - crop_w) // 2
        top = (height - crop_h) // 2
        right = left + crop_w
        bottom = top + crop_h
        
        if left >= 0 and top >= 0 and right <= width and bottom <= height:
            cropped = image.crop((left, top, right, bottom))
            
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
    
    # Fallback to original if all else fails
    return image

def generate_filename(player):
    """Generate filename in format: Name-Age-Category-Mobile"""
    
    # Clean name (replace spaces and special chars with hyphens)
    name = re.sub(r'[^a-zA-Z0-9]', '-', player['name'].strip())
    name = re.sub(r'-+', '-', name).strip('-')
    
    # Clean category
    category = re.sub(r'[^a-zA-Z0-9]', '-', player['category'].strip())
    category = re.sub(r'-+', '-', category).strip('-')
    
    # Get age and mobile
    age = player.get('age', '0')
    mobile = player.get('mobile', '0000000000')
    
    # Generate filename
    filename = f"{name}-{age}-{category}-{mobile}.png"
    
    # Ensure filename is not too long
    if len(filename) > 100:
        # Truncate name if needed
        max_name_length = 100 - len(f"-{age}-{category}-{mobile}.png")
        name = name[:max_name_length]
        filename = f"{name}-{age}-{category}-{mobile}.png"
    
    return filename

if __name__ == "__main__":
    improved_extract_player_photos()
