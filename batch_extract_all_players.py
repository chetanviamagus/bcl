#!/usr/bin/env python3
"""
BATCH EXTRACT ALL PLAYERS
Process all 145 pages from screenshots/ folder and extract player photos to players/ folder.
Uses the safe margin white removal algorithm for consistent results.
"""

import os
import sys
import glob
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
from scipy import ndimage
import time

class BatchPlayerExtractor:
    """
    Batch processor for extracting all player photos from PDF pages.
    """
    
    def __init__(self, white_threshold=225, blue_threshold=50, safety_margin=2):
        self.white_threshold = white_threshold
        self.blue_threshold = blue_threshold
        self.safety_margin = safety_margin
        self.processed_count = 0
        self.error_count = 0
        self.start_time = time.time()
        
    def is_white_pixel(self, rgb):
        """Very aggressive white detection."""
        r, g, b = rgb
        return (r >= self.white_threshold and 
                g >= self.white_threshold and 
                b >= self.white_threshold)
    
    def is_blue_text_pixel(self, rgb):
        """Check if pixel is blue text."""
        r, g, b = rgb
        return (b > (r + self.blue_threshold) and 
                b > (g + self.blue_threshold) and 
                b > 100)
    
    def is_white_clothing_pixel(self, rgb, position, img_array):
        """Enhanced white clothing detection."""
        r, g, b = rgb
        y, x = position
        height, width = img_array.shape[:2]
        
        # Check larger area around pixel (5x5)
        y_start = max(0, y-2)
        y_end = min(height, y+3)
        x_start = max(0, x-2)
        x_end = min(width, x+3)
        
        surrounding_area = img_array[y_start:y_end, x_start:x_end]
        
        # Count non-white pixels in surrounding area
        non_white_count = 0
        for py in range(surrounding_area.shape[0]):
            for px in range(surrounding_area.shape[1]):
                pr, pg, pb = surrounding_area[py, px]
                if not (pr >= 240 and pg >= 240 and pb >= 240):
                    non_white_count += 1
        
        # If surrounded by significant content, likely white clothing
        return non_white_count > 4
    
    def is_subject_pixel(self, rgb, position, img_array):
        """Enhanced subject pixel detection."""
        # Not white background
        if self.is_white_pixel(rgb):
            # Check if it's white clothing vs background
            return self.is_white_clothing_pixel(rgb, position, img_array)
        
        # Not blue text
        if self.is_blue_text_pixel(rgb):
            return False
            
        # Everything else is subject
        return True
    
    def detect_content_with_safety_margin(self, img_array):
        """Detect content and apply safety margin."""
        height, width = img_array.shape[:2]
        
        # Create content mask
        content_mask = np.zeros((height, width), dtype=bool)
        
        # Scan every pixel
        for y in range(height):
            for x in range(width):
                if self.is_subject_pixel(img_array[y, x], (y, x), img_array):
                    content_mask[y, x] = True
        
        # Apply morphological operations
        content_mask = ndimage.binary_fill_holes(content_mask)
        content_mask = ndimage.binary_erosion(content_mask, iterations=1)
        content_mask = ndimage.binary_dilation(content_mask, iterations=1)
        
        # Find largest connected component
        labeled_array, num_features = ndimage.label(content_mask)
        if num_features > 0:
            component_sizes = ndimage.sum(content_mask, labeled_array, range(1, num_features + 1))
            largest_component = np.argmax(component_sizes) + 1
            content_mask = (labeled_array == largest_component)
        
        return content_mask
    
    def find_content_bounds_with_safety_margin(self, mask):
        """Find content bounds and apply 2px safety margin from all sides."""
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            return None
        
        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]
        
        # Apply safety margin - remove 2px from all sides
        height, width = mask.shape
        
        # Add safety margin
        x_min = max(0, x_min + self.safety_margin)
        y_min = max(0, y_min + self.safety_margin)
        x_max = min(width, x_max - self.safety_margin)
        y_max = min(height, y_max - self.safety_margin)
        
        # Ensure we don't have negative dimensions
        if x_max <= x_min or y_max <= y_min:
            rows = np.any(mask, axis=1)
            cols = np.any(mask, axis=0)
            y_min, y_max = np.where(rows)[0][[0, -1]]
            x_min, x_max = np.where(cols)[0][[0, -1]]
        
        return (x_min, y_min), (x_max, y_max)
    
    def extract_player_from_page(self, page_path, output_path):
        """Extract player photo from a single page."""
        try:
            # Load image
            img = Image.open(page_path)
            
            # Convert to RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get image dimensions
            width, height = img.size
            
            # Crop the left half (where the player photo is)
            crop_width = width // 2
            left_crop = img.crop((0, 0, crop_width, height))
            
            # Convert to numpy array
            img_array = np.array(left_crop)
            
            # Detect content
            content_mask = self.detect_content_with_safety_margin(img_array)
            
            # Find content bounds with safety margin
            bounds = self.find_content_bounds_with_safety_margin(content_mask)
            if bounds is None:
                print(f"  ⚠️  No content found in {os.path.basename(page_path)}")
                return False
            
            (x_min, y_min), (x_max, y_max) = bounds
            
            # Crop to bounds with safety margin
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(crop_width, x_max)
            y_max = min(height, y_max)
            
            # Final crop
            final_img = left_crop.crop((x_min, y_min, x_max, y_max))
            
            # Save result
            final_img.save(output_path, 'PNG', quality=95)
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error processing {os.path.basename(page_path)}: {e}")
            return False
    
    def process_all_pages(self, screenshots_dir, players_dir):
        """Process all pages in the screenshots directory."""
        print("BATCH EXTRACT ALL PLAYERS")
        print("="*60)
        print(f"Screenshots directory: {screenshots_dir}")
        print(f"Players directory: {players_dir}")
        print("-" * 60)
        
        # Get all page files
        page_files = sorted(glob.glob(os.path.join(screenshots_dir, "page_*.png")))
        
        if not page_files:
            print("❌ No page files found in screenshots directory!")
            return
        
        total_pages = len(page_files)
        print(f"Found {total_pages} pages to process")
        print("-" * 60)
        
        # Process each page
        for i, page_path in enumerate(page_files, 1):
            page_name = os.path.basename(page_path)
            page_number = page_name.replace("page_", "").replace(".png", "")
            
            # Create output filename
            output_filename = f"player_{page_number.zfill(3)}.png"
            output_path = os.path.join(players_dir, output_filename)
            
            print(f"[{i:3d}/{total_pages}] Processing {page_name}...", end=" ")
            
            # Extract player photo
            success = self.extract_player_from_page(page_path, output_path)
            
            if success:
                self.processed_count += 1
                print("✅")
            else:
                self.error_count += 1
                print("❌")
            
            # Show progress every 10 pages
            if i % 10 == 0:
                elapsed = time.time() - self.start_time
                avg_time = elapsed / i
                remaining = (total_pages - i) * avg_time
                print(f"    Progress: {i}/{total_pages} ({i/total_pages*100:.1f}%) - ETA: {remaining/60:.1f}min")
        
        # Final summary
        elapsed = time.time() - self.start_time
        print("\n" + "="*60)
        print("BATCH PROCESSING COMPLETE")
        print("="*60)
        print(f"Total pages processed: {total_pages}")
        print(f"Successfully extracted: {self.processed_count}")
        print(f"Errors: {self.error_count}")
        print(f"Success rate: {self.processed_count/total_pages*100:.1f}%")
        print(f"Total time: {elapsed/60:.1f} minutes")
        print(f"Average time per page: {elapsed/total_pages:.1f} seconds")
        print("="*60)
        
        if self.error_count > 0:
            print(f"⚠️  {self.error_count} pages had errors. Check the output above for details.")
        else:
            print("🎉 All pages processed successfully!")

def main():
    """Main function for batch processing."""
    # Directory paths
    screenshots_dir = "screenshots"
    players_dir = "players"
    
    # Check if screenshots directory exists
    if not os.path.exists(screenshots_dir):
        print(f"❌ Screenshots directory not found: {screenshots_dir}")
        return
    
    # Create players directory if it doesn't exist
    os.makedirs(players_dir, exist_ok=True)
    
    # Create batch processor
    processor = BatchPlayerExtractor(
        white_threshold=225,
        blue_threshold=50,
        safety_margin=2
    )
    
    # Process all pages
    processor.process_all_pages(screenshots_dir, players_dir)

if __name__ == "__main__":
    main()
