
import os
import re

# Define the directory containing the log files and the output file path
log_dir = ''
output_file_path = ''

# Define the regular expression patterns to match the phrases
patterns = {
    'vylúštenie': r'vyluští\s+(.*?)\s+vyhrává!',
    'prehodenie': r'přehodí\s+(.*?)\s+vyhrává!',
    #'opísanie': r'opíše\s+(.*?)\s+vyhrává!',
    'doplnenie': r'doplní\s+(.*?)\s+vyhrává!',
    'napísanie v správnom poradí': r'napíše ve správném sledu\s+(.*?)\s+vyhrává!',
    #'vypočítanie': r'vypočítá\s+(.*?)\s+vyhrává!',
    'prehodenie späť': r'přehodí\s+(.*?)\s+zpět vyhrává!'
}

# Function to search for phrases in a single log file
def search_in_file(file_path, patterns):
    results = {}
    try:
        # Try reading with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        try:
            # If UTF-8 fails, try reading with 'ISO-8859-1' encoding
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                content = file.read()
        except UnicodeDecodeError:
            # If other encodings fail, print an error message and skip the file
            print(f"Could not decode {file_path}. Skipping file.")
            return results

    for keyword, pattern in patterns.items():
        # Find all matches for the pattern and add them to the results
        matches = re.findall(pattern, content)
        if matches:
            results[keyword] = matches
    return results

# Search in all log files and collect the results
all_results = {}
for log_file in os.listdir(log_dir):
    if log_file.endswith('.log'):
        file_path = os.path.join(log_dir, log_file)
        results = search_in_file(file_path, patterns)
        # Combine results from this file with the overall results
        for keyword, matches in results.items():
            if keyword in all_results:
                all_results[keyword].extend(matches)
            else:
                all_results[keyword] = matches

# Write the results to the output file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for keyword, matches in all_results.items():
        for match in matches:
            output_file.write(f'{keyword}: {match}\n')

print(f'Search completed. Results are saved to {output_file_path}')
