#!/usr/bin/env python3
"""
Face-Focused Player Photo Extraction
Uses advanced techniques to detect and crop player faces
"""

import json
import os
import re
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import io
import numpy as np

def face_focused_extract_player_photos():
    """Extract player photos with face-focused cropping"""
    
    print("👤 Face-Focused Player Photo Extraction")
    print("=" * 50)
    
    # Paths
    pdf_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/New-2025-BCL-Players.pptx.pdf'
    data_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/complete_pdf_players_data.json'
    output_dir = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/players'
    
    # Backup current images
    backup_dir = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/players_backup_v2'
    if os.path.exists(output_dir) and not os.path.exists(backup_dir):
        import shutil
        shutil.copytree(output_dir, backup_dir)
        print(f"📁 Backed up current images to: {backup_dir}")
    
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
            
            # Extract image with face-focused cropping
            success = extract_face_focused_photo(doc, page_num, player, output_dir)
            
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

def extract_face_focused_photo(doc, page_num, player, output_dir):
    """Extract and crop focusing on facial features"""
    
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
            if pix.width < 100 or pix.height < 100:
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
            
            # Apply face-focused cropping
            cropped_image = face_focused_crop(pil_image, page_num)
            
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

def face_focused_crop(image, page_num):
    """Crop image focusing on facial features"""
    
    try:
        width, height = image.size
        
        # Convert to numpy array for analysis
        img_array = np.array(image)
        
        # Strategy 1: Skin tone detection and face region finding
        face_crop = detect_face_region(image, img_array)
        if face_crop:
            return face_crop
        
        # Strategy 2: Eye/feature detection
        feature_crop = detect_facial_features(image, img_array)
        if feature_crop:
            return feature_crop
        
        # Strategy 3: Portrait-style cropping (upper portion focus)
        portrait_crop = portrait_style_crop(image)
        if portrait_crop:
            return portrait_crop
        
        # Strategy 4: Brightness and contrast analysis
        contrast_crop = contrast_based_crop(image, img_array)
        if contrast_crop:
            return contrast_crop
        
        # Fallback: Smart upper crop (faces are usually in upper portion)
        return smart_upper_crop(image)
    
    except Exception as e:
        print(f"   ⚠️  Face-focused crop error: {e}")
        return image

def detect_face_region(image, img_array):
    """Detect face region using skin tone and shape analysis"""
    
    try:
        # Convert to HSV for better skin tone detection
        hsv = np.array(image.convert('HSV'))
        
        # Define skin tone ranges in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Create skin mask
        skin_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for i in range(hsv.shape[0]):
            for j in range(hsv.shape[1]):
                pixel = hsv[i, j]
                if (lower_skin[0] <= pixel[0] <= upper_skin[0] and
                    lower_skin[1] <= pixel[1] <= upper_skin[1] and
                    lower_skin[2] <= pixel[2] <= upper_skin[2]):
                    skin_mask[i, j] = 255
        
        # Find contours in skin mask
        height, width = skin_mask.shape
        
        # Look for the largest skin region (likely face)
        best_region = None
        best_size = 0
        
        # Scan for skin regions
        for y in range(0, height - 50, 20):
            for x in range(0, width - 50, 20):
                # Check region around this point
                region_size = 100
                end_y = min(y + region_size, height)
                end_x = min(x + region_size, width)
                
                skin_pixels = np.sum(skin_mask[y:end_y, x:end_x])
                region_area = (end_y - y) * (end_x - x)
                skin_ratio = skin_pixels / region_area if region_area > 0 else 0
                
                # If significant skin content, this might be a face
                if skin_ratio > 0.1 and skin_pixels > best_size:
                    best_size = skin_pixels
                    # Expand region to capture full face
                    face_size = min(300, width - x, height - y)
                    left = max(0, x - face_size//4)
                    top = max(0, y - face_size//4)
                    right = min(width, left + face_size)
                    bottom = min(height, top + face_size)
                    
                    if right - left >= 100 and bottom - top >= 100:
                        best_region = (left, top, right, bottom)
        
        if best_region:
            left, top, right, bottom = best_region
            cropped = image.crop((left, top, right, bottom))
            
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  Face region detection error: {e}")
        return None

def detect_facial_features(image, img_array):
    """Detect facial features using edge and texture analysis"""
    
    try:
        # Convert to grayscale
        gray = ImageOps.grayscale(image)
        gray_array = np.array(gray)
        
        # Apply edge detection
        edges = np.abs(np.gradient(gray_array, axis=1)) + np.abs(np.gradient(gray_array, axis=0))
        
        # Look for regions with high edge density (eyes, nose, mouth)
        height, width = edges.shape
        
        # Focus on upper portion where faces typically are
        upper_height = int(height * 0.6)  # Focus on upper 60%
        
        best_region = None
        best_edge_density = 0
        
        # Scan upper portion for high edge density regions
        for y in range(0, upper_height - 100, 30):
            for x in range(0, width - 100, 30):
                # Check region
                region_size = 150
                end_y = min(y + region_size, upper_height)
                end_x = min(x + region_size, width)
                
                region_edges = edges[y:end_y, x:end_x]
                edge_density = np.mean(region_edges)
                
                if edge_density > best_edge_density:
                    best_edge_density = edge_density
                    # Expand to capture full face
                    face_size = min(250, width - x, upper_height - y)
                    left = max(0, x - face_size//4)
                    top = max(0, y - face_size//4)
                    right = min(width, left + face_size)
                    bottom = min(height, top + face_size)
                    
                    if right - left >= 100 and bottom - top >= 100:
                        best_region = (left, top, right, bottom)
        
        if best_region:
            left, top, right, bottom = best_region
            cropped = image.crop((left, top, right, bottom))
            
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  Facial feature detection error: {e}")
        return None

def portrait_style_crop(image):
    """Portrait-style cropping focusing on upper portion"""
    
    width, height = image.size
    
    # Portrait crops (focus on upper portion where faces are)
    portrait_ratios = [
        (3, 4),      # Classic portrait
        (2, 3),      # Tall portrait
        (4, 5),      # Slightly wide portrait
    ]
    
    for ratio_w, ratio_h in portrait_ratios:
        # Calculate crop size
        if width * ratio_h > height * ratio_w:
            crop_h = height
            crop_w = int(height * ratio_w / ratio_h)
        else:
            crop_w = width
            crop_h = int(width * ratio_h / ratio_w)
        
        # Focus on upper portion (where faces typically are)
        left = (width - crop_w) // 2
        top = max(0, int(height * 0.1))  # Start from 10% down from top
        right = left + crop_w
        bottom = min(height, top + crop_h)
        
        if right <= width and bottom <= height and crop_w >= 150 and crop_h >= 150:
            cropped = image.crop((left, top, right, bottom))
            
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
    
    return None

def contrast_based_crop(image, img_array):
    """Crop based on contrast analysis (faces have high contrast)"""
    
    try:
        # Convert to grayscale
        gray = ImageOps.grayscale(image)
        gray_array = np.array(gray)
        
        height, width = gray_array.shape
        
        # Calculate local contrast
        best_region = None
        best_contrast = 0
        
        # Focus on upper portion
        upper_height = int(height * 0.7)
        
        for y in range(0, upper_height - 100, 25):
            for x in range(0, width - 100, 25):
                # Check region
                region_size = 120
                end_y = min(y + region_size, upper_height)
                end_x = min(x + region_size, width)
                
                region = gray_array[y:end_y, x:end_x]
                
                # Calculate contrast (standard deviation)
                contrast = np.std(region)
                
                if contrast > best_contrast:
                    best_contrast = contrast
                    # Expand region
                    face_size = min(200, width - x, upper_height - y)
                    left = max(0, x - face_size//4)
                    top = max(0, y - face_size//4)
                    right = min(width, left + face_size)
                    bottom = min(height, top + face_size)
                    
                    if right - left >= 100 and bottom - top >= 100:
                        best_region = (left, top, right, bottom)
        
        if best_region:
            left, top, right, bottom = best_region
            cropped = image.crop((left, top, right, bottom))
            
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  Contrast-based crop error: {e}")
        return None

def smart_upper_crop(image):
    """Smart upper crop focusing on face area"""
    
    width, height = image.size
    
    # Focus on upper portion where faces typically are
    crop_ratios = [0.6, 0.7, 0.8]
    
    for ratio in crop_ratios:
        crop_w = int(width * ratio)
        crop_h = int(height * ratio)
        
        # Center horizontally, focus on upper portion vertically
        left = (width - crop_w) // 2
        top = max(0, int(height * 0.05))  # Start from 5% down from top
        right = left + crop_w
        bottom = min(height, top + crop_h)
        
        if left >= 0 and top >= 0 and right <= width and bottom <= height:
            cropped = image.crop((left, top, right, bottom))
            
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
    
    # Fallback to original
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
    face_focused_extract_player_photos()
