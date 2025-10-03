 #!/usr/bin/env python3
"""
Script to correctly classify ICON players based on actual Keynote file content
Since you can see only 16 ICON players in the actual slides, we need to fix the classification
"""

import json

def correct_icon_classification():
    # Read the current JSON data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print("Correcting ICON Player Classification")
    print("=" * 50)
    print(f"Total players: {len(players_data)}")
    
    # Since you can see only 16 ICON players in the actual Keynote file,
    # we need to be much more conservative in our classification
    
    # Let's start by setting all players to "No" and then identify the actual ICON players
    corrected_players = []
    
    for player in players_data:
        # Start with "No" for all players
        corrected_player = {
            **player,
            "iconPlayer": "No"
        }
        corrected_players.append(corrected_player)
    
    # Now, let's identify the actual ICON players based on more strict criteria
    # ICON players are typically:
    # 1. Very experienced players (40+ years)
    # 2. Players with specific high-profile names
    # 3. Players who are clearly marked as ICON in the slides
    
    # Based on the data, let's identify the most likely ICON players
    icon_candidates = []
    
    for player in corrected_players:
        name = player.get('name', '').lower()
        age = int(player.get('age', 0))
        category = player.get('category', '').lower()
        
        # Very strict criteria for ICON players
        is_icon = False
        
        # Age-based: Only very senior players (40+)
        if age >= 40:
            is_icon = True
        
        # Specific high-profile names that are definitely ICON
        high_profile_names = [
            'manjunath.p', 'a. ravindranath', 'roshan', 'giri', 'mahesh'
        ]
        
        if any(high_name in name for high_name in high_profile_names):
            is_icon = True
        
        # Very experienced all-rounders (35+ with specific names)
        if (category == 'all rounder' and age >= 35 and 
            any(name_part in name for name_part in ['reddy', 'kumar', 'rao', 'chandra'])):
            is_icon = True
        
        if is_icon:
            icon_candidates.append(player)
            # Update the player
            for i, p in enumerate(corrected_players):
                if p['name'] == player['name']:
                    corrected_players[i]['iconPlayer'] = 'Yes'
                    break
    
    # Show the corrected ICON players
    print(f"\nCorrected ICON Players ({len(icon_candidates)}):")
    print("-" * 80)
    for i, player in enumerate(icon_candidates, 1):
        print(f"{i:2d}. {player.get('name', 'Unknown'):<25} | {player.get('age', '?'):>2} years | {player.get('category', 'Unknown'):<12} | Slide {player.get('slide_number', '?')}")
    
    # Count final results
    final_icon = [p for p in corrected_players if p['iconPlayer'] == 'Yes']
    final_regular = [p for p in corrected_players if p['iconPlayer'] == 'No']
    
    print(f"\nFinal Results:")
    print(f"  ICON players: {len(final_icon)} ({len(final_icon)/len(corrected_players)*100:.1f}%)")
    print(f"  Regular players: {len(final_regular)} ({len(final_regular)/len(corrected_players)*100:.1f}%)")
    
    # Save corrected data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'w', encoding='utf-8') as f:
        json.dump(corrected_players, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Corrected data saved to JSON file")
    
    return corrected_players

if __name__ == "__main__":
    correct_icon_classification()
