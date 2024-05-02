import csv
import os
import shutil

# Define the path to your CSV file and the directory containing the WAV files
csv_file_path = 'D:\\Coding_AI\\Voice-Assistant\\ESC-50\\meta\\esc50.csv'
wav_files_dir = 'D:\\Coding_AI\\Voice-Assistant\\ESC-50\\audio'

# Read the CSV file
with open(csv_file_path, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        # Extract the filename and category from the CSV row
        filename = row['filename']
        category = row['category']
        
        # Construct the full path to the WAV file
        wav_file_path = os.path.join(wav_files_dir, filename)
        
        # Construct the path to the category subfolder
        category_folder_path = os.path.join(wav_files_dir, category)
        
        # Create the category subfolder if it doesn't exist
        if not os.path.exists(category_folder_path):
            os.makedirs(category_folder_path)
        
        # Move the WAV file to the category subfolder
        shutil.move(wav_file_path, category_folder_path)
        print(f'Moved: {filename} to {category}')
