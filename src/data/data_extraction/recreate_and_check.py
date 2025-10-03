#!/usr/bin/env python3
"""
Script to recreate JSON and check slide numbering
"""

import json
import re

def recreate_json_from_ts():
    # Read the TypeScript file
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.ts', 'r', encoding='utf-8') as f:
        ts_content = f.read()
    
    # Find the array content between [ and ];
    start = ts_content.find('export const playersData: PlayerData[] = [')
    if start == -1:
        print("Could not find playersData array")
        return []
    
    start = ts_content.find('[', start) + 1
    end = ts_content.rfind('];')
    
    array_content = ts_content[start:end]
    
    # Parse the TypeScript array to Python objects
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
    
    return players

def check_slide_numbering(players):
    print("BCL Slide Numbering Check")
    print("=" * 50)
    print(f"Total players: {len(players)}")
    
    # Get all slide numbers
    slide_numbers = [player.get('slide_number', 0) for player in players]
    slide_numbers = sorted(set(slide_numbers))
    
    print(f"Current slide numbers: {slide_numbers[:10]}...{slide_numbers[-5:]}")
    print(f"Slide range: {min(slide_numbers)} to {max(slide_numbers)}")
    
    # Check if slide 1 exists
    slide_1_players = [p for p in players if p.get('slide_number') == 1]
    print(f"\nPlayers in slide 1: {len(slide_1_players)}")
    for player in slide_1_players:
        print(f"  - {player.get('name', 'Unknown')}")
    
    # Check for Manjunath.P
    manjunath_players = [p for p in players if 'manjunath' in p.get('name', '').lower()]
    print(f"\nAll Manjunath players:")
    for player in manjunath_players:
        print(f"  - {player.get('name', 'Unknown')} (Slide {player.get('slide_number', '?')})")
    
    # Show first few players
    print(f"\nFirst few players by current slide number:")
    sorted_players = sorted(players, key=lambda x: x.get('slide_number', 0))
    for i, player in enumerate(sorted_players[:10]):
        print(f"  Slide {player.get('slide_number', '?')}: {player.get('name', 'Unknown')}")
    
    # Check if we need to adjust slide numbers
    if min(slide_numbers) == 2:
        print(f"\n⚠️  Current numbering starts from slide 2, but you mentioned slide 1 is Manjunath.P")
        print(f"This suggests the slide numbering might be off by 1")
        
        # Show what slide 1 should be
        first_player = sorted_players[0]
        print(f"Current 'first' player: {first_player.get('name', 'Unknown')} in slide {first_player.get('slide_number', '?')}")
        
        if 'manjunath' in first_player.get('name', '').lower():
            print(f"✅ This matches - Manjunath.P should be in slide 1")
        else:
            print(f"❌ This doesn't match - Manjunath.P is not the first player")
    
    # Count total slides
    print(f"\nTotal slides with players: {len(slide_numbers)}")
    print(f"Expected total slides: {max(slide_numbers) - min(slide_numbers) + 1}")
    print(f"Missing slides: {max(slide_numbers) - min(slide_numbers) + 1 - len(slide_numbers)}")

if __name__ == "__main__":
    players = recreate_json_from_ts()
    if players:
        check_slide_numbering(players)
    else:
        print("Failed to recreate JSON from TypeScript")
