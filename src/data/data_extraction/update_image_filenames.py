#!/usr/bin/env python3
"""
Script to update player image filenames with correct mobile numbers from players_data.json
"""

import json
import os
import re
from pathlib import Path

def load_player_data(json_file):
    """Load player data from JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_name_mapping(players_data):
    """Create a mapping from player names to their mobile numbers."""
    name_to_mobile = {}
    
    for player in players_data:
        name = player['name'].strip()
        mobile = player['mobile'].strip()
        
        if mobile:  # Only include players with mobile numbers
            name_to_mobile[name] = mobile
    
    return name_to_mobile

def normalize_name_for_matching(name):
    """Normalize name for better matching."""
    # Remove extra spaces and special characters
    name = re.sub(r'\s+', ' ', name.strip())
    # Remove dots and other special characters
    name = re.sub(r'[^\w\s]', '', name)
    # Convert to lowercase for matching
    return name.lower()

def find_matching_player(filename, name_to_mobile):
    """Find the matching player for a given filename."""
    # Extract name from filename (before the first underscore with age)
    # Format: Name_Age_Category_MobileNumber.jpg
    parts = filename.replace('.jpg', '').split('_')
    
    if len(parts) < 3:
        return None
    
    # Try to match the name part
    file_name_part = parts[0]
    
    # Try exact match first
    for player_name, mobile in name_to_mobile.items():
        if file_name_part.lower() == player_name.lower():
            return mobile
    
    # Try normalized matching
    file_name_normalized = normalize_name_for_matching(file_name_part)
    for player_name, mobile in name_to_mobile.items():
        player_name_normalized = normalize_name_for_matching(player_name)
        if file_name_normalized == player_name_normalized:
            return mobile
    
    # Try partial matching for complex names
    for player_name, mobile in name_to_mobile.items():
        player_name_normalized = normalize_name_for_matching(player_name)
        if file_name_normalized in player_name_normalized or player_name_normalized in file_name_normalized:
            return mobile
    
    return None

def update_image_filenames(players_dir, name_to_mobile):
    """Update image filenames with correct mobile numbers."""
    
    print("BCL Player Image Filename Updater")
    print("=" * 50)
    print(f"Players directory: {players_dir}")
    print(f"Found {len(name_to_mobile)} players with mobile numbers")
    print()
    
    updated_count = 0
    not_found_count = 0
    errors = []
    
    # Get all image files
    image_files = [f for f in os.listdir(players_dir) if f.endswith('.jpg')]
    print(f"Found {len(image_files)} image files to process")
    print()
    
    for filename in image_files:
        try:
            # Find matching mobile number
            mobile = find_matching_player(filename, name_to_mobile)
            
            if mobile:
                # Create new filename
                parts = filename.replace('.jpg', '').split('_')
                if len(parts) >= 3:
                    # Replace the last part (mobile number) with the correct one
                    new_parts = parts[:-1] + [mobile]
                    new_filename = '_'.join(new_parts) + '.jpg'
                    
                    # Rename the file
                    old_path = os.path.join(players_dir, filename)
                    new_path = os.path.join(players_dir, new_filename)
                    
                    if old_path != new_path:
                        os.rename(old_path, new_path)
                        print(f"✓ {filename} → {new_filename}")
                        updated_count += 1
                    else:
                        print(f"- {filename} (already correct)")
                else:
                    print(f"✗ {filename} (invalid format)")
                    not_found_count += 1
            else:
                print(f"✗ {filename} (no matching player found)")
                not_found_count += 1
                
        except Exception as e:
            error_msg = f"Error processing {filename}: {str(e)}"
            print(f"✗ {error_msg}")
            errors.append(error_msg)
    
    print()
    print("=" * 50)
    print(f"Update Summary:")
    print(f"  Successfully updated: {updated_count}")
    print(f"  Not found/errors: {not_found_count}")
    print(f"  Total processed: {len(image_files)}")
    
    if errors:
        print(f"\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")
    
    return updated_count, not_found_count, errors

def main():
    # File paths
    json_file = "/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json"
    players_dir = "/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/players"
    
    # Check if files exist
    if not os.path.exists(json_file):
        print(f"Error: JSON file not found at {json_file}")
        return
    
    if not os.path.exists(players_dir):
        print(f"Error: Players directory not found at {players_dir}")
        return
    
    # Load player data
    players_data = load_player_data(json_file)
    print(f"Loaded {len(players_data)} players from JSON file")
    
    # Create name to mobile mapping
    name_to_mobile = create_name_mapping(players_data)
    print(f"Created mapping for {len(name_to_mobile)} players with mobile numbers")
    
    # Update filenames
    updated_count, not_found_count, errors = update_image_filenames(players_dir, name_to_mobile)
    
    print(f"\nUpdate complete! {updated_count} files updated successfully.")

if __name__ == "__main__":
    main()
