import os
from collections import Counter
from multiprocessing import Pool, cpu_count
import re


def extract_prefix(filename):
    """
    Extract the video segment prefix, ignoring 'shaky' and similar suffixes.
    We want 'video_77_1' and 'video_77_1_shaky' to count as 'video_77_1',
    but 'video_77_1' and 'video_77_2' should be treated as separate.
    """
    # Remove 'shaky' or any other suffix after the main pattern
    clean_filename = re.sub(r'_shaky.*', '', filename)

    # Match the pattern up to the second numeric part (e.g., video_77_1, video_1_0)
    match = re.match(r'([a-zA-Z]+_\d+_\d+)', clean_filename)
    return match.group(1) if match else None


def count_prefixes(file_list):
    """Count prefixes in a list of filenames."""
    return Counter(extract_prefix(f) for f in file_list if extract_prefix(f) is not None)


def main(directory, output_file):
    # Get a list of all JSON files in the specified directory
    all_files = [f for f in os.listdir(directory) if f.endswith('.json')]

    # Split the files into chunks for multiprocessing
    num_chunks = cpu_count()  # Use the number of CPU cores
    chunk_size = len(all_files) // num_chunks
    file_chunks = [all_files[i:i + chunk_size]
                   for i in range(0, len(all_files), chunk_size)]

    # Create a multiprocessing pool
    with Pool(processes=num_chunks) as pool:
        results = pool.map(count_prefixes, file_chunks)

    # Combine the results from all processes
    total_counts = Counter()
    for result in results:
        total_counts.update(result)
    print(len(total_counts))

    # Save the frequency of each prefix to a text file
    with open(output_file, 'w') as f:
        for prefix, count in total_counts.most_common():
            f.write(f"{prefix}: {count}\n")


if __name__ == '__main__':
    # Replace with your directory path
    directory = '/Users/bocchi/Downloads/json_keypoints'
    output_file = 'prefix_frequency.txt'    # Specify the output file name
    main(directory, output_file)
