#!/usr/bin/env python3
"""
Simple Player Photo Extraction
Extract the main player photo from each PDF page
"""

import json
import os
import re
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image, ImageOps
import io

def simple_extract_player_photos():
    """Extract player photos from each PDF page"""
    
    print("📸 Simple Player Photo Extraction")
    print("=" * 40)
    
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
            
            # Extract the main image from page
            success = extract_main_image_from_page(doc, page_num, player, output_dir)
            
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

def extract_main_image_from_page(doc, page_num, player, output_dir):
    """Extract the main/largest image from a PDF page"""
    
    try:
        page = doc[page_num]
        
        # Get all images on the page
        image_list = page.get_images(full=True)
        
        if not image_list:
            print(f"   No images found on page {page_num + 1}")
            return False
        
        print(f"   Found {len(image_list)} image(s) on page {page_num + 1}")
        
        # Find the largest image (likely the main player photo)
        largest_image = None
        largest_area = 0
        
        for img_index, img in enumerate(image_list):
            # Get image data
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            
            # Calculate area
            area = pix.width * pix.height
            
            print(f"   Image {img_index + 1}: {pix.width}x{pix.height} (area: {area})")
            
            # Skip very small images (likely icons or decorative elements)
            if area < 10000:  # Less than 100x100 pixels
                pix = None
                continue
            
            # Keep track of the largest image
            if area > largest_area:
                if largest_image:
                    largest_image.close()  # Close previous image
                
                # Convert to PIL Image
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    img_data = pix.tobytes("png")
                    largest_image = Image.open(io.BytesIO(img_data))
                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    img_data = pix1.tobytes("png")
                    largest_image = Image.open(io.BytesIO(img_data))
                    pix1 = None
                
                largest_area = area
            
            pix = None
        
        if largest_image:
            # Apply smart cropping to focus on the player
            cropped_image = smart_crop_for_player(largest_image)
            
            # Generate filename
            filename = generate_filename(player)
            filepath = os.path.join(output_dir, filename)
            
            # Save image
            cropped_image.save(filepath, 'PNG', quality=95)
            
            print(f"   💾 Saved: {filename} ({cropped_image.size[0]}x{cropped_image.size[1]})")
            return True
        
        print(f"   No suitable image found on page {page_num + 1}")
        return False
    
    except Exception as e:
        print(f"   ❌ Error processing page {page_num + 1}: {e}")
        return False

def smart_crop_for_player(image):
    """Apply smart cropping to focus on the player photo"""
    
    width, height = image.size
    
    # Strategy: Focus on the upper portion where player photos typically are
    # and create a reasonable aspect ratio
    
    # If the image is very wide, crop it to focus on the player
    if width > height * 1.5:  # Very wide image
        # Focus on left or center portion
        crop_width = int(height * 0.8)  # Make it roughly square
        left = (width - crop_width) // 2  # Center crop
        top = int(height * 0.1)  # Start from 10% down from top
        right = left + crop_width
        bottom = min(height, top + crop_width)
    else:
        # For normal or tall images, focus on upper portion
        crop_height = int(height * 0.8)  # Use 80% of height
        crop_width = min(width, int(crop_height * 0.8))  # Make it roughly square
        
        left = (width - crop_width) // 2  # Center horizontally
        top = int(height * 0.1)  # Start from 10% down from top
        right = left + crop_width
        bottom = top + crop_height
    
    # Ensure crop coordinates are valid
    left = max(0, left)
    top = max(0, top)
    right = min(width, right)
    bottom = min(height, bottom)
    
    # Ensure minimum size
    if right - left < 100 or bottom - top < 100:
        # If crop is too small, use a larger portion
        crop_size = min(width, height, 400)  # Maximum 400px
        left = (width - crop_size) // 2
        top = (height - crop_size) // 2
        right = left + crop_size
        bottom = top + crop_size
        
        # Ensure coordinates are valid
        left = max(0, left)
        top = max(0, top)
        right = min(width, right)
        bottom = min(height, bottom)
    
    cropped = image.crop((left, top, right, bottom))
    
    # If the result is still very large, resize it
    if cropped.width > 500 or cropped.height > 500:
        # Resize while maintaining aspect ratio
        if cropped.width > cropped.height:
            new_width = 400
            new_height = int((cropped.height * new_width) / cropped.width)
        else:
            new_height = 400
            new_width = int((cropped.width * new_height) / cropped.height)
        
        cropped = cropped.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return cropped

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
    simple_extract_player_photos()
