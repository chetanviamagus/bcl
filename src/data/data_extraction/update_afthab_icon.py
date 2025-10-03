#!/usr/bin/env python3
"""
Script to update Afthab as ICON player
"""

import json

def update_afthab_icon():
    # Read the current JSON data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print("Updating Afthab as ICON Player")
    print("=" * 50)
    
    # Find and update Afthab
    updated = False
    for player in players_data:
        if player.get('name', '').lower() == 'afthab':
            print(f"Found Afthab in slide {player.get('slide_number')}")
            print(f"Current status: {player.get('iconPlayer')}")
            player['iconPlayer'] = 'Yes'
            updated = True
            print(f"✅ Updated Afthab to ICON player")
            break
    
    if not updated:
        print("❌ Afthab not found in the data")
        return
    
    # Save updated data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'w', encoding='utf-8') as f:
        json.dump(players_data, f, indent=2, ensure_ascii=False)
    
    # Update TypeScript file
    update_ts_file(players_data)
    
    # Show updated statistics
    icon_players = [p for p in players_data if p.get('iconPlayer') == 'Yes']
    regular_players = [p for p in players_data if p.get('iconPlayer') == 'No']
    
    print(f"\nUpdated Statistics:")
    print(f"  ICON players: {len(icon_players)}")
    print(f"  Regular players: {len(regular_players)}")
    
    # Show first few ICON players
    print(f"\nFirst few ICON players:")
    icon_players_sorted = sorted([p for p in players_data if p.get('iconPlayer') == 'Yes'], key=lambda x: x.get('slide_number', 0))
    for i, player in enumerate(icon_players_sorted[:10]):
        print(f"  Slide {player.get('slide_number', '?')}: {player.get('name', 'Unknown')}")

def update_ts_file(players):
    # Generate TypeScript data
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
    
    # Write to TypeScript file
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"✅ Updated TypeScript file")

if __name__ == "__main__":
    update_afthab_icon()
