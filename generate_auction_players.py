#!/usr/bin/env python3
"""
GENERATE AUCTION PLAYERS DATA
Generate TypeScript auction players data from the extracted player JSON data.
"""

import json
import re

def clean_name_for_filename(name):
    """Clean player name to be safe for filename."""
    cleaned = re.sub(r'[^\w\s-]', '', name)
    cleaned = re.sub(r'[-\s]+', '-', cleaned)
    return cleaned.strip('-')

def generate_auction_players():
    """Generate auction players data from JSON."""
    
    # Load player data
    with open('src/data/complete_pdf_players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print(f"Loaded {len(players_data)} player records")
    
    # Generate TypeScript code
    ts_code = """// Generated auction players data from PDF extraction
import { AuctionPlayer } from '@/types'

export const auctionPlayers: AuctionPlayer[] = [
"""
    
    for i, player in enumerate(players_data):
        slide_num = player.get('slide_number', i + 1)
        name = player.get('name', 'Unknown Player')
        category = player.get('category', 'Batsman')
        age = player.get('age', '25')
        mobile = player.get('mobile', '0000000000')
        icon_player = player.get('iconPlayer', 'No')
        
        # Clean name for photo path
        clean_name = clean_name_for_filename(name)
        photo_path = f"/src/assets/players/{mobile}-{clean_name}.png"
        
        # Generate base price based on category and icon status
        base_price = 50000  # Default base price
        if icon_player == 'Yes':
            base_price = 100000  # Higher base price for icon players
        elif category == 'All Rounder':
            base_price = 75000
        elif category == 'Bowler':
            base_price = 60000
        elif category == 'Wicket Keeper':
            base_price = 70000
        
        # Generate player ID
        player_id = f"player-{slide_num:03d}"
        
        # Generate TypeScript object
        ts_code += f"""  {{
    id: '{player_id}',
    name: '{name}',
    role: '{category}',
    age: {age},
    mobile: '{mobile}',
    basePrice: {base_price},
    currentBid: {base_price},
    status: 'available' as const,
    photo: '{photo_path}',
    iconPlayer: '{icon_player}',
    soldTo: undefined,
    soldPrice: undefined,
    teamLogo: undefined
  }}{',' if i < len(players_data) - 1 else ''}
"""
    
    ts_code += """]
"""
    
    # Write to file
    with open('src/data/auctionPlayers.ts', 'w', encoding='utf-8') as f:
        f.write(ts_code)
    
    print(f"Generated auction players data for {len(players_data)} players")
    print("Saved to: src/data/auctionPlayers.ts")

if __name__ == "__main__":
    generate_auction_players()
