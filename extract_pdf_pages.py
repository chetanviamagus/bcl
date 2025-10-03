#!/usr/bin/env python3
"""
Extract each page from the 2025-BCL-Players.pdf as images and save them to screenshots/ directory.
"""

import fitz  # PyMuPDF
import os
from pathlib import Path

def extract_pdf_pages_as_images(pdf_path, output_dir, image_format='PNG', dpi=300):
    """
    Extract each page from a PDF as images and save them to the output directory.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save the images
        image_format (str): Image format (PNG, JPEG, etc.)
        dpi (int): Resolution for the images
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Open the PDF
    try:
        doc = fitz.open(pdf_path)
        print(f"PDF opened successfully. Total pages: {len(doc)}")
        
        # Extract each page as image
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Create a matrix for scaling (higher DPI = better quality)
            mat = fitz.Matrix(dpi/72, dpi/72)  # 72 is the default DPI
            
            # Render page to pixmap
            pix = page.get_pixmap(matrix=mat)
            
            # Generate filename
            filename = f"page_{page_num + 1:03d}.{image_format.lower()}"
            filepath = os.path.join(output_dir, filename)
            
            # Save the image
            pix.save(filepath)
            
            print(f"Extracted page {page_num + 1}/{len(doc)}: {filename}")
        
        doc.close()
        print(f"\nExtraction completed! {len(doc)} pages saved to {output_dir}")
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return False
    
    return True

def main():
    # File paths
    pdf_path = "src/data/2025-BCL-Players.pdf"
    output_dir = "screenshots"
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return
    
    print(f"Extracting pages from: {pdf_path}")
    print(f"Saving images to: {output_dir}")
    print(f"Image format: PNG")
    print(f"DPI: 300")
    print("-" * 50)
    
    # Extract pages
    success = extract_pdf_pages_as_images(pdf_path, output_dir, image_format='PNG', dpi=300)
    
    if success:
        print("\n✅ PDF page extraction completed successfully!")
    else:
        print("\n❌ PDF page extraction failed!")

if __name__ == "__main__":
    main()
