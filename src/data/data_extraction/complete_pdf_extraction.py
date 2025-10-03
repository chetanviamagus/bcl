#!/usr/bin/env python3
"""
Complete PDF extraction - check all 145 pages
"""

import json
import re
import os

def complete_pdf_extraction():
    """Extract data from all 145 pages of the PDF"""
    
    print("📄 Complete PDF Data Extraction - All 145 Pages")
    print("=" * 60)
    
    # PDF file path
    pdf_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/New-2025-BCL-Players.pptx.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"📁 PDF file: {os.path.basename(pdf_path)}")
    
    try:
        import fitz
        print("🔍 Using PyMuPDF for complete extraction...")
        
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        print(f"📄 Total pages: {total_pages}")
        
        all_players = []
        pages_with_players = []
        pages_without_players = []
        
        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text()
            
            # Extract players from this page
            players = extract_players_from_page(text, page_num + 1)
            
            if players:
                all_players.extend(players)
                pages_with_players.append(page_num + 1)
                print(f"✅ Page {page_num + 1}: Found {len(players)} player(s)")
            else:
                pages_without_players.append(page_num + 1)
                print(f"❌ Page {page_num + 1}: No players found")
                
                # Show content of pages without players for debugging
                if page_num < 10:  # Show first 10 empty pages
                    print(f"   Content preview: {text[:200]}...")
        
        doc.close()
        
        print(f"\n📊 Complete Extraction Results:")
        print(f"  Total pages processed: {total_pages}")
        print(f"  Pages with players: {len(pages_with_players)}")
        print(f"  Pages without players: {len(pages_without_players)}")
        print(f"  Total players found: {len(all_players)}")
        
        if pages_without_players:
            print(f"\n📄 Pages without players: {pages_without_players}")
        
        # Process and clean data
        processed_players = process_extracted_players(all_players)
        
        print(f"\n📊 Processed Results:")
        print(f"  Valid players: {len(processed_players)}")
        
        if processed_players:
            # Show first few players
            print(f"\n🏏 First 10 players:")
            for i, player in enumerate(processed_players[:10]):
                print(f"  {i+1:2d}. {player['name']} - {player['category']} - Age: {player['age']} - ICON: {player['iconPlayer']}")
            
            # Show last few players
            print(f"\n🏏 Last 10 players:")
            for i, player in enumerate(processed_players[-10:], len(processed_players)-9):
                print(f"  {i:2d}. {player['name']} - {player['category']} - Age: {player['age']} - ICON: {player['iconPlayer']}")
            
            # Save data
            save_complete_data(processed_players, pages_with_players, pages_without_players)
            
            return processed_players
        else:
            print("❌ No valid player data found")
            return []
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def extract_players_from_page(text, page_num):
    """Extract player data from a single page with improved patterns"""
    
    players = []
    
    # Split text into lines for better processing
    lines = text.split('\n')
    
    # Look for various player data patterns
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Pattern 1: "Name:" at start of line
        if line.startswith('Name:'):
            player = extract_player_from_name_line(lines, i, page_num)
            if player:
                players.append(player)
        
        # Pattern 2: Look for name patterns without "Name:" prefix
        elif re.match(r'^[A-Za-z][A-Za-z\s\.]+$', line) and len(line) > 2:
            # Check if next lines contain category, age, phone
            if is_likely_player_name(lines, i):
                player = extract_player_from_name_line(lines, i, page_num, has_name_prefix=False)
                if player:
                    players.append(player)
        
        i += 1
    
    return players

def is_likely_player_name(lines, start_idx):
    """Check if a line is likely a player name by looking at following lines"""
    
    # Look at next 5 lines for category, age, phone patterns
    for i in range(start_idx + 1, min(start_idx + 6, len(lines))):
        line = lines[i].strip()
        if (line.startswith('Category:') or 
            line.startswith('Age:') or 
            line.startswith('Ph:') or
            'Batsman' in line or
            'Bowler' in line or
            'All Rounder' in line or
            'Wicket Keeper' in line):
            return True
    return False

def extract_player_from_name_line(lines, start_idx, page_num, has_name_prefix=True):
    """Extract player data starting from a name line"""
    
    player = {}
    
    # Extract name
    name_line = lines[start_idx].strip()
    if has_name_prefix:
        name = name_line.replace('Name:', '').strip()
    else:
        name = name_line
    
    if not name or len(name) < 2:
        return None
    
    player['name'] = name
    player['page'] = page_num
    
    # Look for category, age, phone in following lines
    j = start_idx + 1
    while j < len(lines) and j < start_idx + 10:  # Look within next 10 lines
        line = lines[j].strip()
        
        if line.startswith('Category:'):
            category = line.replace('Category:', '').strip()
            player['category'] = category
        elif line.startswith('Age:'):
            age_match = re.search(r'Age:\s*(\d+)', line)
            if age_match:
                player['age'] = age_match.group(1)
        elif line.startswith('Ph:'):
            phone_match = re.search(r'Ph:\s*(\d+)', line)
            if phone_match:
                player['mobile'] = phone_match.group(1)
        elif 'ICON' in line.upper():
            player['iconPlayer'] = 'Yes'
        
        j += 1
    
    # Only return if we have essential data
    if 'name' in player and 'category' in player and 'age' in player:
        if 'mobile' not in player:
            player['mobile'] = ''
        if 'iconPlayer' not in player:
            player['iconPlayer'] = 'No'
        
        return player
    
    return None

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

def save_complete_data(players, pages_with_players, pages_without_players):
    """Save complete data with page analysis"""
    
    if not players:
        print("❌ No data to save")
        return
    
    # Save as JSON
    json_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/complete_pdf_players_data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(players, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved JSON: {json_path}")
    
    # Save as CSV
    csv_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/complete_pdf_players_data.csv'
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("slide_number,name,category,age,mobile,iconPlayer,source\n")
        for player in players:
            f.write(f"{player['slide_number']},{player['name']},{player['category']},{player['age']},{player['mobile']},{player['iconPlayer']},{player['source']}\n")
    print(f"✅ Saved CSV: {csv_path}")
    
    # Save as TypeScript
    ts_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/complete_pdf_players_data.ts'
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write('export interface CompletePDFPlayerData {\n')
        f.write('  slide_number: number;\n')
        f.write('  name: string;\n')
        f.write('  category: string;\n')
        f.write('  age: string;\n')
        f.write('  mobile: string;\n')
        f.write('  iconPlayer: string;\n')
        f.write('  source: string;\n')
        f.write('}\n\n')
        f.write('export const completePdfPlayersData: CompletePDFPlayerData[] = [\n')
        
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
    
    # Generate detailed summary
    summary_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/complete_pdf_players_summary.txt'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("Complete PDF Player Data Extraction Summary\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total pages in PDF: 145\n")
        f.write(f"Pages with players: {len(pages_with_players)}\n")
        f.write(f"Pages without players: {len(pages_without_players)}\n")
        f.write(f"Total players extracted: {len(players)}\n")
        f.write(f"Source file: New-2025-BCL-Players.pptx.pdf\n")
        f.write(f"Extraction date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if pages_without_players:
            f.write(f"Pages without players: {pages_without_players}\n\n")
        
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
        
        f.write(f"\nAll players by page:\n")
        for player in players:
            f.write(f"  Page {player['slide_number']:3d}: {player['name']} - {player['category']} - Age: {player['age']} - ICON: {player['iconPlayer']}\n")
    
    print(f"✅ Saved detailed summary: {summary_path}")

if __name__ == "__main__":
    complete_pdf_extraction()
