import os

def process_file(filename):
    """
    Process the input file to extract and sort BMI values based on frequency.
    
    Args:
    - filename (str): Path to the input file.
    
    Returns:
    - List of sorted BMI values based on frequency (descending order).
    """
    # Read the content of the file
    with open(filename, 'r') as file:
        data = [line.strip().split(', ') for line in file]
    
    # Convert data types (BMI and frequency)
    data = [(float(bmi), float(freq)) for bmi, freq in data]
    
    # Sort data by frequency in descending order
    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
    
    # Extract and return BMI values
    bmi_values = [bmi for bmi, freq in sorted_data]
    return bmi_values

# Define the base path and sample ratios (TODO: Replace with actual path)
base_path = "TODO: Define the base path to the dataset files"
sample_ratios = ["0.001", "0.005", "0.01", "0.02", "0.05", "0.1", "0.3", "0.5"]

# Store matching results for each ratio
match_results = {}

# Process each pair of files
for ratio in sample_ratios:
    # Define file paths (TODO: Modify filenames if necessary)
    sample_file = os.path.join(base_path, f'frequency_BMI_{ratio}.txt')
    remaining_file = os.path.join(base_path, f'remaining_frequency_BMI_{ratio}.txt')
    
    try:
        # Process the sample and remaining data
        sample_data = process_file(sample_file)
        remaining_data = process_file(remaining_file)
    except FileNotFoundError:
        print(f"Error: One or both files not found for ratio {ratio}.")
        continue
    
    # Calculate the number of successful matches
    matches = sum(1 for i, j in zip(remaining_data, sample_data) if i == j)
    total_bmis = len(sample_data)
    match_percentage = matches / total_bmis * 100
    
    # Store the match results for the current ratio
    match_results[ratio] = match_percentage
    
    # Output the match results for the current ratio
    print(f"{ratio} Auxiliary dataset - Total Matches: {matches}")
    print(f"{ratio} Auxiliary dataset - Match Percentage: {match_percentage:.2f}%\n")

# Output the summary of match rates for all ratios
print("Match rate summary for all ratios:")
for ratio, percentage in match_results.items():
    print(f"Match rate for {ratio} ratio: {percentage:.2f}%")
