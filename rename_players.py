#!/usr/bin/env python3
"""
RENAME PLAYER FILES
Rename all player photos from player_XXX.png to Mobile-Name.png format
using data from complete_pdf_players_data.json
"""

import os
import json
import re
import glob
from pathlib import Path

def clean_name_for_filename(name):
    """Clean player name to be safe for filename."""
    # Remove special characters and replace spaces with hyphens
    cleaned = re.sub(r'[^\w\s-]', '', name)
    cleaned = re.sub(r'[-\s]+', '-', cleaned)
    return cleaned.strip('-')

def rename_player_files(players_dir, json_file):
    """Rename all player files using Mobile-Name format."""
    
    print("RENAMING PLAYER FILES")
    print("="*60)
    print(f"Players directory: {players_dir}")
    print(f"JSON data file: {json_file}")
    print("-" * 60)
    
    # Load player data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            players_data = json.load(f)
        print(f"Loaded {len(players_data)} player records")
    except Exception as e:
        print(f"❌ Error loading JSON file: {e}")
        return
    
    # Create mapping from slide number to player info
    player_map = {}
    for player in players_data:
        slide_num = player.get('slide_number')
        if slide_num:
            player_map[slide_num] = player
    
    print(f"Created mapping for {len(player_map)} players")
    print("-" * 60)
    
    # Get all player files
    player_files = sorted(glob.glob(os.path.join(players_dir, "player_*.png")))
    
    if not player_files:
        print("❌ No player files found!")
        return
    
    print(f"Found {len(player_files)} player files to rename")
    print("-" * 60)
    
    renamed_count = 0
    error_count = 0
    
    # Process each file
    for i, old_path in enumerate(player_files, 1):
        filename = os.path.basename(old_path)
        
        # Extract page number from filename (player_XXX.png)
        match = re.match(r'player_(\d+)\.png', filename)
        if not match:
            print(f"[{i:3d}] ❌ Invalid filename format: {filename}")
            error_count += 1
            continue
        
        page_num = int(match.group(1))
        
        # Get player data
        if page_num not in player_map:
            print(f"[{i:3d}] ❌ No data found for page {page_num}: {filename}")
            error_count += 1
            continue
        
        player = player_map[page_num]
        name = player.get('name', 'Unknown')
        mobile = player.get('mobile', '0000000000')
        
        # Clean name for filename
        clean_name = clean_name_for_filename(name)
        
        # Create new filename: Mobile-Name.png
        new_filename = f"{mobile}-{clean_name}.png"
        new_path = os.path.join(players_dir, new_filename)
        
        # Check if target file already exists
        if os.path.exists(new_path):
            print(f"[{i:3d}] ⚠️  Target exists, skipping: {new_filename}")
            continue
        
        try:
            # Rename file
            os.rename(old_path, new_path)
            print(f"[{i:3d}] ✅ {filename} → {new_filename}")
            renamed_count += 1
        except Exception as e:
            print(f"[{i:3d}] ❌ Error renaming {filename}: {e}")
            error_count += 1
    
    # Final summary
    print("\n" + "="*60)
    print("RENAMING COMPLETE")
    print("="*60)
    print(f"Total files processed: {len(player_files)}")
    print(f"Successfully renamed: {renamed_count}")
    print(f"Errors: {error_count}")
    print(f"Success rate: {renamed_count/len(player_files)*100:.1f}%")
    print("="*60)
    
    if error_count > 0:
        print(f"⚠️  {error_count} files had errors. Check the output above for details.")
    else:
        print("🎉 All files renamed successfully!")

def main():
    """Main function for renaming player files."""
    
    # Directory and file paths
    players_dir = "src/assets/players"
    json_file = "src/data/complete_pdf_players_data.json"
    
    # Check if players directory exists
    if not os.path.exists(players_dir):
        print(f"❌ Players directory not found: {players_dir}")
        return
    
    # Check if JSON file exists
    if not os.path.exists(json_file):
        print(f"❌ JSON data file not found: {json_file}")
        return
    
    # Rename player files
    rename_player_files(players_dir, json_file)

if __name__ == "__main__":
    main()
