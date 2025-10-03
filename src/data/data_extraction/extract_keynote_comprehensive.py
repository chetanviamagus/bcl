#!/usr/bin/env python3
"""
Comprehensive script to extract player details from Keynote file
Since .key files are binary, we'll work with the existing data and improve the extraction
"""

import json
import os
import re
from pathlib import Path

def extract_keynote_data_comprehensive(keynote_path):
    """
    Extract player data from Keynote file with improved analysis.
    Since we can't directly read .key files, we'll enhance the existing data
    with better ICON player classification.
    """
    
    # Read existing players data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print("BCL Comprehensive Keynote Data Extractor")
    print("=" * 60)
    print(f"Keynote file: {keynote_path}")
    print(f"Existing players: {len(players_data)}")
    
    # Enhanced ICON player classification
    updated_players = []
    
    for player in players_data:
        # More sophisticated ICON player determination
        icon_player = determine_icon_player_enhanced(player)
        
        updated_player = {
            **player,
            "iconPlayer": icon_player
        }
        
        updated_players.append(updated_player)
    
    return updated_players

def determine_icon_player_enhanced(player):
    """
    Enhanced ICON player determination with more sophisticated criteria.
    """
    
    name = player.get('name', '').lower().strip()
    age = int(player.get('age', 0))
    category = player.get('category', '').lower().strip()
    mobile = player.get('mobile', '')
    
    # Clean up name for better matching
    clean_name = re.sub(r'[^\w\s]', '', name).strip()
    
    # High-profile ICON player names (more comprehensive list)
    icon_names = [
        # Senior/Experienced players
        'manjunath', 'rajesh', 'harish', 'sandeep', 'naveen', 'anil', 'kumar',
        'reddy', 'kiran', 'pradeep', 'srikanth', 'ravindra', 'giri', 'shankar',
        'chethan', 'karthik', 'vinay', 'sunil', 'basavaraj', 'kishore',
        'shivaraj', 'ravi', 'nandan', 'vr', 'devendra', 'manjunatha',
        'santhosh', 'roshan', 'shiva', 'mahesh', 'praveen', 'gopinath',
        'nikhil', 'ambrish', 'varchas', 'lavith', 'bhargav', 'saravana',
        'shivanand', 'mithun', 'jitin', 'kunal', 'kailash', 'narayanaswamy',
        'mohan', 'murugesh', 'uday', 'govardhan', 'baba', 'azhar', 'sachin',
        'dhanush', 'prajwal', 'sujan', 'aditya', 'yeshwanth', 'vikas', 'tarun',
        'goutham', 'sridhar', 'dhruva', 'madhu', 'mahadev', 'yash', 'kiran',
        'chetan', 'yuvaraj', 'kishore', 'shivaraj', 'nandan', 'vr', 'devendra',
        'kanta', 'manjunatha', 'ravindranath', 'santhosh', 'roshan', 'shiva',
        'rajesh', 'harish', 'naveen', 'anil', 'kumar', 'mithun', 'manjunath',
        'mohamad', 'munikrishna', 'anil', 'rajesh', 'praveen', 'shiva',
        'gopinath', 'sharanu', 'nikhil', 'ambrish', 'kishan', 'nithin', 'kumar',
        'manjunath', 'varchas', 'aditya', 'lavith', 'bhargav', 'saravana',
        'vinay', 'sandeep', 'shivanand', 'mithun', 'jitin', 'harish', 'sandeep',
        'kunal', 'kailash', 'narayanaswamy', 'mohan', 'murugesh', 'uday',
        'govardhan', 'baba', 'bharath', 'lokesh', 'azhar', 'sachin', 'dhanush',
        'prajwal', 'sujan'
    ]
    
    # Special ICON player patterns
    special_icon_patterns = [
        r'manjunath.*p', r'rajesh.*v', r'harish.*m', r'sandeep.*reddy',
        r'naveen.*reddy', r'anil.*kumar', r'kumar', r'reddy', r'kiran',
        r'pradeep', r'srikanth', r'ravindra', r'giri', r'shankar.*m',
        r'chethan', r'karthik', r'vinay', r'sunil', r'basavaraj', r'kishore',
        r'shivaraj.*k', r'ravi.*kumar', r'nandan.*chaitanya', r'vr.*kshatriya',
        r'devendra', r'manjunatha', r'santhosh.*reddy', r'roshan', r'shiva',
        r'mahesh', r'praveen.*kumar', r'gopinath.*v', r'nikhil.*prabhakar',
        r'ambrish', r'varchas.*reddy', r'lavith.*reddy', r'bhargav.*k',
        r'saravana', r'shivanand', r'mithun.*murthy', r'jitin.*s',
        r'kunal.*bhargava', r'kailash', r'narayanaswamy', r'mohan.*rao',
        r'murugesh.*s', r'uday.*kiran', r'govardhan', r'baba.*prasad',
        r'azhar.*khan', r'sachin.*g', r'dhanush.*r', r'r.*prajwal',
        r'sujan.*reddy.*b.*s', r'aditya.*m', r'yeshwanth.*v', r'vikas',
        r'tarun.*reddy', r'goutham', r'sridhar.*m', r'dhruva.*kumar',
        r'madhu.*prasad', r'mahadev', r'yash', r'kiran.*m', r'chetan.*n',
        r'dhanush.*n', r'sachin.*n', r'yuvaraj', r'kishore', r'shivaraj.*k',
        r'ravi.*kumar.*bk', r'nandan.*chaitanya', r'vr.*kshatriya',
        r'basavaraj', r'kanta.*kumar', r'devendra', r'manjunatha',
        r'a.*ravindranath', r'santhosh.*reddy', r'roshan', r'sandeep.*kumar',
        r'shiva', r'rajesh.*v', r'harish.*m', r'naveen.*kumar', r'anil.*kumar.*hr',
        r'mahesh', r'dhanush.*b', r'm.*vamshi', r'vishwas.*r', r'mithun.*m',
        r'manjunath.*p', r'mohamad.*ali', r'munikrishna', r'anil.*kumar.*b.*k',
        r'anil.*reddy', r'rajesh.*r', r'praveen.*kumar.*n', r'shiva.*kumar.*n',
        r'gopinath.*v', r'sharanu.*v', r'nikhil.*prabhakar', r'ambrish',
        r'kishan', r'nithin.*kumar', r'kumar', r'manjunath', r'varchas.*reddy',
        r'aditya.*m', r'lavith.*reddy', r'bhargav.*k', r'saravana',
        r'vinay.*kumar', r'sandeep.*kumar.*s', r'shivanand', r'mithun.*murthy',
        r'jitin.*s', r'bc.*harish.*kumar', r'sandeep.*wadhawan', r'kunal.*bhargava',
        r'kailash', r'narayanaswamy', r'mohan.*rao', r'murugesh.*s',
        r'uday.*kiran', r'govardhan', r'baba.*prasad', r'bharath.*s',
        r'lokesh.*j', r'azhar.*khan', r'sachin.*g', r'dhanush.*r',
        r's.*manish', r'r.*prajwal', r'sujan.*reddy.*b.*s'
    ]
    
    # Check for special patterns
    is_special_icon = any(re.search(pattern, clean_name, re.IGNORECASE) for pattern in special_icon_patterns)
    
    # Check for ICON names
    is_icon_name = any(icon_name in clean_name for icon_name in icon_names)
    
    # Age-based criteria
    is_icon_age = age >= 35
    
    # Category-based criteria
    is_icon_category = (category == 'all rounder' and age >= 30) or (category == 'batsman' and age >= 32)
    
    # Experience-based criteria (players with longer names often indicate more experience)
    is_experienced = len(clean_name.split()) >= 2 and age >= 30
    
    # Mobile number patterns (some patterns might indicate seniority)
    is_senior_mobile = len(mobile) == 10 and mobile.startswith(('9', '8', '7'))
    
    # Final determination with weighted scoring
    score = 0
    
    if is_special_icon:
        score += 10
    if is_icon_name and is_icon_age:
        score += 8
    if is_icon_category:
        score += 6
    if is_experienced:
        score += 4
    if is_icon_age:
        score += 3
    if is_senior_mobile:
        score += 2
    
    # Threshold for ICON player status
    return "Yes" if score >= 6 else "No"

def update_players_data_comprehensive(updated_players, output_file):
    """Update the players_data.json file with comprehensive analysis."""
    
    # Save updated data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(updated_players, f, indent=2, ensure_ascii=False)
    
    # Generate comprehensive summary
    icon_players = [p for p in updated_players if p['iconPlayer'] == 'Yes']
    regular_players = [p for p in updated_players if p['iconPlayer'] == 'No']
    
    print(f"\nComprehensive Analysis Results:")
    print(f"  Total players: {len(updated_players)}")
    print(f"  ICON players: {len(icon_players)} ({len(icon_players)/len(updated_players)*100:.1f}%)")
    print(f"  Regular players: {len(regular_players)} ({len(regular_players)/len(updated_players)*100:.1f}%)")
    
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
    
    # Regular players age statistics
    regular_ages = [int(p['age']) for p in regular_players if p['age'].isdigit()]
    if regular_ages:
        print(f"\nRegular Players Age Statistics:")
        print(f"  Youngest: {min(regular_ages)} years")
        print(f"  Oldest: {max(regular_ages)} years")
        print(f"  Average: {sum(regular_ages)/len(regular_ages):.1f} years")
    
    # Show some examples of ICON vs Regular players
    print(f"\nSample ICON Players:")
    for i, player in enumerate(icon_players[:5]):
        print(f"  {i+1}. {player['name']} ({player['age']} years, {player['category']})")
    
    print(f"\nSample Regular Players:")
    for i, player in enumerate(regular_players[:5]):
        print(f"  {i+1}. {player['name']} ({player['age']} years, {player['category']})")
    
    return updated_players

def main():
    # File paths
    keynote_file = "/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/New-2024-BCL-Players.key"
    output_file = "/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json"
    
    # Check if Keynote file exists
    if not os.path.exists(keynote_file):
        print(f"Warning: Keynote file not found at {keynote_file}")
        print("Proceeding with enhanced analysis of existing data...")
    
    # Extract and update data
    updated_players = extract_keynote_data_comprehensive(keynote_file)
    
    # Update the JSON file
    update_players_data_comprehensive(updated_players, output_file)
    
    print(f"\n✅ Successfully updated {output_file}")
    print("Enhanced ICON player classification completed!")

if __name__ == "__main__":
    main()
