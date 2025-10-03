#!/usr/bin/env python3
"""
Extract player photos from New-2025-BCL-Players.pptx.pdf
Save images with format: Name-Age-Category-Mobile
"""

import json
import os
import re
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io

def extract_player_photos():
    """Extract player photos from PDF and save with proper naming"""
    
    print("📸 Extracting Player Photos from PDF")
    print("=" * 50)
    
    # Paths
    pdf_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/New-2025-BCL-Players.pptx.pdf'
    data_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/complete_pdf_players_data.json'
    output_dir = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/players'
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    # Load player data
    if not os.path.exists(data_path):
        print(f"❌ Player data not found: {data_path}")
        return
    
    with open(data_path, 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print(f"📊 Loaded {len(players_data)} players")
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
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
            
            # Extract image from page
            success = extract_image_from_page(doc, page_num, player, output_dir)
            
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

def extract_image_from_page(doc, page_num, player, output_dir):
    """Extract and save image from a specific page"""
    
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
            
            # Skip if image is too small (likely not a player photo)
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
            
            # Crop the image to focus on player photo
            cropped_image = crop_player_photo(pil_image)
            
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

def crop_player_photo(image):
    """Crop image to focus on player photo area"""
    
    try:
        width, height = image.size
        
        # Common player photo areas (adjust based on PDF layout)
        # Most player photos are in the center or upper portion
        
        # Strategy 1: Center crop (most common)
        center_crop = crop_center_region(image, width, height)
        if center_crop:
            return center_crop
        
        # Strategy 2: Upper portion crop
        upper_crop = crop_upper_region(image, width, height)
        if upper_crop:
            return upper_crop
        
        # Strategy 3: Auto-detect faces or significant content
        auto_crop = crop_auto_detect(image)
        if auto_crop:
            return auto_crop
        
        # Fallback: Return original image if no good crop found
        return image
    
    except Exception as e:
        print(f"   ⚠️  Crop error: {e}")
        return image

def crop_center_region(image, width, height):
    """Crop center region of the image"""
    
    # Define crop area (adjust these ratios based on your PDF layout)
    crop_ratio = 0.6  # Crop to 60% of original size
    crop_width = int(width * crop_ratio)
    crop_height = int(height * crop_ratio)
    
    # Center the crop
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height
    
    # Ensure crop area is valid
    if left >= 0 and top >= 0 and right <= width and bottom <= height:
        cropped = image.crop((left, top, right, bottom))
        
        # Check if cropped image has reasonable dimensions
        if cropped.width >= 100 and cropped.height >= 100:
            return cropped
    
    return None

def crop_upper_region(image, width, height):
    """Crop upper portion of the image (common for player photos)"""
    
    # Crop upper 70% of the image
    crop_height = int(height * 0.7)
    left = 0
    top = 0
    right = width
    bottom = crop_height
    
    cropped = image.crop((left, top, right, bottom))
    
    if cropped.width >= 100 and cropped.height >= 100:
        return cropped
    
    return None

def crop_auto_detect(image):
    """Auto-detect and crop based on content analysis"""
    
    # Convert to grayscale for analysis
    gray = image.convert('L')
    width, height = gray.size
    
    # Find areas with significant content (not just background)
    # This is a simple approach - you might want to use more sophisticated methods
    
    # Sample the image to find content-rich regions
    step = 20
    content_areas = []
    
    for y in range(0, height - step, step):
        for x in range(0, width - step, step):
            # Get pixel values in this region
            region = gray.crop((x, y, x + step, y + step))
            pixels = list(region.getdata())
            
            # Calculate variance (measure of content richness)
            if pixels:
                mean = sum(pixels) / len(pixels)
                variance = sum((p - mean) ** 2 for p in pixels) / len(pixels)
                
                if variance > 500:  # Threshold for "interesting" content
                    content_areas.append((x, y, variance))
    
    if content_areas:
        # Find the region with highest content
        content_areas.sort(key=lambda x: x[2], reverse=True)
        best_x, best_y, _ = content_areas[0]
        
        # Crop around the best region
        crop_size = min(300, width - best_x, height - best_y)
        left = max(0, best_x - 50)
        top = max(0, best_y - 50)
        right = min(width, left + crop_size)
        bottom = min(height, top + crop_size)
        
        cropped = image.crop((left, top, right, bottom))
        
        if cropped.width >= 100 and cropped.height >= 100:
            return cropped
    
    return None

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

def analyze_pdf_layout():
    """Analyze PDF layout to understand image positioning"""
    
    pdf_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/New-2025-BCL-Players.pptx.pdf'
    
    try:
        doc = fitz.open(pdf_path)
        print("\\n📊 Analyzing PDF Layout...")
        
        # Analyze first few pages
        for page_num in range(min(5, doc.page_count)):
            page = doc[page_num]
            images = page.get_images(full=True)
            
            print(f"\\nPage {page_num + 1}:")
            print(f"  Size: {page.rect.width} x {page.rect.height}")
            print(f"  Images: {len(images)}")
            
            for i, img in enumerate(images):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                print(f"    Image {i+1}: {pix.width} x {pix.height}")
                pix = None
        
        doc.close()
        
    except Exception as e:
        print(f"❌ Layout analysis error: {e}")

if __name__ == "__main__":
    # First analyze the PDF layout
    analyze_pdf_layout()
    
    # Then extract photos
    extract_player_photos()
