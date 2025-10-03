#!/usr/bin/env python3
"""
Script to fix slide numbering by subtracting 1 from all slide numbers
"""

import json

def fix_slide_numbering():
    # Read the current JSON data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print("Fixing Slide Numbering")
    print("=" * 50)
    print(f"Total players: {len(players_data)}")
    
    # Fix slide numbers by subtracting 1
    corrected_players = []
    for player in players_data:
        corrected_player = {
            **player,
            "slide_number": player.get('slide_number', 2) - 1
        }
        corrected_players.append(corrected_player)
    
    # Show the corrected first few players
    print(f"\nCorrected first few players:")
    sorted_players = sorted(corrected_players, key=lambda x: x.get('slide_number', 0))
    for i, player in enumerate(sorted_players[:10]):
        print(f"  Slide {player.get('slide_number', '?')}: {player.get('name', 'Unknown')}")
    
    # Check slide range
    slide_numbers = [player.get('slide_number', 0) for player in corrected_players]
    slide_numbers = sorted(set(slide_numbers))
    
    print(f"\nCorrected slide range: {min(slide_numbers)} to {max(slide_numbers)}")
    print(f"Total slides with players: {len(slide_numbers)}")
    
    # Check for Manjunath.P in slide 1
    slide_1_players = [p for p in corrected_players if p.get('slide_number') == 1]
    print(f"\nPlayers in slide 1: {len(slide_1_players)}")
    for player in slide_1_players:
        print(f"  - {player.get('name', 'Unknown')}")
    
    # Save corrected data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'w', encoding='utf-8') as f:
        json.dump(corrected_players, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Corrected slide numbering saved to JSON file")
    
    # Update TypeScript file
    update_ts_file(corrected_players)
    
    return corrected_players

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
    
    print(f"✅ Updated TypeScript file with corrected slide numbers")

if __name__ == "__main__":
    fix_slide_numbering()
