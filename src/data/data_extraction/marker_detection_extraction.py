#!/usr/bin/env python3
"""
Advanced Marker Detection Player Photo Extraction
Detects white frames with black corner markers to extract player photos
"""

import json
import os
import re
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw
import io
import numpy as np
import cv2

def marker_detection_extract_player_photos():
    """Extract player photos by detecting visual crop markers"""
    
    print("🎯 Advanced Marker Detection Player Photo Extraction")
    print("=" * 60)
    
    # Paths
    pdf_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/New-2025-BCL-Players.pptx.pdf'
    data_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/complete_pdf_players_data.json'
    output_dir = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/players'
    
    # Backup current images
    backup_dir = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/players_backup_v3'
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
            
            # Extract image with marker detection
            success = extract_with_marker_detection(doc, page_num, player, output_dir)
            
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

def extract_with_marker_detection(doc, page_num, player, output_dir):
    """Extract image using visual marker detection"""
    
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
            
            # Apply marker detection cropping
            cropped_image = detect_and_crop_markers(pil_image, page_num)
            
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

def detect_and_crop_markers(image, page_num):
    """Detect visual crop markers and extract the region within"""
    
    try:
        # Convert PIL to OpenCV format
        img_array = np.array(image)
        
        # Convert RGB to BGR for OpenCV
        if len(img_array.shape) == 3:
            img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_cv = img_array
        
        # Strategy 1: Detect white frame with black corner markers
        frame_crop = detect_white_frame_markers(img_cv, image)
        if frame_crop:
            return frame_crop
        
        # Strategy 2: Detect rectangular borders
        border_crop = detect_rectangular_borders(img_cv, image)
        if border_crop:
            return border_crop
        
        # Strategy 3: Detect corner markers specifically
        corner_crop = detect_corner_markers(img_cv, image)
        if corner_crop:
            return corner_crop
        
        # Strategy 4: Detect high contrast rectangular regions
        contrast_crop = detect_high_contrast_rectangles(img_cv, image)
        if contrast_crop:
            return contrast_crop
        
        # Fallback: Enhanced face detection
        return enhanced_face_detection(image)
    
    except Exception as e:
        print(f"   ⚠️  Marker detection error: {e}")
        return enhanced_face_detection(image)

def detect_white_frame_markers(img_cv, image):
    """Detect white frames with black corner markers"""
    
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Use adaptive threshold to detect edges
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Look for rectangular contours that could be frames
        best_contour = None
        best_score = 0
        
        for contour in contours:
            # Approximate the contour
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Check if it's roughly rectangular (4 corners)
            if len(approx) >= 4:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                area = cv2.contourArea(contour)
                rect_area = w * h
                
                # Calculate aspect ratio and fill ratio
                aspect_ratio = w / h if h > 0 else 0
                fill_ratio = area / rect_area if rect_area > 0 else 0
                
                # Score based on being roughly square and well-filled
                if (0.7 <= aspect_ratio <= 1.3 and  # Roughly square
                    fill_ratio > 0.3 and  # Well-filled
                    w > 100 and h > 100 and  # Minimum size
                    w < img_cv.shape[1] * 0.8 and h < img_cv.shape[0] * 0.8):  # Not too large
                    
                    # Additional check: look for white frame characteristics
                    roi = gray[y:y+h, x:x+w]
                    mean_intensity = np.mean(roi)
                    
                    # Score higher for frames that are bright (white)
                    score = fill_ratio * (mean_intensity / 255.0)
                    
                    if score > best_score:
                        best_score = score
                        best_contour = (x, y, w, h)
        
        if best_contour:
            x, y, w, h = best_contour
            # Expand slightly to capture the full frame content
            margin = 10
            x = max(0, x - margin)
            y = max(0, y - margin)
            w = min(img_cv.shape[1] - x, w + 2 * margin)
            h = min(img_cv.shape[0] - y, h + 2 * margin)
            
            cropped = image.crop((x, y, x + w, y + h))
            if cropped.width >= 100 and cropped.height >= 100:
                print(f"   🎯 Found white frame marker: {w}x{h}")
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  White frame detection error: {e}")
        return None

def detect_rectangular_borders(img_cv, image):
    """Detect rectangular borders using edge detection"""
    
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply Canny edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Look for rectangular contours
        best_rect = None
        best_area = 0
        
        for contour in contours:
            # Approximate contour
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Check if it's roughly rectangular
            if len(approx) >= 4:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                area = cv2.contourArea(contour)
                
                # Filter for reasonable rectangles
                if (w > 80 and h > 80 and  # Minimum size
                    w < img_cv.shape[1] * 0.7 and h < img_cv.shape[0] * 0.7 and  # Not too large
                    area > best_area):  # Larger area (likely the main frame)
                    
                    best_area = area
                    best_rect = (x, y, w, h)
        
        if best_rect:
            x, y, w, h = best_rect
            cropped = image.crop((x, y, x + w, y + h))
            if cropped.width >= 100 and cropped.height >= 100:
                print(f"   📐 Found rectangular border: {w}x{h}")
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  Rectangular border detection error: {e}")
        return None

def detect_corner_markers(img_cv, image):
    """Detect corner markers specifically"""
    
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Use corner detection (Harris corners)
        corners = cv2.cornerHarris(gray, 2, 3, 0.04)
        corners = cv2.dilate(corners, None)
        
        # Find corner points
        corner_points = np.where(corners > 0.01 * corners.max())
        corner_coords = list(zip(corner_points[1], corner_points[0]))  # (x, y)
        
        if len(corner_coords) >= 4:
            # Group nearby corners and find the best rectangular region
            best_region = find_best_corner_region(corner_coords, img_cv.shape)
            
            if best_region:
                x, y, w, h = best_region
                cropped = image.crop((x, y, x + w, y + h))
                if cropped.width >= 100 and cropped.height >= 100:
                    print(f"   🔲 Found corner markers: {w}x{h}")
                    return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  Corner marker detection error: {e}")
        return None

def find_best_corner_region(corner_coords, img_shape):
    """Find the best rectangular region from corner coordinates"""
    
    try:
        if len(corner_coords) < 4:
            return None
        
        # Sort corners by position
        corners = sorted(corner_coords, key=lambda p: (p[1], p[0]))  # Sort by y, then x
        
        # Find potential rectangular regions
        best_region = None
        best_area = 0
        
        # Try different combinations of corners
        for i in range(len(corners) - 3):
            for j in range(i + 1, len(corners) - 2):
                for k in range(j + 1, len(corners) - 1):
                    for l in range(k + 1, len(corners)):
                        # Get 4 corners
                        p1, p2, p3, p4 = corners[i], corners[j], corners[k], corners[l]
                        
                        # Calculate bounding rectangle
                        x_coords = [p[0] for p in [p1, p2, p3, p4]]
                        y_coords = [p[1] for p in [p1, p2, p3, p4]]
                        
                        x_min, x_max = min(x_coords), max(x_coords)
                        y_min, y_max = min(y_coords), max(y_coords)
                        
                        w = x_max - x_min
                        h = y_max - y_min
                        
                        # Check if this forms a reasonable rectangle
                        if (w > 100 and h > 100 and  # Minimum size
                            w < img_shape[1] * 0.8 and h < img_shape[0] * 0.8 and  # Not too large
                            w * h > best_area):  # Larger area
                            
                            best_area = w * h
                            best_region = (x_min, y_min, w, h)
        
        return best_region
    
    except Exception as e:
        print(f"   ⚠️  Corner region finding error: {e}")
        return None

def detect_high_contrast_rectangles(img_cv, image):
    """Detect high contrast rectangular regions"""
    
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Calculate local contrast using standard deviation
        kernel_size = 15
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
        mean = cv2.filter2D(gray.astype(np.float32), -1, kernel)
        sqr_mean = cv2.filter2D((gray.astype(np.float32)) ** 2, -1, kernel)
        contrast = np.sqrt(np.maximum(sqr_mean - mean ** 2, 0))
        
        # Find regions with high contrast
        high_contrast = contrast > np.percentile(contrast, 80)
        
        # Find contours in high contrast regions
        high_contrast_uint8 = (high_contrast * 255).astype(np.uint8)
        contours, _ = cv2.findContours(high_contrast_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        best_rect = None
        best_score = 0
        
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            rect_area = w * h
            
            if rect_area > 0:
                fill_ratio = area / rect_area
                aspect_ratio = w / h if h > 0 else 0
                
                # Score based on size, aspect ratio, and fill ratio
                if (100 <= w <= img_cv.shape[1] * 0.7 and
                    100 <= h <= img_cv.shape[0] * 0.7 and
                    0.7 <= aspect_ratio <= 1.3):  # Roughly square
                    
                    score = fill_ratio * (rect_area / (img_cv.shape[0] * img_cv.shape[1]))
                    
                    if score > best_score:
                        best_score = score
                        best_rect = (x, y, w, h)
        
        if best_rect:
            x, y, w, h = best_rect
            cropped = image.crop((x, y, x + w, y + h))
            if cropped.width >= 100 and cropped.height >= 100:
                print(f"   ⚡ Found high contrast rectangle: {w}x{h}")
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  High contrast rectangle detection error: {e}")
        return None

def enhanced_face_detection(image):
    """Enhanced fallback face detection"""
    
    try:
        width, height = image.size
        
        # Focus on upper portion where faces typically are
        upper_ratio = 0.6
        upper_height = int(height * upper_ratio)
        
        # Create a crop focusing on the upper portion
        left = 0
        top = 0
        right = width
        bottom = upper_height
        
        cropped = image.crop((left, top, right, bottom))
        
        # Further crop to create a square or portrait format
        if cropped.width > cropped.height:
            # Landscape - center crop to portrait
            new_width = cropped.height
            left_offset = (cropped.width - new_width) // 2
            cropped = cropped.crop((left_offset, 0, left_offset + new_width, cropped.height))
        
        if cropped.width >= 100 and cropped.height >= 100:
            print(f"   👤 Using enhanced face detection fallback: {cropped.size[0]}x{cropped.size[1]}")
            return cropped
        
        return image
    
    except Exception as e:
        print(f"   ⚠️  Enhanced face detection error: {e}")
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
    marker_detection_extract_player_photos()
