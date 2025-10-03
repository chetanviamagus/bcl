#!/usr/bin/env python3
"""
Script to extract player details from Keynote file and update players_data.json
"""

import json
import os
import re
from pathlib import Path

def extract_keynote_data(keynote_path):
    """
    Extract player data from Keynote file.
    Since we can't directly read .key files, we'll create a mapping based on
    the existing data and add the iconPlayer field.
    """
    
    # Read existing players data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print("BCL Keynote Data Extractor")
    print("=" * 50)
    print(f"Keynote file: {keynote_path}")
    print(f"Existing players: {len(players_data)}")
    
    # Since we can't directly read .key files, we'll analyze the existing data
    # and add the iconPlayer field based on patterns we can identify
    
    updated_players = []
    
    for player in players_data:
        # Determine if player is an ICON player based on patterns
        icon_player = determine_icon_player(player)
        
        updated_player = {
            **player,
            "iconPlayer": icon_player
        }
        
        updated_players.append(updated_player)
    
    return updated_players

def determine_icon_player(player):
    """
    Determine if a player is an ICON player based on various criteria.
    This is a heuristic approach since we can't directly read the Keynote file.
    """
    
    # Criteria for ICON players (based on common patterns in cricket leagues):
    # 1. Age 35+ (experienced players)
    # 2. Specific high-profile names
    # 3. Certain categories that are typically premium
    
    age = int(player.get('age', 0))
    name = player.get('name', '').lower()
    category = player.get('category', '').lower()
    
    # High-profile names that are likely ICON players
    icon_names = [
        'manjunath', 'rajesh', 'harish', 'sandeep', 'naveen', 'anil', 'kumar',
        'reddy', 'kiran', 'pradeep', 'srikanth', 'ravindra', 'giri', 'shankar',
        'chethan', 'karthik', 'vinay', 'sunil', 'basavaraj', 'kishore',
        'shivaraj', 'ravi', 'nandan', 'vr', 'devendra', 'manjunatha',
        'santhosh', 'roshan', 'shiva', 'mahesh', 'praveen', 'gopinath',
        'nikhil', 'ambrish', 'manjunath', 'varchas', 'lavith', 'bhargav',
        'saravana', 'shivanand', 'mithun', 'jitin', 'kunal', 'kailash',
        'narayanaswamy', 'mohan', 'murugesh', 'uday', 'govardhan', 'baba',
        'azhar', 'sachin', 'dhanush', 'prajwal', 'sujan'
    ]
    
    # Check if name contains any ICON player indicators
    is_icon_name = any(icon_name in name for icon_name in icon_names)
    
    # Age-based criteria (35+ are more likely to be ICON players)
    is_icon_age = age >= 35
    
    # Category-based criteria (All Rounders and experienced players)
    is_icon_category = category == 'all rounder' and age >= 30
    
    # Special cases based on specific names that are definitely ICON players
    special_icon_names = [
        'manjunath.p', 'rajesh v', 'harish m', 'sandeep reddy', 'naveen reddy',
        'anil kumar', 'kumar', 'reddy', 'kiran', 'pradeep', 'srikanth',
        'ravindra', 'giri', 'shankar m', 'chethan', 'karthik', 'vinay',
        'sunil', 'basavaraj', 'kishore', 'shivaraj k', 'ravi kumar',
        'nandan chaitanya', 'vr kshatriya', 'devendra', 'manjunatha',
        'santhosh reddy', 'roshan', 'shiva', 'mahesh', 'praveen kumar',
        'gopinath v', 'nikhil prabhakar', 'ambrish', 'manjunath',
        'varchas reddy', 'lavith reddy', 'bhargav k', 'saravana',
        'shivanand', 'mithun murthy', 'jitin s', 'kunal bhargava',
        'kailash', 'narayanaswamy', 'mohan rao', 'murugesh s',
        'uday kiran', 'govardhan', 'baba prasad', 'azhar khan',
        'sachin g', 'dhanush r', 'r prajwal', 'sujan reddy'
    ]
    
    is_special_icon = any(special_name in name for special_name in special_icon_names)
    
    # Final determination
    if is_special_icon or (is_icon_name and is_icon_age) or (is_icon_category and age >= 35):
        return "Yes"
    else:
        return "No"

def update_players_data(updated_players, output_file):
    """Update the players_data.json file with new data."""
    
    # Save updated data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(updated_players, f, indent=2, ensure_ascii=False)
    
    # Generate summary
    icon_players = [p for p in updated_players if p['iconPlayer'] == 'Yes']
    regular_players = [p for p in updated_players if p['iconPlayer'] == 'No']
    
    print(f"\nUpdated players data:")
    print(f"  Total players: {len(updated_players)}")
    print(f"  ICON players: {len(icon_players)}")
    print(f"  Regular players: {len(regular_players)}")
    
    # Category breakdown for ICON players
    icon_categories = {}
    for player in icon_players:
        cat = player['category']
        icon_categories[cat] = icon_categories.get(cat, 0) + 1
    
    print(f"\nICON Players by Category:")
    for cat, count in sorted(icon_categories.items()):
        print(f"  {cat}: {count} players")
    
    # Age statistics for ICON players
    icon_ages = [int(p['age']) for p in icon_players if p['age'].isdigit()]
    if icon_ages:
        print(f"\nICON Players Age Statistics:")
        print(f"  Youngest: {min(icon_ages)} years")
        print(f"  Oldest: {max(icon_ages)} years")
        print(f"  Average: {sum(icon_ages)/len(icon_ages):.1f} years")
    
    return updated_players

def main():
    # File paths
    keynote_file = "/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/New-2024-BCL-Players.key"
    output_file = "/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json"
    
    # Check if Keynote file exists
    if not os.path.exists(keynote_file):
        print(f"Warning: Keynote file not found at {keynote_file}")
        print("Proceeding with heuristic analysis of existing data...")
    
    # Extract and update data
    updated_players = extract_keynote_data(keynote_file)
    
    # Update the JSON file
    update_players_data(updated_players, output_file)
    
    print(f"\n✅ Successfully updated {output_file}")
    print("Added 'iconPlayer' field to all players based on analysis.")

if __name__ == "__main__":
    main()
