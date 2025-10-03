#!/usr/bin/env python3
"""
PDF Reader Demo - Shows capabilities for reading PDF files
"""

import os
import sys

def check_pdf_libraries():
    """Check what PDF libraries are available"""
    
    print("📚 PDF Reading Capabilities")
    print("=" * 50)
    
    # Check for PyPDF2
    try:
        import PyPDF2
        print("✅ PyPDF2 - Available (basic text extraction)")
    except ImportError:
        print("❌ PyPDF2 - Not installed")
    
    # Check for pdfplumber
    try:
        import pdfplumber
        print("✅ pdfplumber - Available (advanced text extraction, tables)")
    except ImportError:
        print("❌ pdfplumber - Not installed")
    
    # Check for pymupdf (fitz)
    try:
        import fitz
        print("✅ PyMuPDF (fitz) - Available (fast, images, text)")
    except ImportError:
        print("❌ PyMuPDF (fitz) - Not installed")
    
    # Check for pdfminer
    try:
        from pdfminer.high_level import extract_text
        print("✅ pdfminer - Available (detailed text extraction)")
    except ImportError:
        print("❌ pdfminer - Not installed")
    
    print("\n🔧 What I can do with PDFs:")
    print("  • Extract text content")
    print("  • Extract tables and structured data")
    print("  • Extract images")
    print("  • Get page-by-page content")
    print("  • Search for specific text patterns")
    print("  • Convert PDF to other formats")
    print("  • Analyze document structure")

def install_pdf_libraries():
    """Install PDF reading libraries"""
    
    print("\n📦 Installing PDF Libraries...")
    print("=" * 50)
    
    libraries = [
        "PyPDF2",
        "pdfplumber", 
        "PyMuPDF",
        "pdfminer.six"
    ]
    
    for lib in libraries:
        try:
            print(f"Installing {lib}...")
            os.system(f"pip install {lib}")
            print(f"✅ {lib} installed successfully")
        except Exception as e:
            print(f"❌ Failed to install {lib}: {e}")

def read_pdf_example(pdf_path):
    """Example of reading a PDF file"""
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"\n📖 Reading PDF: {pdf_path}")
    print("=" * 50)
    
    # Try different methods
    methods = []
    
    # Method 1: PyPDF2
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            methods.append(("PyPDF2", text[:500] + "..." if len(text) > 500 else text))
    except Exception as e:
        methods.append(("PyPDF2", f"Error: {e}"))
    
    # Method 2: pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            methods.append(("pdfplumber", text[:500] + "..." if len(text) > 500 else text))
    except Exception as e:
        methods.append(("pdfplumber", f"Error: {e}"))
    
    # Method 3: PyMuPDF
    try:
        import fitz
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text() + "\n"
        doc.close()
        methods.append(("PyMuPDF", text[:500] + "..." if len(text) > 500 else text))
    except Exception as e:
        methods.append(("PyMuPDF", f"Error: {e}"))
    
    # Show results
    for method_name, result in methods:
        print(f"\n📋 {method_name} Results:")
        print("-" * 30)
        print(result)

if __name__ == "__main__":
    check_pdf_libraries()
    
    # Check if user wants to install libraries
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        install_pdf_libraries()
    
    # Check if user provided a PDF file
    if len(sys.argv) > 2:
        pdf_file = sys.argv[2]
        read_pdf_example(pdf_file)
    else:
        print("\n💡 Usage examples:")
        print("  python pdf_reader_demo.py --install")
        print("  python pdf_reader_demo.py /path/to/your/file.pdf")
