import pandas as pd
import os

def sample_and_save(file_path, column_name, sample_ratio, output_dir):
    """
    This function samples a specified column from a CSV file, saves the sampled data, 
    and generates frequency statistics in text files.
    
    Args:
    - file_path (str): Path to the input CSV file.
    - column_name (str): The column name to sample from the CSV file.
    - sample_ratio (float): The ratio of data to sample (e.g., 0.005 for 0.5%).
    - output_dir (str): The directory where the output files will be saved.
    
    The function performs the following tasks:
    - Samples the data based on the given ratio.
    - Saves the sampled data to a CSV file.
    - Generates frequency statistics for the sampled and remaining data.
    - Saves the frequency statistics to text files.
    """
    
    # Read the CSV file
    data = pd.read_csv(file_path)
    
    # Check if the specified column exists in the data
    if column_name not in data.columns:
        print(f"Column '{column_name}' not found in the data. Please check the column name.")
        return
    
    # Perform sampling with the given ratio (no random seed)
    sampled_data = data[[column_name]].sample(frac=sample_ratio)
    
    # Set output file paths (with sampling ratio suffix)
    sampled_csv_path = os.path.join(output_dir, f'sampled_{column_name}_{sample_ratio}.csv')
    frequency_txt_path = os.path.join(output_dir, f'frequency_{column_name}_{sample_ratio}.txt')
    remaining_frequency_txt_path = os.path.join(output_dir, f'remaining_frequency_{column_name}_{sample_ratio}.txt')
    
    # Save the sampled data to a CSV file
    sampled_data.to_csv(sampled_csv_path, index=False)
    print(f"Sampled data saved to: {sampled_csv_path}")
    
    # Compute the frequency statistics for the sampled data and convert to percentage format
    frequency = sampled_data[column_name].value_counts(normalize=True).sort_index()
    
    # Save the frequency statistics as a TXT file (in percentage format with 16 decimal places)
    with open(frequency_txt_path, 'w') as f:
        for value, freq in frequency.items():
            f.write(f"{value}, {freq * 100:.16f}\n")
    print(f"Frequency statistics for sampled data saved to: {frequency_txt_path}")
    
    # Remove the sampled data from the original dataset to get the remaining data
    remaining_data = data.drop(sampled_data.index)
    
    # Compute the frequency statistics for the remaining data and convert to percentage format
    remaining_frequency = remaining_data[column_name].value_counts(normalize=True).sort_index()
    
    # Save the frequency statistics for the remaining data as a TXT file
    with open(remaining_frequency_txt_path, 'w') as f:
        for value, freq in remaining_frequency.items():
            f.write(f"{value}, {freq * 100:.16f}\n")
    print(f"Frequency statistics for remaining data saved to: {remaining_frequency_txt_path}")

# Example usage (TODO: Replace with actual file paths and column names)
file_path = "TODO: Define the full path to the input CSV file"
output_dir = "TODO: Define the directory where the output files will be saved"
column_name = "MentHlth"  # Replace with the column you want to sample
sample_ratio = 0.005  # Replace with the desired sample ratio, e.g., 0.02 for 2%

# Call the function with the specified parameters
sample_and_save(file_path, column_name, sample_ratio, output_dir)
