import os
import shutil
import gzip

# Define the path to the source and destination directories
source_dir = r''
destination_dir = r''

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Python script to unzip and copy log files, excluding the 'telemetry' folder
for root, dirs, files in os.walk(source_dir):
    # Skip the telemetry folder
    if 'telemetry' in dirs:
        dirs.remove('telemetry')

    for file in files:
        # Check if the file is a .log.gz file
        if file.endswith('.log.gz'):
            # Construct the full file path
            file_path = os.path.join(root, file)
            # Construct the destination file path
            destination_file_path = os.path.join(destination_dir, file[:-3])  # remove .gz from the filename
            
            # Unzip and copy the content to the destination directory
            with gzip.open(file_path, 'rb') as f_in:
                with open(destination_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
