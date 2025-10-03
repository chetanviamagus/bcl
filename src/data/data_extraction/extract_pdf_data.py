#!/usr/bin/env python3
"""
Extract player data from New-2025-BCL-Players.pptx.pdf
"""

import json
import re
import os
from pathlib import Path

def extract_pdf_data():
    """Extract player data from the PDF file"""
    
    print("📄 PDF Data Extraction - New-2025-BCL-Players.pptx.pdf")
    print("=" * 70)
    
    # PDF file path
    pdf_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/New-2025-BCL-Players.pptx.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"📁 PDF file found: {os.path.basename(pdf_path)}")
    print(f"📊 File size: {os.path.getsize(pdf_path) / (1024*1024):.1f} MB")
    
    # Try different PDF extraction methods
    extracted_data = []
    
    # Method 1: PyPDF2
    try:
        import PyPDF2
        print("\n🔍 Method 1: PyPDF2")
        print("-" * 30)
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            print(f"📄 Total pages: {total_pages}")
            
            for page_num in range(min(5, total_pages)):  # First 5 pages
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                print(f"📄 Page {page_num + 1} preview:")
                print(text[:200] + "..." if len(text) > 200 else text)
                print()
                
                # Look for player data patterns
                players = extract_players_from_text(text, page_num + 1)
                extracted_data.extend(players)
    
    except Exception as e:
        print(f"❌ PyPDF2 error: {e}")
    
    # Method 2: pdfplumber
    try:
        import pdfplumber
        print("\n🔍 Method 2: pdfplumber")
        print("-" * 30)
        
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"📄 Total pages: {total_pages}")
            
            for page_num in range(min(5, total_pages)):  # First 5 pages
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    print(f"📄 Page {page_num + 1} preview:")
                    print(text[:200] + "..." if len(text) > 200 else text)
                    print()
                    
                    # Look for player data patterns
                    players = extract_players_from_text(text, page_num + 1)
                    extracted_data.extend(players)
    
    except Exception as e:
        print(f"❌ pdfplumber error: {e}")
    
    # Method 3: PyMuPDF
    try:
        import fitz
        print("\n🔍 Method 3: PyMuPDF")
        print("-" * 30)
        
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        print(f"📄 Total pages: {total_pages}")
        
        for page_num in range(min(5, total_pages)):  # First 5 pages
            page = doc[page_num]
            text = page.get_text()
            print(f"📄 Page {page_num + 1} preview:")
            print(text[:200] + "..." if len(text) > 200 else text)
            print()
            
            # Look for player data patterns
            players = extract_players_from_text(text, page_num + 1)
            extracted_data.extend(players)
        
        doc.close()
    
    except Exception as e:
        print(f"❌ PyMuPDF error: {e}")
    
    # Process and clean extracted data
    print(f"\n📊 Extraction Results:")
    print(f"  Total players found: {len(extracted_data)}")
    
    if extracted_data:
        # Remove duplicates
        unique_players = []
        seen_names = set()
        
        for player in extracted_data:
            name = player.get('name', '').strip()
            if name and name not in seen_names:
                unique_players.append(player)
                seen_names.add(name)
        
        print(f"  Unique players: {len(unique_players)}")
        
        # Show first few players
        print(f"\n🏏 First 10 players found:")
        for i, player in enumerate(unique_players[:10]):
            print(f"  {i+1:2d}. {player.get('name', 'Unknown')} - {player.get('category', 'Unknown')} - Age: {player.get('age', 'Unknown')}")
        
        # Save extracted data
        save_extracted_data(unique_players)
        
        return unique_players
    else:
        print("❌ No player data found in PDF")
        return []

def extract_players_from_text(text, page_num):
    """Extract player information from text using regex patterns"""
    
    players = []
    
    # Common patterns for player data
    patterns = [
        # Pattern 1: Name: PlayerName Category: Category Age: XX years Ph: XXXXXXXXXX
        r'Name:\s*([^:]+?)\s*Category:\s*([^:]+?)\s*Age:\s*(\d+)\s*years?\s*Ph:\s*(\d+)',
        
        # Pattern 2: PlayerName Category: Category Age: XX years Ph: XXXXXXXXXX
        r'^([^:]+?)\s*Category:\s*([^:]+?)\s*Age:\s*(\d+)\s*years?\s*Ph:\s*(\d+)',
        
        # Pattern 3: Name: PlayerName\nCategory: Category\nAge: XX years\nPh: XXXXXXXXXX
        r'Name:\s*([^\n]+?)\nCategory:\s*([^\n]+?)\nAge:\s*(\d+)\s*years?\nPh:\s*(\d+)',
        
        # Pattern 4: PlayerName\nCategory: Category\nAge: XX years\nPh: XXXXXXXXXX
        r'^([^\n]+?)\nCategory:\s*([^\n]+?)\nAge:\s*(\d+)\s*years?\nPh:\s*(\d+)',
        
        # Pattern 5: More flexible pattern
        r'([A-Za-z\s\.]+?)\s*Category:\s*([A-Za-z\s]+?)\s*Age:\s*(\d+)\s*years?\s*Ph:\s*(\d+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.MULTILINE | re.IGNORECASE)
        
        for match in matches:
            if len(match) >= 4:
                name = match[0].strip()
                category = match[1].strip()
                age = match[2].strip()
                phone = match[3].strip()
                
                # Clean up the data
                name = re.sub(r'\s+', ' ', name).strip()
                category = re.sub(r'\s+', ' ', category).strip()
                
                # Skip if data looks invalid
                if (len(name) < 2 or len(category) < 2 or 
                    not age.isdigit() or len(phone) < 10):
                    continue
                
                player = {
                    'slide_number': page_num,
                    'name': name,
                    'category': category,
                    'age': age,
                    'mobile': phone,
                    'iconPlayer': 'No',  # Default, can be updated later
                    'source': 'PDF'
                }
                
                players.append(player)
    
    return players

def save_extracted_data(players):
    """Save extracted data to files"""
    
    if not players:
        print("❌ No data to save")
        return
    
    # Save as JSON
    json_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/pdf_players_data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(players, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved JSON data: {json_path}")
    
    # Save as CSV
    csv_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/pdf_players_data.csv'
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("slide_number,name,category,age,mobile,iconPlayer,source\n")
        for player in players:
            f.write(f"{player['slide_number']},{player['name']},{player['category']},{player['age']},{player['mobile']},{player['iconPlayer']},{player['source']}\n")
    print(f"✅ Saved CSV data: {csv_path}")
    
    # Save as TypeScript
    ts_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/pdf_players_data.ts'
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write('export interface PDFPlayerData {\n')
        f.write('  slide_number: number;\n')
        f.write('  name: string;\n')
        f.write('  category: string;\n')
        f.write('  age: string;\n')
        f.write('  mobile: string;\n')
        f.write('  iconPlayer: string;\n')
        f.write('  source: string;\n')
        f.write('}\n\n')
        f.write('export const pdfPlayersData: PDFPlayerData[] = [\n')
        
        for i, player in enumerate(players):
            f.write('  {\n')
            f.write(f'    "slide_number": {player["slide_number"]},\n')
            f.write(f'    "name": "{player["name"]}",\n')
            f.write(f'    "category": "{player["category"]}",\n')
            f.write(f'    "age": "{player["age"]}",\n')
            f.write(f'    "mobile": "{player["mobile"]}",\n')
            f.write(f'    "iconPlayer": "{player["iconPlayer"]}",\n')
            f.write(f'    "source": "{player["source"]}"\n')
            f.write('  }')
            if i < len(players) - 1:
                f.write(',')
            f.write('\n')
        
        f.write('];\n')
    print(f"✅ Saved TypeScript data: {ts_path}")
    
    # Generate summary
    summary_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/pdf_players_summary.txt'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("PDF Player Data Extraction Summary\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total players extracted: {len(players)}\n")
        f.write(f"Source file: New-2025-BCL-Players.pptx.pdf\n")
        f.write(f"Extraction date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Category breakdown
        categories = {}
        for player in players:
            cat = player.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        f.write("Category breakdown:\n")
        for cat, count in sorted(categories.items()):
            f.write(f"  {cat}: {count} players\n")
        
        f.write(f"\nAge range: {min(int(p['age']) for p in players)} - {max(int(p['age']) for p in players)}\n")
        
        f.write(f"\nFirst 10 players:\n")
        for i, player in enumerate(players[:10]):
            f.write(f"  {i+1:2d}. {player['name']} - {player['category']} - Age: {player['age']}\n")
    
    print(f"✅ Saved summary: {summary_path}")

if __name__ == "__main__":
    extract_pdf_data()
