#!/usr/bin/env python3
"""
Extract data for missing slides from PDF
Missing slides: 22, 32, 46, 84, 100
"""

import json
import re
import os

def extract_missing_slides():
    """Extract data for the missing slide numbers"""
    
    print("📄 Extracting Missing Slides Data")
    print("=" * 50)
    
    missing_slides = [22, 32, 46, 84, 100]
    pdf_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/New-2025-BCL-Players.pptx.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    try:
        import fitz
        print(f"🔍 Extracting data for missing slides: {missing_slides}")
        
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        print(f"📄 Total pages in PDF: {total_pages}")
        
        extracted_players = []
        
        for slide_num in missing_slides:
            page_num = slide_num - 1  # Convert slide number to page index (0-based)
            
            if page_num < total_pages:
                print(f"\n🔍 Processing slide {slide_num} (page {page_num + 1})...")
                
                page = doc[page_num]
                text = page.get_text()
                
                print(f"📄 Page content preview:")
                print(text[:500] + "..." if len(text) > 500 else text)
                print("-" * 50)
                
                # Extract player data from this page
                players = extract_players_from_page(text, slide_num)
                
                if players:
                    extracted_players.extend(players)
                    print(f"✅ Found {len(players)} player(s) on slide {slide_num}")
                    for player in players:
                        print(f"   - {player['name']} ({player['category']}, Age: {player['age']})")
                else:
                    print(f"❌ No player data found on slide {slide_num}")
                    
                    # Try to extract any text that might be player info
                    lines = text.split('\n')
                    print(f"📝 All text lines on this page:")
                    for i, line in enumerate(lines):
                        if line.strip():
                            print(f"   {i+1:2d}: {line.strip()}")
            else:
                print(f"❌ Slide {slide_num} is beyond PDF page range ({total_pages})")
        
        doc.close()
        
        print(f"\n📊 Extraction Results:")
        print(f"  Missing slides processed: {len(missing_slides)}")
        print(f"  Players found: {len(extracted_players)}")
        
        if extracted_players:
            # Load existing data
            existing_data_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/complete_pdf_players_data.json'
            existing_players = []
            
            if os.path.exists(existing_data_path):
                with open(existing_data_path, 'r', encoding='utf-8') as f:
                    existing_players = json.load(f)
                print(f"📁 Loaded existing data: {len(existing_players)} players")
            
            # Merge new data with existing data
            merged_players = merge_player_data(existing_players, extracted_players)
            
            print(f"📊 After merging:")
            print(f"  Total players: {len(merged_players)}")
            
            # Save updated data
            save_updated_data(merged_players, extracted_players)
            
            return extracted_players
        else:
            print("❌ No new player data found for missing slides")
            return []
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def extract_players_from_page(text, slide_num):
    """Extract player data from a single page with comprehensive patterns"""
    
    players = []
    lines = text.split('\n')
    
    print(f"🔍 Analyzing {len(lines)} lines of text...")
    
    # Pattern 1: Look for explicit "Name:" patterns
    for i, line in enumerate(lines):
        line = line.strip()
        
        if line.startswith('Name:'):
            player = extract_player_from_name_line(lines, i, slide_num)
            if player:
                players.append(player)
                print(f"✅ Found player via Name: pattern - {player['name']}")
        
        # Pattern 2: Look for name-like patterns followed by category/age info
        elif re.match(r'^[A-Za-z][A-Za-z\s\.\-]+$', line) and len(line) > 2 and len(line) < 50:
            # Check if this looks like a player name
            if is_likely_player_name(lines, i):
                player = extract_player_from_name_line(lines, i, slide_num, has_name_prefix=False)
                if player:
                    players.append(player)
                    print(f"✅ Found player via name pattern - {player['name']}")
    
    # Pattern 3: Look for structured data in tables or lists
    structured_players = extract_structured_players(text, slide_num)
    players.extend(structured_players)
    
    return players

def is_likely_player_name(lines, start_idx):
    """Check if a line is likely a player name by analyzing context"""
    
    # Look at next 10 lines for category, age, phone patterns
    for i in range(start_idx + 1, min(start_idx + 11, len(lines))):
        line = lines[i].strip()
        
        # Check for category indicators
        if (line.startswith('Category:') or 
            line.startswith('Age:') or 
            line.startswith('Ph:') or
            'Batsman' in line or
            'Bowler' in line or
            'All Rounder' in line or
            'Wicket Keeper' in line or
            re.match(r'\d+\s*years?', line) or  # Age pattern
            re.match(r'\d{10}', line)):  # Phone number pattern
            return True
    
    return False

def extract_player_from_name_line(lines, start_idx, slide_num, has_name_prefix=True):
    """Extract player data starting from a name line"""
    
    player = {}
    
    # Extract name
    name_line = lines[start_idx].strip()
    if has_name_prefix:
        name = name_line.replace('Name:', '').strip()
    else:
        name = name_line
    
    # Clean name
    name = re.sub(r'\s+', ' ', name).strip()
    
    if not name or len(name) < 2:
        return None
    
    player['name'] = name
    player['slide_number'] = slide_num
    
    # Look for category, age, phone in following lines
    j = start_idx + 1
    while j < len(lines) and j < start_idx + 15:  # Look within next 15 lines
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
        elif re.match(r'^\d+\s*years?$', line):  # Age without prefix
            age_match = re.search(r'(\d+)', line)
            if age_match:
                player['age'] = age_match.group(1)
        elif re.match(r'^\d{10}$', line):  # Phone without prefix
            player['mobile'] = line
        elif line in ['Batsman', 'Bowler', 'All Rounder', 'Wicket Keeper']:
            player['category'] = line
        
        j += 1
    
    # Only return if we have essential data
    if 'name' in player and len(player['name']) > 2:
        # Set defaults for missing fields
        if 'category' not in player:
            player['category'] = 'Unknown'
        if 'age' not in player:
            player['age'] = '0'
        if 'mobile' not in player:
            player['mobile'] = ''
        if 'iconPlayer' not in player:
            player['iconPlayer'] = 'No'
        
        return player
    
    return None

def extract_structured_players(text, slide_num):
    """Extract players from structured data (tables, lists)"""
    
    players = []
    
    # Pattern for structured data like: Name | Category | Age | Phone
    structured_pattern = r'([A-Za-z\s\.\-]+?)\s*\|\s*([A-Za-z\s]+?)\s*\|\s*(\d+)\s*\|\s*(\d+)'
    matches = re.findall(structured_pattern, text)
    
    for match in matches:
        if len(match) >= 4:
            name = match[0].strip()
            category = match[1].strip()
            age = match[2].strip()
            phone = match[3].strip()
            
            if len(name) > 2 and len(category) > 2:
                player = {
                    'slide_number': slide_num,
                    'name': name,
                    'category': category,
                    'age': age,
                    'mobile': phone,
                    'iconPlayer': 'No',
                    'source': 'PDF_STRUCTURED'
                }
                players.append(player)
                print(f"✅ Found structured player - {name}")
    
    return players

def merge_player_data(existing_players, new_players):
    """Merge new player data with existing data"""
    
    # Create a set of existing slide numbers for quick lookup
    existing_slides = {p['slide_number'] for p in existing_players}
    
    merged = existing_players.copy()
    
    for new_player in new_players:
        slide_num = new_player['slide_number']
        
        if slide_num not in existing_slides:
            merged.append(new_player)
            print(f"➕ Added new player from slide {slide_num}: {new_player['name']}")
        else:
            print(f"⚠️  Slide {slide_num} already exists in data")
    
    # Sort by slide number
    merged.sort(key=lambda x: x['slide_number'])
    
    return merged

def save_updated_data(all_players, new_players):
    """Save the updated player data"""
    
    if not all_players:
        print("❌ No data to save")
        return
    
    # Save as JSON
    json_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/complete_pdf_players_data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_players, f, indent=2, ensure_ascii=False)
    print(f"✅ Updated JSON: {json_path}")
    
    # Save new players separately
    if new_players:
        new_players_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/missing_slides_players.json'
        with open(new_players_path, 'w', encoding='utf-8') as f:
            json.dump(new_players, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved new players: {new_players_path}")
    
    # Generate summary
    summary_path = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/missing_slides_summary.txt'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("Missing Slides Extraction Summary\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Missing slides processed: [22, 32, 46, 84, 100]\n")
        f.write(f"New players found: {len(new_players)}\n")
        f.write(f"Total players after merge: {len(all_players)}\n")
        f.write(f"Extraction date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if new_players:
            f.write("New players found:\n")
            for player in new_players:
                f.write(f"  Slide {player['slide_number']}: {player['name']} - {player['category']} - Age: {player['age']}\n")
        else:
            f.write("No new players found in missing slides.\n")
            f.write("This could mean:\n")
            f.write("  1. The slides contain no player data\n")
            f.write("  2. The slides contain non-player content (headers, summaries, etc.)\n")
            f.write("  3. The extraction patterns need adjustment\n")
    
    print(f"✅ Saved summary: {summary_path}")

if __name__ == "__main__":
    extract_missing_slides()
