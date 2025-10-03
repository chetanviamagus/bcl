#!/usr/bin/env python3
"""
Manual update of ICON players based on user feedback
"""

import json

def manual_icon_update():
    """Update ICON players based on user corrections"""
    
    print("🎯 Manual ICON Player Update")
    print("=" * 50)
    
    # Read current player data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)
    
    print(f"📊 Current data: {len(players_data)} players")
    
    # Players that should be ICON based on user feedback
    icon_players = [
        "Manjunath.P",      # Slide 1 - confirmed
        "Ranjith",          # Slide 2 - confirmed  
        "Afthab",           # Slide 4 - confirmed
        "Sudeep G",         # Slide 8 - user mentioned
        "Naveen Reddy",     # Slide 9 - already ICON
        "Sandeep Reddy",    # Slide 10 - already ICON
        "Dishu",            # Slide 12 - already ICON
        "Indresh Kumar",    # Slide 16 - already ICON
        "Sanjay Kumar",     # Slide 18 - already ICON
        "Noorulla",         # Slide 19 - already ICON
        "Arun Kumar",       # Slide 20 - already ICON
        "Anil",             # Slide 21 - already ICON
        "Sanjay Kumar",     # Slide 23 - already ICON
        "Chethan",          # Slide 24 - already ICON
        "Srikanth",         # Slide 26 - already ICON
        "Pradeep",          # Slide 28 - already ICON
        "Bharath R",        # Slide 30 - already ICON
        "Jaga",             # Slide 31 - already ICON
        "Manjunatha BG",    # Slide 33 - already ICON
        "Arya",             # Slide 35 - already ICON
        "Rama Chandra",     # Slide 36 - already ICON
        "Satyajit Reddy",   # Slide 37 - already ICON
        "Nagavendra M",     # Slide 38 - already ICON
        "Mithun Reddy",     # Slide 39 - already ICON
        "Manjunath M",      # Slide 42 - already ICON
        "Pradeep BG",       # Slide 43 - already ICON
        "Chetan Kumar N",   # Slide 44 - already ICON
        "Prakash",          # Slide 46 - already ICON
        "Vajresh",          # Slide 47 - already ICON
        "Ravindra",         # Slide 48 - already ICON
        "Chethan",          # Slide 50 - already ICON
        "Giri",             # Slide 51 - already ICON
        "Shashi kumar",     # Slide 52 - already ICON
        "Chandrashekar",    # Slide 55 - already ICON
        "Shankar M",        # Slide 56 - already ICON
        "Murugesh .M",      # Slide 57 - already ICON
        "Umesh BK",         # Slide 60 - already ICON
        "Ramesh",           # Slide 61 - already ICON
        "Karagappa",        # Slide 62 - already ICON
        "Karthik",          # Slide 63 - already ICON
        "Madhu Prasad",     # Slide 64 - already ICON
        "Mahadev",          # Slide 65 - already ICON
        "Uday Kumar",       # Slide 66 - already ICON
        "Dhruva Kumar",     # Slide 67 - already ICON
        "Yeshwanth V",      # Slide 68 - already ICON
        "YASH",             # Slide 69 - already ICON
        "Vikas",            # Slide 70 - already ICON
        "Tarun Reddy",      # Slide 71 - already ICON
        "Vinay",            # Slide 72 - already ICON
        "Goutham",          # Slide 73 - already ICON
        "Sunil",            # Slide 74 - already ICON
        "Sridhar M",        # Slide 75 - already ICON
        "Basavaraj",        # Slide 76 - already ICON
        "Karthik P",        # Slide 77 - already ICON
        "Kiran M",          # Slide 78 - already ICON
        "Chetan N",         # Slide 79 - already ICON
        "Dhanush N",        # Slide 80 - already ICON
        "Sachin N",         # Slide 81 - already ICON
        "Yuvaraj",          # Slide 82 - already ICON
        "Kishore",          # Slide 83 - already ICON
        "Shivaraj K",       # Slide 84 - already ICON
        "Ravi Kumar BK",    # Slide 85 - already ICON
        "Nandan Chaitanya", # Slide 86 - already ICON
        "VR Kshatriya",     # Slide 88 - already ICON
        "Basavaraj",        # Slide 89 - already ICON
        "Kantha Kumar",     # Slide 90 - already ICON
        "Devendra",         # Slide 91 - already ICON
        "Manjunatha",       # Slide 92 - already ICON
        "A. Ravindranath",  # Slide 93 - already ICON
        "Santhosh Reddy",   # Slide 94 - already ICON
        "Roshan",           # Slide 95 - already ICON
        "Sandeep Kumar",    # Slide 96 - already ICON
        "Shiva",            # Slide 97 - already ICON
        "Rajesh V",         # Slide 98 - already ICON
        "Harish M",         # Slide 99 - already ICON
        "Naveen Kumar",     # Slide 100 - already ICON
        "Anil Kumar HR",    # Slide 101 - already ICON
        "Mahesh",           # Slide 102 - already ICON
        "Dhanush B",        # Slide 103 - already ICON
        "M Vamshi",         # Slide 104 - already ICON
        "Mithun M",         # Slide 106 - already ICON
        "Manjunath P",      # Slide 107 - already ICON
        "Mohamad Ali",      # Slide 108 - already ICON
        "Munikrishna",      # Slide 109 - already ICON
        "Anil Kumar B K",   # Slide 110 - already ICON
        "Anil Reddy",       # Slide 111 - already ICON
        "Rajesh R",         # Slide 112 - already ICON
        "Praveen Kumar N",  # Slide 113 - already ICON
        "Shiva Kumar N",    # Slide 114 - already ICON
        "Gopinath V",       # Slide 115 - already ICON
        "Sharanu V",        # Slide 116 - already ICON
        "Nikhil Prabhakar", # Slide 117 - already ICON
        "Ambrish",          # Slide 118 - already ICON
        "Kishan",           # Slide 119 - already ICON
        "Nithin Kumar",     # Slide 120 - already ICON
        "Kumar",            # Slide 121 - already ICON
        "Manjunath",        # Slide 122 - already ICON
        "Varchas Reddy",    # Slide 123 - already ICON
        "Aditya. M",        # Slide 124 - already ICON
        "Lavith Reddy",     # Slide 126 - already ICON
        "Bhargav. K",       # Slide 127 - already ICON
        "Saravana",         # Slide 128 - already ICON
        "Vinay Kumar",      # Slide 130 - already ICON
        "Sandeep Kumar S",  # Slide 131 - already ICON
        "Shivanand",        # Slide 132 - already ICON
        "Mithun Murthy",    # Slide 133 - already ICON
        "Jitin S",          # Slide 134 - already ICON
        "BC Harish Kumar",  # Slide 135 - already ICON
        "Sandeep Wadhawan", # Slide 136 - already ICON
        "Kunal Bhargava",   # Slide 137 - already ICON
        "Kailash",          # Slide 138 - already ICON
        "Narayanaswamy",    # Slide 139 - already ICON
        "Mohan Rao",        # Slide 140 - already ICON
        "Murugesh S",       # Slide 141 - already ICON
        "Uday Kiran",       # Slide 143 - already ICON
        "Govardhan",        # Slide 144 - already ICON
        "Baba Prasad",      # Slide 145 - already ICON
        "Bharath S",        # Slide 146 - already ICON
        "LOKESH J",         # Slide 147 - already ICON
        "Azhar Khan",       # Slide 148 - already ICON
        "Sachin G",         # Slide 149 - already ICON
        "Dhanush R",        # Slide 150 - already ICON
        "S Manish",         # Slide 151 - already ICON
        "R Prajwal",        # Slide 152 - already ICON
        "Sujan Reddy B S"   # Slide 153 - already ICON
    ]
    
    # Update players
    updated_players = []
    icon_count = 0
    
    for player in players_data:
        player_name = player.get('name', '')
        
        if player_name in icon_players:
            player['iconPlayer'] = 'Yes'
            icon_count += 1
        else:
            player['iconPlayer'] = 'No'
        
        updated_players.append(player)
    
    print(f"📊 Updated Statistics:")
    print(f"  Total players: {len(updated_players)}")
    print(f"  ICON players: {icon_count}")
    print(f"  Regular players: {len(updated_players) - icon_count}")
    
    # Show first few ICON players
    icon_players_list = [p for p in updated_players if p.get('iconPlayer') == 'Yes']
    print(f"\n🏆 ICON Players (first 20):")
    for i, player in enumerate(icon_players_list[:20]):
        print(f"  {i+1:2d}. Slide {player.get('slide_number'):3d}: {player.get('name')}")
    
    if len(icon_players_list) > 20:
        print(f"  ... and {len(icon_players_list) - 20} more")
    
    # Save updated data
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json', 'w', encoding='utf-8') as f:
        json.dump(updated_players, f, indent=2, ensure_ascii=False)
    
    # Update TypeScript file
    update_ts_file(updated_players)
    
    print(f"\n✅ Updated players_data.json and players_data.ts")
    
    return updated_players

def update_ts_file(players):
    """Update the TypeScript file with the new data"""
    ts_content = 'export interface PlayerData {\n'
    ts_content += '  slide_number: number;\n'
    ts_content += '  name: string;\n'
    ts_content += '  age: string;\n'
    ts_content += '  category: string;\n'
    ts_content += '  mobile: string;\n'
    ts_content += '  iconPlayer: string;\n'
    ts_content += '}\n\n'
    ts_content += 'export const playersData: PlayerData[] = [\n'
    
    for i, player in enumerate(players):
        ts_content += '  {\n'
        ts_content += f'    "slide_number": {player["slide_number"]},\n'
        ts_content += f'    "name": "{player["name"]}",\n'
        ts_content += f'    "age": "{player["age"]}",\n'
        ts_content += f'    "category": "{player["category"]}",\n'
        ts_content += f'    "mobile": "{player["mobile"]}",\n'
        ts_content += f'    "iconPlayer": "{player["iconPlayer"]}"\n'
        ts_content += '  }'
        if i < len(players) - 1:
            ts_content += ','
        ts_content += '\n'
    
    ts_content += '];\n'
    
    with open('/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)

if __name__ == "__main__":
    manual_icon_update()
