#!/usr/bin/env python3
"""
Advanced Marker Detection Player Photo Extraction
Specifically designed to detect visual crop markers (black corner frames) and extract the region within
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

def advanced_marker_detection_extract_first_page():
    """Extract player photo from first page using advanced marker detection"""
    
    print("🎯 Advanced Marker Detection - First Page Only")
    print("=" * 60)
    
    # Paths
    pdf_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/New-2025-BCL-Players.pptx.pdf'
    data_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/complete_pdf_players_data.json'
    output_dir = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/players'
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    # Load player data
    with open(data_path, 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print(f"📊 Loaded {len(players_data)} players")
    
    # Find first player (slide 1)
    first_player = None
    for player in players_data:
        if player['slide_number'] == 1:
            first_player = player
            break
    
    if not first_player:
        print("❌ No player found for slide 1")
        return False, 0
    
    print(f"🎯 Processing first player: {first_player['name']}")
    
    try:
        # Open PDF
        doc = fitz.open(pdf_path)
        print(f"📄 PDF has {doc.page_count} pages")
        
        # Process first page (page 0)
        success = extract_with_advanced_marker_detection(doc, 0, first_player, output_dir)
        
        doc.close()
        
        if success:
            print(f"✅ Successfully extracted photo for {first_player['name']}")
            return True, 1
        else:
            print(f"❌ Failed to extract photo for {first_player['name']}")
            return False, 0
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, 0

def extract_with_advanced_marker_detection(doc, page_num, player, output_dir):
    """Extract image using advanced visual marker detection"""
    
    try:
        page = doc[page_num]
        
        # Get images on the page
        image_list = page.get_images(full=True)
        
        if not image_list:
            print(f"   No images found on page {page_num + 1}")
            return False
        
        print(f"   Found {len(image_list)} images on page {page_num + 1}")
        
        # Process each image on the page
        for img_index, img in enumerate(image_list):
            print(f"   Processing image {img_index + 1}/{len(image_list)}")
            
            # Get image data
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            
            # Skip if image is too small
            if pix.width < 100 or pix.height < 100:
                print(f"   Skipping image {img_index + 1}: too small ({pix.width}x{pix.height})")
                pix = None
                continue
            
            print(f"   Image {img_index + 1} size: {pix.width}x{pix.height}")
            
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
            
            # Save original image for debugging
            debug_path = f"/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/debug_original_{img_index}.png"
            pil_image.save(debug_path)
            print(f"   💾 Saved original image for debugging: {debug_path}")
            
            # Apply advanced marker detection cropping
            cropped_image = detect_and_crop_visual_markers(pil_image, page_num, img_index)
            
            if cropped_image:
                # Generate filename
                filename = generate_filename(player)
                filepath = os.path.join(output_dir, filename)
                
                # Save image
                cropped_image.save(filepath, 'PNG', quality=95)
                
                print(f"   💾 Saved: {filename} ({cropped_image.size[0]}x{cropped_image.size[1]})")
                return True
            else:
                print(f"   ❌ No valid crop found for image {img_index + 1}")
        
        return False
    
    except Exception as e:
        print(f"   ❌ Error processing page {page_num + 1}: {e}")
        return False

def detect_and_crop_visual_markers(image, page_num, img_index):
    """Detect visual crop markers (black corner frames) and extract the region within"""
    
    try:
        print(f"   🔍 Analyzing image for visual markers...")
        
        # Convert PIL to OpenCV format
        img_array = np.array(image)
        
        # Convert RGB to BGR for OpenCV
        if len(img_array.shape) == 3:
            img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_cv = img_array
        
        # Strategy 1: Detect black corner markers specifically
        corner_crop = detect_black_corner_markers(img_cv, image, img_index)
        if corner_crop:
            return corner_crop
        
        # Strategy 2: Detect rectangular frames with high contrast borders
        frame_crop = detect_high_contrast_frames(img_cv, image, img_index)
        if frame_crop:
            return frame_crop
        
        # Strategy 3: Detect white frames with dark borders
        white_frame_crop = detect_white_frames_with_dark_borders(img_cv, image, img_index)
        if white_frame_crop:
            return white_frame_crop
        
        # Strategy 4: Detect rectangular regions with edge patterns
        edge_pattern_crop = detect_edge_pattern_rectangles(img_cv, image, img_index)
        if edge_pattern_crop:
            return edge_pattern_crop
        
        # Fallback: Enhanced center crop
        print(f"   ⚠️  No markers detected, using enhanced center crop")
        return enhanced_center_crop(image)
    
    except Exception as e:
        print(f"   ⚠️  Marker detection error: {e}")
        return enhanced_center_crop(image)

def detect_black_corner_markers(img_cv, image, img_index):
    """Detect black corner markers and extract the region within"""
    
    try:
        print(f"   🎯 Detecting black corner markers...")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Use adaptive threshold to detect dark regions
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        
        # Save threshold image for debugging
        debug_path = f"/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/debug_thresh_{img_index}.png"
        cv2.imwrite(debug_path, thresh)
        print(f"   💾 Saved threshold image: {debug_path}")
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        print(f"   Found {len(contours)} contours")
        
        # Look for rectangular contours that could be frames
        best_contour = None
        best_score = 0
        
        for i, contour in enumerate(contours):
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
                
                print(f"   Contour {i}: {w}x{h}, aspect={aspect_ratio:.2f}, fill={fill_ratio:.2f}")
                
                # Score based on being roughly square and well-filled
                if (0.7 <= aspect_ratio <= 1.3 and  # Roughly square
                    fill_ratio > 0.3 and  # Well-filled
                    w > 150 and h > 150 and  # Minimum size
                    w < img_cv.shape[1] * 0.8 and h < img_cv.shape[0] * 0.8):  # Not too large
                    
                    # Additional check: look for corner marker characteristics
                    # Check if corners have dark pixels (markers)
                    corner_score = check_corner_markers(gray, x, y, w, h)
                    
                    # Score higher for frames with corner markers
                    score = fill_ratio * (1 + corner_score) * (area / (img_cv.shape[0] * img_cv.shape[1]))
                    
                    print(f"   Contour {i} score: {score:.3f} (corner_score: {corner_score:.3f})")
                    
                    if score > best_score:
                        best_score = score
                        best_contour = (x, y, w, h)
        
        if best_contour:
            x, y, w, h = best_contour
            print(f"   🎯 Found best contour: {w}x{h} at ({x}, {y}) with score {best_score:.3f}")
            
            # Expand slightly to capture the full frame content
            margin = 15
            x = max(0, x - margin)
            y = max(0, y - margin)
            w = min(img_cv.shape[1] - x, w + 2 * margin)
            h = min(img_cv.shape[0] - y, h + 2 * margin)
            
            cropped = image.crop((x, y, x + w, y + h))
            if cropped.width >= 100 and cropped.height >= 100:
                print(f"   ✅ Successfully cropped: {cropped.size[0]}x{cropped.size[1]}")
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  Black corner marker detection error: {e}")
        return None

def check_corner_markers(gray, x, y, w, h):
    """Check if the corners have dark pixels (markers)"""
    
    try:
        # Define corner regions
        corner_size = min(20, w//10, h//10)
        
        # Top-left corner
        tl_region = gray[y:y+corner_size, x:x+corner_size]
        tl_dark = np.sum(tl_region < 50) / (corner_size * corner_size)
        
        # Top-right corner
        tr_region = gray[y:y+corner_size, x+w-corner_size:x+w]
        tr_dark = np.sum(tr_region < 50) / (corner_size * corner_size)
        
        # Bottom-left corner
        bl_region = gray[y+h-corner_size:y+h, x:x+corner_size]
        bl_dark = np.sum(bl_region < 50) / (corner_size * corner_size)
        
        # Bottom-right corner
        br_region = gray[y+h-corner_size:y+h, x+w-corner_size:x+w]
        br_dark = np.sum(br_region < 50) / (corner_size * corner_size)
        
        # Average dark pixel ratio in corners
        avg_dark = (tl_dark + tr_dark + bl_dark + br_dark) / 4
        
        return avg_dark
    
    except Exception as e:
        print(f"   ⚠️  Corner marker check error: {e}")
        return 0

def detect_high_contrast_frames(img_cv, image, img_index):
    """Detect rectangular frames with high contrast borders"""
    
    try:
        print(f"   🔍 Detecting high contrast frames...")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply Canny edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Save edge image for debugging
        debug_path = f"/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/debug_edges_{img_index}.png"
        cv2.imwrite(debug_path, edges)
        print(f"   💾 Saved edge image: {debug_path}")
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        print(f"   Found {len(contours)} edge contours")
        
        # Look for rectangular contours
        best_rect = None
        best_area = 0
        
        for i, contour in enumerate(contours):
            # Approximate contour
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Check if it's roughly rectangular
            if len(approx) >= 4:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                area = cv2.contourArea(contour)
                
                print(f"   Edge contour {i}: {w}x{h}, area={area}")
                
                # Filter for reasonable rectangles
                if (w > 100 and h > 100 and  # Minimum size
                    w < img_cv.shape[1] * 0.7 and h < img_cv.shape[0] * 0.7 and  # Not too large
                    area > best_area):  # Larger area (likely the main frame)
                    
                    best_area = area
                    best_rect = (x, y, w, h)
                    print(f"   New best edge contour: {w}x{h}")
        
        if best_rect:
            x, y, w, h = best_rect
            print(f"   📐 Found high contrast frame: {w}x{h}")
            cropped = image.crop((x, y, x + w, y + h))
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  High contrast frame detection error: {e}")
        return None

def detect_white_frames_with_dark_borders(img_cv, image, img_index):
    """Detect white frames with dark borders"""
    
    try:
        print(f"   🔍 Detecting white frames with dark borders...")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply morphological operations to enhance frame detection
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morph = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        
        # Use Otsu's threshold
        _, thresh = cv2.threshold(morph, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Save threshold image for debugging
        debug_path = f"/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/debug_white_{img_index}.png"
        cv2.imwrite(debug_path, thresh)
        print(f"   💾 Saved white frame threshold: {debug_path}")
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        print(f"   Found {len(contours)} white frame contours")
        
        # Look for rectangular contours
        best_rect = None
        best_score = 0
        
        for i, contour in enumerate(contours):
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            rect_area = w * h
            
            if rect_area > 0:
                fill_ratio = area / rect_area
                aspect_ratio = w / h if h > 0 else 0
                
                print(f"   White contour {i}: {w}x{h}, aspect={aspect_ratio:.2f}, fill={fill_ratio:.2f}")
                
                # Score based on size, aspect ratio, and fill ratio
                if (100 <= w <= img_cv.shape[1] * 0.7 and
                    100 <= h <= img_cv.shape[0] * 0.7 and
                    0.7 <= aspect_ratio <= 1.3 and  # Roughly square
                    fill_ratio > 0.3):  # Well-filled
                    
                    score = fill_ratio * (rect_area / (img_cv.shape[0] * img_cv.shape[1]))
                    
                    if score > best_score:
                        best_score = score
                        best_rect = (x, y, w, h)
                        print(f"   New best white frame: {w}x{h} (score: {score:.3f})")
        
        if best_rect:
            x, y, w, h = best_rect
            print(f"   ⚪ Found white frame: {w}x{h}")
            cropped = image.crop((x, y, x + w, y + h))
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  White frame detection error: {e}")
        return None

def detect_edge_pattern_rectangles(img_cv, image, img_index):
    """Detect rectangular regions with specific edge patterns"""
    
    try:
        print(f"   🔍 Detecting edge pattern rectangles...")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply Sobel edge detection
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        
        # Normalize
        sobel_magnitude = np.uint8(sobel_magnitude / sobel_magnitude.max() * 255)
        
        # Save Sobel image for debugging
        debug_path = f"/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/debug_sobel_{img_index}.png"
        cv2.imwrite(debug_path, sobel_magnitude)
        print(f"   💾 Saved Sobel image: {debug_path}")
        
        # Apply threshold to get strong edges
        _, edges = cv2.threshold(sobel_magnitude, 50, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        print(f"   Found {len(contours)} edge pattern contours")
        
        # Look for rectangular contours
        best_rect = None
        best_score = 0
        
        for i, contour in enumerate(contours):
            # Approximate contour
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Check if it's roughly rectangular
            if len(approx) >= 4:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                area = cv2.contourArea(contour)
                rect_area = w * h
                
                if rect_area > 0:
                    fill_ratio = area / rect_area
                    aspect_ratio = w / h if h > 0 else 0
                    
                    print(f"   Edge pattern contour {i}: {w}x{h}, aspect={aspect_ratio:.2f}, fill={fill_ratio:.2f}")
                    
                    # Score based on being roughly square and well-filled
                    if (100 <= w <= img_cv.shape[1] * 0.7 and
                        100 <= h <= img_cv.shape[0] * 0.7 and
                        0.7 <= aspect_ratio <= 1.3 and  # Roughly square
                        fill_ratio > 0.2):  # Somewhat filled
                        
                        score = fill_ratio * (rect_area / (img_cv.shape[0] * img_cv.shape[1]))
                        
                        if score > best_score:
                            best_score = score
                            best_rect = (x, y, w, h)
                            print(f"   New best edge pattern: {w}x{h} (score: {score:.3f})")
        
        if best_rect:
            x, y, w, h = best_rect
            print(f"   📐 Found edge pattern rectangle: {w}x{h}")
            cropped = image.crop((x, y, x + w, y + h))
            if cropped.width >= 100 and cropped.height >= 100:
                return cropped
        
        return None
    
    except Exception as e:
        print(f"   ⚠️  Edge pattern detection error: {e}")
        return None

def enhanced_center_crop(image):
    """Enhanced center crop as fallback"""
    
    try:
        width, height = image.size
        
        # Try different crop ratios, prioritizing square
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
                    print(f"   📐 Using enhanced center crop: {cropped.size[0]}x{cropped.size[1]}")
                    return cropped
        
        # Fallback to original
        print(f"   ⚠️  Using original image as fallback")
        return image
    
    except Exception as e:
        print(f"   ⚠️  Enhanced center crop error: {e}")
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
    success, count = advanced_marker_detection_extract_first_page()
    if success:
        print(f"\n🎉 Successfully extracted {count} player photo(s) using advanced marker detection!")
    else:
        print(f"\n❌ Failed to extract player photos")
