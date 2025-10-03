#!/usr/bin/env python3
"""
Script to update the TypeScript players_data.ts file with iconPlayer field
"""

import json
import re

def update_ts_file():
    # Read the updated JSON data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
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
    
    for i, player in enumerate(players_data):
        ts_content += '  {\n'
        ts_content += f'    "slide_number": {player["slide_number"]},\n'
        ts_content += f'    "name": "{player["name"]}",\n'
        ts_content += f'    "age": "{player["age"]}",\n'
        ts_content += f'    "category": "{player["category"]}",\n'
        ts_content += f'    "mobile": "{player["mobile"]}",\n'
        ts_content += f'    "iconPlayer": "{player["iconPlayer"]}"\n'
        ts_content += '  }'
        if i < len(players_data) - 1:
            ts_content += ','
        ts_content += '\n'
    
    ts_content += '];\n'
    
    # Write to TypeScript file
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"✅ Updated TypeScript file with {len(players_data)} players")
    print(f"   - ICON players: {len([p for p in players_data if p['iconPlayer'] == 'Yes'])}")
    print(f"   - Regular players: {len([p for p in players_data if p['iconPlayer'] == 'No'])}")

if __name__ == "__main__":
    update_ts_file()
