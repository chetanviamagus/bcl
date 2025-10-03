#!/usr/bin/env python3
"""
Simple script to convert TypeScript data to JSON
"""

import re
import json

def convert_ts_to_json():
    """Convert TypeScript players data to JSON format."""
    
    # Read the TypeScript file
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the array content between [ and ];
    start = content.find('export const playersData: PlayerData[] = [')
    if start == -1:
        print("Could not find playersData array")
        return
    
    start = content.find('[', start) + 1
    end = content.rfind('];')
    
    array_content = content[start:end]
    
    # Split by player objects
    players = []
    
    # Find all player objects using regex
    pattern = r'{\s*"slide_number":\s*(\d+),\s*"name":\s*"([^"]+)",\s*"age":\s*"([^"]+)",\s*"category":\s*"([^"]+)",\s*"mobile":\s*"([^"]*)",\s*"iconPlayer":\s*"([^"]+)"\s*}'
    
    matches = re.findall(pattern, array_content)
    
    for match in matches:
        player = {
            "slide_number": int(match[0]),
            "name": match[1],
            "age": match[2],
            "category": match[3],
            "mobile": match[4],
            "iconPlayer": match[5]
        }
        players.append(player)
    
    # Save to JSON
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'w', encoding='utf-8') as f:
        json.dump(players, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Converted {len(players)} players from TypeScript to JSON")
    
    # Show summary
    icon_count = len([p for p in players if p.get('iconPlayer') == 'Yes'])
    regular_count = len([p for p in players if p.get('iconPlayer') == 'No'])
    
    print(f"  - ICON players: {icon_count}")
    print(f"  - Regular players: {regular_count}")

if __name__ == "__main__":
    convert_ts_to_json()
