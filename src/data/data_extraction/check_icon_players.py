#!/usr/bin/env python3
"""
Script to check actual ICON players in the data
"""

import json

def check_icon_players():
    # Read the JSON data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print("BCL ICON Players Check")
    print("=" * 50)
    print(f"Total players: {len(players_data)}")
    
    # Count ICON vs Regular players
    icon_players = [p for p in players_data if p.get('iconPlayer') == 'Yes']
    regular_players = [p for p in players_data if p.get('iconPlayer') == 'No']
    
    print(f"ICON players: {len(icon_players)}")
    print(f"Regular players: {len(regular_players)}")
    
    # Show all ICON players with their details
    print(f"\nAll ICON Players:")
    print("-" * 80)
    for i, player in enumerate(icon_players, 1):
        print(f"{i:2d}. {player.get('name', 'Unknown'):<25} | {player.get('age', '?'):>2} years | {player.get('category', 'Unknown'):<12} | Slide {player.get('slide_number', '?')}")
    
    print(f"\nAll Regular Players:")
    print("-" * 80)
    for i, player in enumerate(regular_players, 1):
        print(f"{i:2d}. {player.get('name', 'Unknown'):<25} | {player.get('age', '?'):>2} years | {player.get('category', 'Unknown'):<12} | Slide {player.get('slide_number', '?')}")
    
    # Check for patterns in ICON vs Regular
    print(f"\nAnalysis:")
    print(f"  ICON players: {len(icon_players)} ({len(icon_players)/len(players_data)*100:.1f}%)")
    print(f"  Regular players: {len(regular_players)} ({len(regular_players)/len(players_data)*100:.1f}%)")
    
    # Age analysis
    icon_ages = [int(p.get('age', 0)) for p in icon_players if p.get('age', '').isdigit()]
    regular_ages = [int(p.get('age', 0)) for p in regular_players if p.get('age', '').isdigit()]
    
    if icon_ages:
        print(f"\nICON Players Age Range: {min(icon_ages)}-{max(icon_ages)} years (Avg: {sum(icon_ages)/len(icon_ages):.1f})")
    if regular_ages:
        print(f"Regular Players Age Range: {min(regular_ages)}-{max(regular_ages)} years (Avg: {sum(regular_ages)/len(regular_ages):.1f})")

if __name__ == "__main__":
    check_icon_players()
