#!/usr/bin/env python3
"""
Script to verify the actual data statistics
"""

import json

def verify_data():
    # Read the JSON data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print("BCL Data Verification")
    print("=" * 50)
    print(f"Total players: {len(players_data)}")
    
    # Count ICON vs Regular players
    icon_players = [p for p in players_data if p.get('iconPlayer') == 'Yes']
    regular_players = [p for p in players_data if p.get('iconPlayer') == 'No']
    
    print(f"ICON players: {len(icon_players)} ({len(icon_players)/len(players_data)*100:.1f}%)")
    print(f"Regular players: {len(regular_players)} ({len(regular_players)/len(players_data)*100:.1f}%)")
    
    # Category breakdown for ICON players
    icon_categories = {}
    for player in icon_players:
        cat = player.get('category', 'Unknown')
        icon_categories[cat] = icon_categories.get(cat, 0) + 1
    
    print(f"\nICON Players by Category:")
    for cat, count in sorted(icon_categories.items()):
        print(f"  {cat}: {count} players")
    
    # Age statistics for ICON players
    icon_ages = []
    for player in icon_players:
        try:
            age = int(player.get('age', 0))
            if age > 0:
                icon_ages.append(age)
        except (ValueError, TypeError):
            pass
    
    if icon_ages:
        print(f"\nICON Players Age Statistics:")
        print(f"  Youngest: {min(icon_ages)} years")
        print(f"  Oldest: {max(icon_ages)} years")
        print(f"  Average: {sum(icon_ages)/len(icon_ages):.1f} years")
    
    # Age statistics for Regular players
    regular_ages = []
    for player in regular_players:
        try:
            age = int(player.get('age', 0))
            if age > 0:
                regular_ages.append(age)
        except (ValueError, TypeError):
            pass
    
    if regular_ages:
        print(f"\nRegular Players Age Statistics:")
        print(f"  Youngest: {min(regular_ages)} years")
        print(f"  Oldest: {max(regular_ages)} years")
        print(f"  Average: {sum(regular_ages)/len(regular_ages):.1f} years")
    
    # Show some examples
    print(f"\nSample ICON Players:")
    for i, player in enumerate(icon_players[:10]):
        print(f"  {i+1}. {player.get('name', 'Unknown')} ({player.get('age', '?')} years, {player.get('category', 'Unknown')})")
    
    print(f"\nSample Regular Players:")
    for i, player in enumerate(regular_players[:10]):
        print(f"  {i+1}. {player.get('name', 'Unknown')} ({player.get('age', '?')} years, {player.get('category', 'Unknown')})")
    
    # Check for any data issues
    print(f"\nData Quality Check:")
    missing_icon = [p for p in players_data if 'iconPlayer' not in p]
    if missing_icon:
        print(f"  Players missing iconPlayer field: {len(missing_icon)}")
    else:
        print(f"  All players have iconPlayer field: ✅")
    
    missing_mobile = [p for p in players_data if not p.get('mobile')]
    print(f"  Players missing mobile numbers: {len(missing_mobile)}")
    
    # Check for unusual ages
    unusual_ages = []
    for player in players_data:
        try:
            age = int(player.get('age', 0))
            if age < 12 or age > 50:
                unusual_ages.append((player.get('name', 'Unknown'), age))
        except (ValueError, TypeError):
            pass
    
    if unusual_ages:
        print(f"  Players with unusual ages:")
        for name, age in unusual_ages[:5]:
            print(f"    {name}: {age} years")

if __name__ == "__main__":
    verify_data()
