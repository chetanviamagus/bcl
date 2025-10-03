#!/usr/bin/env python3
"""
Script to recreate JSON file from TypeScript file
"""

import re
import json

def extract_data_from_ts():
    """Extract player data from TypeScript file and convert to JSON."""
    
    # Read the TypeScript file
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.ts', 'r', encoding='utf-8') as f:
        ts_content = f.read()
    
    # Find the playersData array
    start_marker = 'export const playersData: PlayerData[] = ['
    end_marker = '];'
    
    start_idx = ts_content.find(start_marker)
    if start_idx == -1:
        print("Could not find playersData array in TypeScript file")
        return []
    
    start_idx += len(start_marker)
    end_idx = ts_content.find(end_marker, start_idx)
    if end_idx == -1:
        print("Could not find end of playersData array")
        return []
    
    # Extract the array content
    array_content = ts_content[start_idx:end_idx].strip()
    
    # Parse the TypeScript array to Python objects
    players = []
    
    # Split by player objects (look for opening braces)
    player_blocks = re.split(r'{\s*', array_content)
    
    for block in player_blocks[1:]:  # Skip first empty element
        if not block.strip():
            continue
            
        # Find the closing brace for this player
        brace_count = 0
        end_pos = 0
        for i, char in enumerate(block):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = i
                    break
        
        if end_pos == 0:
            continue
            
        player_block = '{' + block[:end_pos + 1]
        
        # Convert TypeScript object to Python dict
        player_dict = {}
        
        # Extract slide_number
        slide_match = re.search(r'"slide_number":\s*(\d+)', player_block)
        if slide_match:
            player_dict['slide_number'] = int(slide_match.group(1))
        
        # Extract name
        name_match = re.search(r'"name":\s*"([^"]+)"', player_block)
        if name_match:
            player_dict['name'] = name_match.group(1)
        
        # Extract age
        age_match = re.search(r'"age":\s*"([^"]+)"', player_block)
        if age_match:
            player_dict['age'] = age_match.group(1)
        
        # Extract category
        category_match = re.search(r'"category":\s*"([^"]+)"', player_block)
        if category_match:
            player_dict['category'] = category_match.group(1)
        
        # Extract mobile
        mobile_match = re.search(r'"mobile":\s*"([^"]*)"', player_block)
        if mobile_match:
            player_dict['mobile'] = mobile_match.group(1)
        
        # Extract iconPlayer
        icon_match = re.search(r'"iconPlayer":\s*"([^"]+)"', player_block)
        if icon_match:
            player_dict['iconPlayer'] = icon_match.group(1)
        
        if len(player_dict) >= 5:  # At least 5 fields
            players.append(player_dict)
    
    return players

def main():
    print("Recreating JSON from TypeScript file...")
    
    players = extract_data_from_ts()
    
    if not players:
        print("No players extracted from TypeScript file")
        return
    
    # Save to JSON file
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'w', encoding='utf-8') as f:
        json.dump(players, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully recreated JSON with {len(players)} players")
    
    # Show summary
    icon_count = len([p for p in players if p.get('iconPlayer') == 'Yes'])
    regular_count = len([p for p in players if p.get('iconPlayer') == 'No'])
    
    print(f"  - ICON players: {icon_count}")
    print(f"  - Regular players: {regular_count}")

if __name__ == "__main__":
    main()
