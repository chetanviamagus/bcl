#!/usr/bin/env python3
"""
Improved PDF extraction for New-2025-BCL-Players.pptx.pdf
"""

import json
import re
import os
from pathlib import Path

def improved_pdf_extraction():
    """Improved extraction with better pattern matching"""
    
    print("📄 Improved PDF Data Extraction")
    print("=" * 50)
    
    # PDF file path
    pdf_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/New-2025-BCL-Players.pptx.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"📁 PDF file: {os.path.basename(pdf_path)}")
    
    # Use PyMuPDF for better text extraction
    try:
        import fitz
        print("🔍 Using PyMuPDF for extraction...")
        
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        print(f"📄 Total pages: {total_pages}")
        
        all_players = []
        
        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text()
            
            # Extract players from this page
            players = extract_players_from_page(text, page_num + 1)
            all_players.extend(players)
            
            if page_num < 5:  # Show first 5 pages
                print(f"\n📄 Page {page_num + 1}:")
                print("-" * 30)
                print(text[:300] + "..." if len(text) > 300 else text)
        
        doc.close()
        
        # Process and clean data
        processed_players = process_extracted_players(all_players)
        
        print(f"\n📊 Extraction Results:")
        print(f"  Raw extractions: {len(all_players)}")
        print(f"  Processed players: {len(processed_players)}")
        
        if processed_players:
            # Show first few players
            print(f"\n🏏 First 10 players:")
            for i, player in enumerate(processed_players[:10]):
                print(f"  {i+1:2d}. {player['name']} - {player['category']} - Age: {player['age']} - ICON: {player['iconPlayer']}")
            
            # Save data
            save_processed_data(processed_players)
            
            return processed_players
        else:
            print("❌ No valid player data found")
            return []
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def extract_players_from_page(text, page_num):
    """Extract player data from a single page"""
    
    players = []
    
    # Split text into lines for better processing
    lines = text.split('\n')
    
    # Look for player data patterns
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for "Name:" pattern
        if line.startswith('Name:'):
            player = {}
            
            # Extract name
            name = line.replace('Name:', '').strip()
            if name:
                player['name'] = name
                player['page'] = page_num
                
                # Look for next lines with category, age, phone
                j = i + 1
                while j < len(lines) and j < i + 10:  # Look within next 10 lines
                    next_line = lines[j].strip()
                    
                    if next_line.startswith('Category:'):
                        category = next_line.replace('Category:', '').strip()
                        player['category'] = category
                    elif next_line.startswith('Age:'):
                        age_match = re.search(r'Age:\s*(\d+)', next_line)
                        if age_match:
                            player['age'] = age_match.group(1)
                    elif next_line.startswith('Ph:'):
                        phone_match = re.search(r'Ph:\s*(\d+)', next_line)
                        if phone_match:
                            player['mobile'] = phone_match.group(1)
                    elif 'ICON' in next_line.upper():
                        player['iconPlayer'] = 'Yes'
                    
                    j += 1
                
                # Only add if we have essential data
                if 'name' in player and 'category' in player and 'age' in player:
                    if 'mobile' not in player:
                        player['mobile'] = ''
                    if 'iconPlayer' not in player:
                        player['iconPlayer'] = 'No'
                    
                    players.append(player)
        
        i += 1
    
    return players

def process_extracted_players(raw_players):
    """Process and clean extracted player data"""
    
    processed = []
    seen_names = set()
    
    for player in raw_players:
        name = player.get('name', '').strip()
        
        # Skip if name is too short or already seen
        if len(name) < 2 or name in seen_names:
            continue
        
        # Clean up the data
        cleaned_player = {
            'slide_number': player.get('page', 1),
            'name': re.sub(r'\s+', ' ', name).strip(),
            'category': re.sub(r'\s+', ' ', player.get('category', '')).strip(),
            'age': str(player.get('age', '')).strip(),
            'mobile': str(player.get('mobile', '')).strip(),
            'iconPlayer': player.get('iconPlayer', 'No'),
            'source': 'PDF'
        }
        
        # Validate data
        if (cleaned_player['name'] and 
            cleaned_player['category'] and 
            cleaned_player['age'].isdigit() and
            len(cleaned_player['age']) <= 3):  # Reasonable age range
            
            processed.append(cleaned_player)
            seen_names.add(name)
    
    return processed

def save_processed_data(players):
    """Save processed data to files"""
    
    if not players:
        print("❌ No data to save")
        return
    
    # Save as JSON
    json_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/pdf_players_data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(players, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved JSON: {json_path}")
    
    # Save as CSV
    csv_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/pdf_players_data.csv'
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("slide_number,name,category,age,mobile,iconPlayer,source\n")
        for player in players:
            f.write(f"{player['slide_number']},{player['name']},{player['category']},{player['age']},{player['mobile']},{player['iconPlayer']},{player['source']}\n")
    print(f"✅ Saved CSV: {csv_path}")
    
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
    print(f"✅ Saved TypeScript: {ts_path}")
    
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
        icon_count = 0
        for player in players:
            cat = player.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
            if player.get('iconPlayer') == 'Yes':
                icon_count += 1
        
        f.write("Category breakdown:\n")
        for cat, count in sorted(categories.items()):
            f.write(f"  {cat}: {count} players\n")
        
        f.write(f"\nICON players: {icon_count}\n")
        f.write(f"Regular players: {len(players) - icon_count}\n")
        
        if players:
            ages = [int(p['age']) for p in players if p['age'].isdigit()]
            if ages:
                f.write(f"\nAge range: {min(ages)} - {max(ages)}\n")
                f.write(f"Average age: {sum(ages) / len(ages):.1f}\n")
        
        f.write(f"\nFirst 20 players:\n")
        for i, player in enumerate(players[:20]):
            f.write(f"  {i+1:2d}. {player['name']} - {player['category']} - Age: {player['age']} - ICON: {player['iconPlayer']}\n")
    
    print(f"✅ Saved summary: {summary_path}")

if __name__ == "__main__":
    improved_pdf_extraction()
