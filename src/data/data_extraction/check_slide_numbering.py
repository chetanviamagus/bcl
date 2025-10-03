#!/usr/bin/env python3
"""
Script to check the correct slide numbering
"""

import json

def check_slide_numbering():
    # Read the JSON data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print("BCL Slide Numbering Check")
    print("=" * 50)
    print(f"Total players: {len(players_data)}")
    
    # Get all slide numbers
    slide_numbers = [player.get('slide_number', 0) for player in players_data]
    slide_numbers = sorted(set(slide_numbers))
    
    print(f"Current slide numbers: {slide_numbers[:10]}...{slide_numbers[-5:]}")
    print(f"Slide range: {min(slide_numbers)} to {max(slide_numbers)}")
    
    # Check if slide 1 exists
    slide_1_players = [p for p in players_data if p.get('slide_number') == 1]
    print(f"\nPlayers in slide 1: {len(slide_1_players)}")
    for player in slide_1_players:
        print(f"  - {player.get('name', 'Unknown')}")
    
    # Check for Manjunath.P
    manjunath_players = [p for p in players_data if 'manjunath' in p.get('name', '').lower()]
    print(f"\nAll Manjunath players:")
    for player in manjunath_players:
        print(f"  - {player.get('name', 'Unknown')} (Slide {player.get('slide_number', '?')})")
    
    # If slide 1 should be Manjunath.P, we need to adjust the numbering
    # Let's check what the actual first slide should be
    print(f"\nFirst few players by current slide number:")
    sorted_players = sorted(players_data, key=lambda x: x.get('slide_number', 0))
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

if __name__ == "__main__":
    check_slide_numbering()
