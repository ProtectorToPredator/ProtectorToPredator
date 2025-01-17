import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment
import sys

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 2:
    print("Usage: python bmi_lp.py <p_norm>")
    sys.exit(1)

# Read the p-norm value from the command-line arguments
p_norm = float(sys.argv[1])

# Define the sample ratios to be tested
sample_ratios = ["0.001", "0.005", "0.01", "0.02", "0.05", "0.1", "0.3", "0.5"]

# Define the base path for the dataset (TODO: Replace with actual path)
base_path = "TODO: Define the base path to the dataset files"

# Store the accuracy rates for each ratio
correct_rates = {}

# Process each ratio
for ratio in sample_ratios:
    # Read the target and auxiliary datasets (TODO: Modify filenames if needed)
    target_file_path = f"{base_path}/remaining_frequency_BMI_{ratio}.txt"
    auxiliary_file_path = f"{base_path}/frequency_BMI_{ratio}.txt"
    
    # Load the datasets into pandas DataFrames
    try:
        file1 = pd.read_csv(target_file_path, header=None, names=["bmi", "freq"])
        file2 = pd.read_csv(auxiliary_file_path, header=None, names=["bmi", "freq"])
    except FileNotFoundError:
        print(f"Error: One or both files not found for ratio {ratio}.")
        sys.exit(1)

    # Extend the auxiliary dataset to match the target dataset row count
    additional_rows = len(file1) - len(file2)
    if additional_rows > 0:
        additional_data = pd.DataFrame({"bmi": [0] * additional_rows, "freq": [0] * additional_rows})
        file2_extended = pd.concat([file2, additional_data], ignore_index=True)
    else:
        file2_extended = file2.copy()

    # Calculate the cost matrix using p-norm
    cost_matrix = np.power(np.abs(file1["freq"].values[:, None] - file2_extended["freq"].values), p_norm)
    
    # Solve the assignment problem to minimize the cost using the Hungarian algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Extract the matched BMI values and calculate the matching distance
    matched_bmi_1 = file1["bmi"].iloc[row_ind].values
    matched_bmi_2 = file2_extended["bmi"].iloc[col_ind].values
    matched_distance = cost_matrix[row_ind, col_ind].sum()

    # Count the number of matches where BMI values are identical
    matched_count = np.sum(matched_bmi_1 == matched_bmi_2)

    # Calculate the total matches and accuracy
    total_matches = len(file2)
    correct_rate = matched_count / total_matches
    correct_rates[ratio] = correct_rate  # Store the accuracy for the current ratio

    # Sort the results based on frequencies in file1 in descending order
    sorted_indices = np.argsort(-file1.iloc[row_ind]["freq"].values)
    sorted_bmi_1 = matched_bmi_1[sorted_indices]
    sorted_bmi_2 = matched_bmi_2[sorted_indices]

    # Print the results for the current ratio
    print(f"{ratio} Matched target dataset BMI:", sorted_bmi_1)
    print(f"{ratio} Matched auxiliary dataset BMI:", sorted_bmi_2)
    print(f"{ratio} Auxiliary dataset - Minimum distance:", matched_distance)
    print(f"{ratio} Auxiliary dataset - Matched count:", matched_count)
    print(f"{ratio} Auxiliary dataset - Accuracy:", correct_rate)
    print("-" * 50)

# Output the summary of matching accuracy for all ratios
print("Matching accuracy summary for all ratios:")
for ratio, rate in correct_rates.items():
    print(f"Accuracy for {ratio} ratio: {rate:.2%}")
