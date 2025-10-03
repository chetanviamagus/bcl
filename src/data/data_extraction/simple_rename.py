#!/usr/bin/env python3
"""
Simple script to rename player images with available information.
"""

import os
import re

def clean_filename(name, age, category):
    """Clean and format the filename according to the specified pattern."""
    # Remove special characters and spaces, replace with underscores
    clean_name = re.sub(r'[^\w\s-]', '', name).strip()
    clean_name = re.sub(r'[-\s]+', '_', clean_name)
    
    clean_category = re.sub(r'[^\w\s-]', '', category).strip()
    clean_category = re.sub(r'[-\s]+', '_', clean_category)
    
    # Format: Name_Age_Category_0000000000 (default mobile)
    filename = f"{clean_name}_{age}_{clean_category}_0000000000.jpg"
    return filename

def rename_images():
    """Rename all player images with a simple sequential approach."""
    
    players_dir = "/Users/chetan/Documents/CodeProjects/ReactProjects/bcl/src/assets/players"
    
    if not os.path.exists(players_dir):
        print(f"Error: Players directory not found at {players_dir}")
        return
    
    # Player data extracted from the PowerPoint (manually curated)
    players_data = [
        ("Manjunath_P", "42", "Batsman"),
        ("Ranjith", "25", "All_Rounder"),
        ("Vinay_G", "23", "Batsman"),
        ("Afthab", "23", "Batsman"),
        ("Shashidhar", "35", "Batsman"),
        ("Kiran", "29", "Batsman"),
        ("Vasanth_Kumar", "28", "Batsman"),
        ("Sudeep_G", "20", "All_Rounder"),
        ("Naveen_Reddy", "40", "All_Rounder"),
        ("Sandeep_Reddy", "34", "All_Rounder"),
        ("Bharath", "27", "All_Rounder"),
        ("Dishu", "32", "All_Rounder"),
        ("Sanjay_BK", "27", "All_Rounder"),
        ("Kashif", "20", "All_Rounder"),
        ("BHARATH", "26", "All_Rounder"),
        ("Indresh_Kumar", "34", "All_Rounder"),
        ("Sanjay_Kumar", "26", "Batsman"),
        ("Noorulla", "37", "Batsman"),
        ("Arun_Kumar", "26", "Batsman"),
        ("Anil", "38", "Batsman"),
        ("Narayana_swamy", "29", "Batsman"),
        ("Sanjay_Kumar_2", "26", "Batsman"),
        ("Chethan", "37", "Batsman"),
        ("Mohan_M", "22", "Batsman"),
        ("Srikanth", "24", "Batsman"),
        ("Lingraj", "20", "Batsman"),
        ("Pradeep", "42", "Batsman"),
        ("Bharath_R", "32", "All_Rounder"),
        ("Jaga", "36", "All_Rounder"),
        ("Dharshan_M", "23", "All_Rounder"),
        ("Manjunatha_BG", "32", "All_Rounder"),
        ("Anil_2", "23", "All_Rounder"),
        ("Arya", "30", "All_Rounder"),
        ("Rama_Chandra", "40", "All_Rounder"),
        ("Satyajit_Reddy", "20", "All_Rounder"),
        ("Nagavendra_M", "35", "All_Rounder"),
        ("Mithun_Reddy", "35", "All_Rounder"),
        ("Krishnamurthy", "32", "Bowler"),
        ("Manjunath_M", "44", "Bowler"),
        ("Pradeep_BG", "35", "Bowler"),
        ("Chetan_Kumar_N", "39", "Bowler"),
        ("Prakash", "32", "Batsman"),
        ("Vajresh", "36", "Batsman"),
        ("Ravindra", "40", "Batsman"),
        ("Sridhar", "29", "Batsman"),
        ("Chethan_2", "31", "Batsman"),
        ("Giri", "44", "Batsman"),
        ("Shashi_kumar", "34", "Batsman"),
        ("SUBRAMANI", "27", "Batsman"),
        ("Shashank", "21", "Batsman"),
        ("Chandrashekar", "37", "Batsman"),
        ("Shankar_M", "30", "Batsman"),
        ("Murugesh_M", "30", "Batsman"),
        ("Preyas", "12", "Batsman"),
        ("Ishthiyak", "26", "Batsman"),
        ("Umesh_BK", "37", "Batsman"),
        ("Ramesh", "38", "Batsman"),
        ("Karagappa", "43", "Batsman"),
        ("Karthik", "36", "All_Rounder"),
        ("Madhu_Prasad", "26", "Batsman"),
        ("Mahadev", "26", "Batsman"),
        ("Uday_Kumar", "37", "Batsman"),
        ("Dhruva_Kumar", "37", "Batsman"),
        ("Yeshwanth_V", "27", "Batsman"),
        ("YASH", "24", "Batsman"),
        ("Vikas", "24", "Batsman"),
        ("Tarun_Reddy", "26", "Batsman"),
        ("Vinay", "25", "Batsman"),
        ("Goutham", "23", "Batsman"),
        ("Sunil", "33", "Batsman"),
        ("Sridhar_M_2", "20", "Batsman"),
        ("Basavaraj", "23", "Batsman"),
        ("Karthik_P", "26", "Batsman"),
        ("Kiran_M", "23", "Batsman"),
        ("Chetan_N", "33", "Batsman"),
        ("Dhanush_N", "27", "Batsman"),
        ("Sachin_N", "26", "Batsman"),
        ("Yuvaraj", "25", "Batsman"),
        ("Kishore", "31", "Batsman"),
        ("Shivaraj_K", "38", "Batsman"),
        ("Ravi_Kumar_BK", "37", "Batsman"),
        ("Nandan_Chaitanya", "17", "Batsman"),
        ("VR_Kshatriya", "32", "All_Rounder"),
        ("Basavaraj_2", "18", "All_Rounder"),
        ("Kantha_Kumar", "32", "All_Rounder"),
        ("Devendra", "36", "All_Rounder"),
        ("Manjunatha_2", "31", "All_Rounder"),
        ("A_Ravindranath", "48", "All_Rounder"),
        ("Santhosh_Reddy", "39", "All_Rounder"),
        ("Roshan", "48", "All_Rounder"),
        ("Sandeep_Kumar", "31", "All_Rounder"),
        ("Shiva", "36", "All_Rounder"),
        ("Rajesh_V", "39", "All_Rounder"),
        ("Harish_M", "38", "All_Rounder"),
        ("Naveen_Kumar", "29", "All_Rounder"),
        ("Anil_Kumar_HR", "24", "All_Rounder"),
        ("Mahesh", "45", "All_Rounder"),
        ("Dhanush_B", "28", "All_Rounder"),
        ("M_Vamshi", "16", "All_Rounder"),
        ("Vishwas_R", "26", "All_Rounder"),
        ("Mithun_M", "25", "All_Rounder"),
        ("Manjunath_P_2", "35", "All_Rounder"),
        ("Mohamad_Ali", "26", "All_Rounder"),
        ("Munikrishna", "28", "All_Rounder"),
        ("Anil_Kumar_B_K", "35", "All_Rounder"),
        ("Anil_Reddy", "26", "All_Rounder"),
        ("Rajesh_R", "35", "All_Rounder"),
        ("Praveen_Kumar_N", "40", "All_Rounder"),
        ("Shiva_Kumar_N", "41", "All_Rounder"),
        ("Gopinath_V", "40", "All_Rounder"),
        ("Sharanu_V", "21", "All_Rounder"),
        ("Nikhil_Prabhakar", "28", "All_Rounder"),
        ("Ambrish", "32", "All_Rounder"),
        ("Kishan", "14", "All_Rounder"),
        ("Nithin_Kumar", "27", "All_Rounder"),
        ("Kumar", "26", "All_Rounder"),
        ("Manjunath_3", "47", "All_Rounder"),
        ("Varchas_Reddy", "22", "All_Rounder"),
        ("Aditya_M", "34", "All_Rounder"),
        ("Lavith_Reddy", "31", "Batsman"),
        ("Bhargav_K", "17", "Batsman"),
        ("Saravana", "24", "Batsman"),
        ("Vinay_Kumar_2", "27", "All_Rounder"),
        ("Sandeep_Kumar_S", "33", "All_Rounder"),
        ("Shivanand", "31", "All_Rounder"),
        ("Mithun_Murthy", "20", "All_Rounder"),
        ("Jitin_S", "20", "All_Rounder"),
        ("BC_Harish_Kumar", "40", "All_Rounder"),
        ("Sandeep_Wadhawan", "43", "All_Rounder"),
        ("Kunal_Bhargava", "38", "All_Rounder"),
        ("Kailash", "32", "All_Rounder"),
        ("Narayanaswamy", "40", "All_Rounder"),
        ("Mohan_Rao", "27", "All_Rounder"),
        ("Murugesh_S", "25", "All_Rounder"),
        ("Uday_Kiran", "25", "Batsman"),
        ("Govardhan", "22", "Batsman"),
        ("Baba_Prasad", "32", "Batsman"),
        ("Bharath_S", "29", "Batsman"),
        ("LOKESH_J", "22", "Batsman"),
        ("Azhar_Khan", "39", "Batsman"),
        ("Sachin_G", "27", "Batsman"),
        ("Dhanush_R", "20", "Batsman"),
        ("S_Manish", "20", "Batsman"),
        ("R_Prajwal", "27", "Batsman"),
        ("Sujan_Reddy_B_S", "24", "Batsman")
    ]
    
    # Get all image files
    image_files = [f for f in os.listdir(players_dir) if f.endswith('.jpg')]
    image_files.sort()  # Sort to maintain order
    
    print(f"Found {len(image_files)} image files")
    print(f"Have data for {len(players_data)} players")
    
    renamed_count = 0
    
    for i, (old_filename, player_data) in enumerate(zip(image_files, players_data)):
        if i >= len(players_data):
            break
            
        name, age, category = player_data
        new_filename = clean_filename(name, age, category)
        
        old_path = os.path.join(players_dir, old_filename)
        new_path = os.path.join(players_dir, new_filename)
        
        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {old_filename} -> {new_filename}")
            renamed_count += 1
        except Exception as e:
            print(f"Error renaming {old_filename}: {e}")
    
    print(f"\nRenaming complete! {renamed_count} images renamed successfully.")

if __name__ == "__main__":
    rename_images()
