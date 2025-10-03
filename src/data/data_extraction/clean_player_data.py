#!/usr/bin/env python3
"""
Script to clean and validate the extracted player data.
"""

import json
import re
import os

def clean_name(name):
    """Clean player name by removing extra text."""
    # Remove everything after "Category:" or similar patterns
    name = re.sub(r'\s+Category:.*$', '', name)
    name = re.sub(r'\s+Age:.*$', '', name)
    name = re.sub(r'\s+Ph:.*$', '', name)
    name = re.sub(r'\s+ICON Player.*$', '', name)
    
    # Clean up extra whitespace and special characters
    name = re.sub(r'\s+', ' ', name.strip())
    name = re.sub(r'[^\w\s\.]', '', name)  # Keep only alphanumeric, spaces, and dots
    
    return name.strip()

def clean_category(category):
    """Clean category by extracting just the role."""
    # Look for common cricket roles
    if 'Batsman' in category:
        return 'Batsman'
    elif 'Bowler' in category:
        return 'Bowler'
    elif 'All Rounder' in category or 'All-rounder' in category:
        return 'All Rounder'
    elif 'Wicket-keeper' in category or 'Wicket Keeper' in category:
        return 'Wicket Keeper'
    else:
        # Try to extract from the text
        match = re.search(r'(Batsman|Bowler|All Rounder|All-rounder|Wicket-keeper|Wicket Keeper)', category, re.IGNORECASE)
        if match:
            return match.group(1).title()
        return 'Unknown'

def clean_age(age):
    """Clean age to ensure it's a valid number."""
    # Extract just the number
    age_match = re.search(r'(\d+)', age)
    if age_match:
        age_num = int(age_match.group(1))
        # Validate age range (reasonable for cricket players)
        if 12 <= age_num <= 60:
            return str(age_num)
    return ""

def clean_mobile(mobile):
    """Clean mobile number."""
    # Extract just the digits
    mobile_digits = re.sub(r'\D', '', mobile)
    # Validate mobile number length (Indian mobile numbers are 10 digits)
    if len(mobile_digits) == 10:
        return mobile_digits
    elif len(mobile_digits) > 10:
        # Take last 10 digits if longer
        return mobile_digits[-10:]
    return ""

def clean_player_data(input_file, output_file):
    """Clean and validate player data."""
    
    print("BCL Player Data Cleaner")
    print("=" * 40)
    
    # Load the raw data
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    print(f"Loaded {len(raw_data)} raw player records")
    
    cleaned_data = []
    invalid_records = []
    
    for i, player in enumerate(raw_data):
        # Clean each field
        cleaned_player = {
            "slide_number": player.get("slide_number", i + 1),
            "name": clean_name(player.get("name", "")),
            "age": clean_age(player.get("age", "")),
            "category": clean_category(player.get("category", "")),
            "mobile": clean_mobile(player.get("mobile", ""))
        }
        
        # Validate the cleaned data
        is_valid = (
            cleaned_player["name"] and 
            cleaned_player["age"] and 
            cleaned_player["category"] != "Unknown" and
            len(cleaned_player["name"]) > 1
        )
        
        if is_valid:
            cleaned_data.append(cleaned_player)
        else:
            invalid_records.append({
                "original": player,
                "cleaned": cleaned_player,
                "issues": []
            })
            
            # Identify specific issues
            if not cleaned_player["name"]:
                invalid_records[-1]["issues"].append("Invalid name")
            if not cleaned_player["age"]:
                invalid_records[-1]["issues"].append("Invalid age")
            if cleaned_player["category"] == "Unknown":
                invalid_records[-1]["issues"].append("Unknown category")
    
    # Save cleaned data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
    
    # Save invalid records for review
    invalid_file = output_file.replace('.json', '_invalid.json')
    with open(invalid_file, 'w', encoding='utf-8') as f:
        json.dump(invalid_records, f, indent=2, ensure_ascii=False)
    
    # Generate summary
    summary_file = output_file.replace('.json', '_summary.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("BCL Player Data Cleaning Summary\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total Records Processed: {len(raw_data)}\n")
        f.write(f"Valid Records: {len(cleaned_data)}\n")
        f.write(f"Invalid Records: {len(invalid_records)}\n")
        f.write(f"Success Rate: {len(cleaned_data)/len(raw_data)*100:.1f}%\n\n")
        
        # Category breakdown
        categories = {}
        for player in cleaned_data:
            cat = player['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        f.write("Category Breakdown:\n")
        for cat, count in sorted(categories.items()):
            f.write(f"  {cat}: {count} players\n")
        
        # Age statistics
        ages = [int(p['age']) for p in cleaned_data if p['age'].isdigit()]
        if ages:
            f.write(f"\nAge Statistics:\n")
            f.write(f"  Youngest: {min(ages)} years\n")
            f.write(f"  Oldest: {max(ages)} years\n")
            f.write(f"  Average: {sum(ages)/len(ages):.1f} years\n")
        
        # Mobile numbers
        with_mobile = sum(1 for p in cleaned_data if p['mobile'])
        f.write(f"\nContact Information:\n")
        f.write(f"  Players with Mobile Numbers: {with_mobile}\n")
        f.write(f"  Players without Mobile Numbers: {len(cleaned_data) - with_mobile}\n")
        
        if invalid_records:
            f.write(f"\nInvalid Records Issues:\n")
            issue_counts = {}
            for record in invalid_records:
                for issue in record['issues']:
                    issue_counts[issue] = issue_counts.get(issue, 0) + 1
            
            for issue, count in issue_counts.items():
                f.write(f"  {issue}: {count} records\n")
    
    print(f"\nCleaning complete!")
    print(f"Valid records: {len(cleaned_data)}")
    print(f"Invalid records: {len(invalid_records)}")
    print(f"Success rate: {len(cleaned_data)/len(raw_data)*100:.1f}%")
    print(f"\nFiles created:")
    print(f"  Cleaned data: {output_file}")
    print(f"  Invalid records: {invalid_file}")
    print(f"  Summary: {summary_file}")
    
    return cleaned_data, invalid_records

def main():
    input_file = "/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data.json"
    output_file = "/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/data/players_data_clean.json"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        return
    
    cleaned_data, invalid_records = clean_player_data(input_file, output_file)
    
    # Show sample of cleaned data
    print(f"\nSample of cleaned data:")
    for i, player in enumerate(cleaned_data[:5]):
        print(f"  {i+1}. {player}")

if __name__ == "__main__":
    main()
