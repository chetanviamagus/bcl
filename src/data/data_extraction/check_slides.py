#!/usr/bin/env python3
"""
Script to check the number of slides in the extracted data
"""

import json

def check_slides():
    # Read the JSON data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print("BCL Slides Analysis")
    print("=" * 50)
    print(f"Total players: {len(players_data)}")
    
    # Get all slide numbers
    slide_numbers = [player.get('slide_number', 0) for player in players_data]
    slide_numbers = sorted(set(slide_numbers))
    
    print(f"Slide numbers found: {len(slide_numbers)}")
    print(f"Slide range: {min(slide_numbers)} to {max(slide_numbers)}")
    
    # Check for missing slides
    expected_slides = list(range(min(slide_numbers), max(slide_numbers) + 1))
    missing_slides = [s for s in expected_slides if s not in slide_numbers]
    
    print(f"\nMissing slide numbers: {missing_slides}")
    print(f"Number of missing slides: {len(missing_slides)}")
    
    # Show slide distribution
    print(f"\nSlide distribution:")
    for slide in slide_numbers:
        players_in_slide = [p for p in players_data if p.get('slide_number') == slide]
        print(f"  Slide {slide}: {len(players_in_slide)} player(s)")
    
    # Check for ICON players by slide
    print(f"\nICON players by slide:")
    icon_by_slide = {}
    for player in players_data:
        slide = player.get('slide_number')
        if player.get('iconPlayer') == 'Yes':
            if slide not in icon_by_slide:
                icon_by_slide[slide] = []
            icon_by_slide[slide].append(player.get('name', 'Unknown'))
    
    for slide in sorted(icon_by_slide.keys()):
        print(f"  Slide {slide}: {icon_by_slide[slide]}")
    
    print(f"\nTotal slides with players: {len(slide_numbers)}")
    print(f"Total slides with ICON players: {len(icon_by_slide)}")

if __name__ == "__main__":
    check_slides()
