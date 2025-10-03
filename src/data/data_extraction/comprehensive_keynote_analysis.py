#!/usr/bin/env python3
"""
Comprehensive analysis of Keynote file to identify ICON players
"""

import json
import zipfile
import xml.etree.ElementTree as ET
import re

def analyze_keynote_file():
    """Analyze the Keynote file to extract slide content and identify ICON players"""
    
    print("🔍 Comprehensive Keynote Analysis")
    print("=" * 60)
    
    # Read current player data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print(f"📊 Current data: {len(players_data)} players")
    
    # Create a mapping of slide numbers to players
    slide_to_player = {}
    for player in players_data:
        slide_num = player.get('slide_number')
        slide_to_player[slide_num] = player
    
    print(f"📋 Players mapped to {len(slide_to_player)} slides")
    
    # Analyze Keynote file
    keynote_file = '/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/New-2024-BCL-Players.key'
    
    try:
        with zipfile.ZipFile(keynote_file, 'r') as zip_file:
            # Get the list of files in the Keynote
            file_list = zip_file.namelist()
            print(f"📁 Keynote contains {len(file_list)} files")
            
            # Look for slide content files
            slide_files = [f for f in file_list if 'slide' in f.lower() and f.endswith('.xml')]
            print(f"🎯 Found {len(slide_files)} potential slide files")
            
            # Try to find the main slide content
            content_files = [f for f in file_list if 'content' in f.lower() or 'slide' in f.lower()]
            print(f"📄 Content files: {content_files[:5]}...")  # Show first 5
            
            # Look for the main presentation file
            main_files = [f for f in file_list if f.endswith('.xml') and ('index' in f or 'presentation' in f)]
            print(f"🎬 Main files: {main_files}")
            
            # Try to extract text from slides
            slide_texts = {}
            
            for file_name in file_list:
                if file_name.endswith('.xml'):
                    try:
                        with zip_file.open(file_name) as f:
                            content = f.read().decode('utf-8', errors='ignore')
                            
                            # Look for slide numbers and text content
                            if 'slide' in content.lower() or 'text' in content.lower():
                                # Extract slide numbers
                                slide_matches = re.findall(r'slide[_-]?(\d+)', content, re.IGNORECASE)
                                if slide_matches:
                                    for slide_num in slide_matches:
                                        slide_num = int(slide_num)
                                        if slide_num not in slide_texts:
                                            slide_texts[slide_num] = []
                                        
                                        # Extract text content
                                        text_matches = re.findall(r'<text[^>]*>([^<]+)</text>', content, re.IGNORECASE)
                                        for text in text_matches:
                                            if text.strip() and len(text.strip()) > 2:
                                                slide_texts[slide_num].append(text.strip())
                                
                                # Also look for direct text content
                                text_content = re.sub(r'<[^>]+>', ' ', content)
                                text_content = re.sub(r'\s+', ' ', text_content).strip()
                                
                                if len(text_content) > 50:  # Only meaningful content
                                    # Try to extract slide number from filename or content
                                    slide_num_match = re.search(r'(\d+)', file_name)
                                    if slide_num_match:
                                        slide_num = int(slide_num_match.group(1))
                                        if slide_num not in slide_texts:
                                            slide_texts[slide_num] = []
                                        slide_texts[slide_num].append(text_content)
                    
                    except Exception as e:
                        continue
            
            print(f"📝 Extracted text from {len(slide_texts)} slides")
            
            # Analyze each slide for ICON indicators
            icon_indicators = [
                'icon', 'star', 'premium', 'vip', 'elite', 'champion', 
                'legend', 'master', 'expert', 'pro', 'ace', 'top',
                'special', 'featured', 'highlighted', 'notable'
            ]
            
            updated_players = []
            icon_count = 0
            
            for player in players_data:
                slide_num = player.get('slide_number')
                player_name = player.get('name', '').lower()
                
                # Check if this slide has ICON indicators
                is_icon = False
                slide_text = slide_texts.get(slide_num, [])
                
                # Combine all text from this slide
                combined_text = ' '.join(slide_text).lower()
                
                # Check for ICON indicators in the slide text
                for indicator in icon_indicators:
                    if indicator in combined_text:
                        is_icon = True
                        print(f"🎯 Slide {slide_num} ({player.get('name')}): Found '{indicator}' indicator")
                        break
                
                # Check for specific patterns that might indicate ICON status
                icon_patterns = [
                    r'\bicon\b',
                    r'\bstar\b',
                    r'\bpremium\b',
                    r'\bvip\b',
                    r'\belite\b',
                    r'\bchampion\b',
                    r'\blegend\b',
                    r'\bmaster\b',
                    r'\bexpert\b',
                    r'\bpro\b',
                    r'\bace\b',
                    r'\btop\b',
                    r'\bspecial\b',
                    r'\bfeatured\b',
                    r'\bhighlighted\b',
                    r'\bnotable\b'
                ]
                
                for pattern in icon_patterns:
                    if re.search(pattern, combined_text, re.IGNORECASE):
                        is_icon = True
                        print(f"🎯 Slide {slide_num} ({player.get('name')}): Found pattern '{pattern}'")
                        break
                
                # Update player status
                updated_player = player.copy()
                if is_icon:
                    updated_player['iconPlayer'] = 'Yes'
                    icon_count += 1
                else:
                    updated_player['iconPlayer'] = 'No'
                
                updated_players.append(updated_player)
            
            print(f"\n📊 Analysis Results:")
            print(f"  Total players: {len(updated_players)}")
            print(f"  ICON players: {icon_count}")
            print(f"  Regular players: {len(updated_players) - icon_count}")
            
            # Show first few ICON players
            icon_players = [p for p in updated_players if p.get('iconPlayer') == 'Yes']
            print(f"\n🏆 ICON Players (first 20):")
            for i, player in enumerate(icon_players[:20]):
                print(f"  {i+1:2d}. Slide {player.get('slide_number'):3d}: {player.get('name')}")
            
            if len(icon_players) > 20:
                print(f"  ... and {len(icon_players) - 20} more")
            
            # Save updated data
            with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'w', encoding='utf-8') as f:
                json.dump(updated_players, f, indent=2, ensure_ascii=False)
            
            # Update TypeScript file
            update_ts_file(updated_players)
            
            print(f"\n✅ Updated players_data.json and players_data.ts")
            
            return updated_players
            
    except Exception as e:
        print(f"❌ Error analyzing Keynote file: {e}")
        return None

def update_ts_file(players):
    """Update the TypeScript file with the new data"""
    ts_content = 'export interface PlayerData {\n'
    ts_content += '  slide_number: number;\n'
    ts_content += '  name: string;\n'
    ts_content += '  age: string;\n'
    ts_content += '  category: string;\n'
    ts_content += '  mobile: string;\n'
    ts_content += '  iconPlayer: string;\n'
    ts_content += '}\n\n'
    ts_content += 'export const playersData: PlayerData[] = [\n'
    
    for i, player in enumerate(players):
        ts_content += '  {\n'
        ts_content += f'    "slide_number": {player["slide_number"]},\n'
        ts_content += f'    "name": "{player["name"]}",\n'
        ts_content += f'    "age": "{player["age"]}",\n'
        ts_content += f'    "category": "{player["category"]}",\n'
        ts_content += f'    "mobile": "{player["mobile"]}",\n'
        ts_content += f'    "iconPlayer": "{player["iconPlayer"]}"\n'
        ts_content += '  }'
        if i < len(players) - 1:
            ts_content += ','
        ts_content += '\n'
    
    ts_content += '];\n'
    
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)

if __name__ == "__main__":
    analyze_keynote_file()
