import os
import sys
import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score

"""
This script performs K-means clustering on frequency data and evaluates the clustering results using the Calinski-Harabasz (CH) Index.
It also matches the clustered data with a target dataset using the Hungarian algorithm and calculates the matching accuracy.
Usage:
    python bmi_kmeans.py <n_clusters> <p_norm>
Arguments:
    n_clusters (int): The number of clusters to form.
    p_norm (float): The p-norm to use for calculating the cost matrix in the Hungarian algorithm.
The script processes multiple sample ratios, reads the target and auxiliary datasets, performs K-means clustering on the auxiliary dataset,
calculates the CH Index, and matches the clustered data with the target dataset. It then calculates and prints the matching accuracy and CH Index for each sample ratio.
Variables:
    base_path (str): The base directory path where the datasets are stored.
    sample_ratios (list): A list of sample ratios to process.
    results (dict): A dictionary to store the matching accuracy for each sample ratio.
    ch_indices (dict): A dictionary to store the CH Index for each sample ratio.
Functions:
    None
Workflow:
    1. Check the number of command-line arguments.
    2. Read the number of clusters and p-norm from the command-line arguments.
    3. Iterate over each sample ratio.
    4. Read the target and auxiliary datasets for the current sample ratio.
    5. Sort the target dataset by frequency in descending order.
    6. Perform K-means clustering on the auxiliary dataset.
    7. Calculate the CH Index for the clustering result.
    8. Print the members of each cluster.
    9. Extend the auxiliary dataset to match the number of rows in the target dataset.
    10. Calculate the cost matrix using the p-norm.
    11. Use the Hungarian algorithm to find the optimal matching.
    12. Calculate and print the matching accuracy and CH Index for the current sample ratio.
    13. Store the matching accuracy and CH Index in the respective dictionaries.
    14. Print the summary of matching accuracy and CH Index for all sample ratios.
"""

# Check command-line arguments
if len(sys.argv) != 3:
    print("Usage: python bmi_kmeans.py <n_clusters> <p_norm>")
    sys.exit(1)

# Read the number of clusters and p-norm from command-line arguments
n_clusters = int(sys.argv[1])
p_norm = float(sys.argv[2])

# Define file paths and sample ratios (TODO: Replace with actual file paths)
base_path = "TODO: Define the base path to the dataset files"
sample_ratios = ["0.001", "0.005", "0.01", "0.02", "0.05", "0.1", "0.3", "0.5"]

# Dictionaries to store matching results and CH Index
results = {}
ch_indices = {}

# Iterate over each sample ratio
for ratio in sample_ratios:
    # Define file paths for target and auxiliary datasets (TODO: Modify filenames if necessary)
    target_file_path = os.path.join(base_path, f'remaining_frequency_BMI_{ratio}.txt')
    auxiliary_file_path = os.path.join(base_path, f'frequency_BMI_{ratio}.txt')

    try:
        # Read the datasets
        file1 = pd.read_csv(target_file_path, header=None, names=["bmi", "freq"])
        file2 = pd.read_csv(auxiliary_file_path, header=None, names=["bmi", "freq"])
    except FileNotFoundError:
        print(f"Error: One or both files not found for ratio {ratio}.")
        continue

    # Sort target dataset by frequency in descending order
    file1 = file1.sort_values(by='freq', ascending=False)

    # Apply K-means clustering to the auxiliary dataset based on frequency
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(file2[['freq']])
    file2['cluster'] = kmeans.labels_

    # Calculate the CH Index for the clustering result
    ch_index = calinski_harabasz_score(file2[['freq']], file2['cluster'])
    ch_indices[ratio] = ch_index

    # Print the members of each cluster
    print(f"Processing ratio {ratio}:")
    for cluster in range(kmeans.n_clusters):
        cluster_members = file2[file2['cluster'] == cluster]
        print(f"Cluster {cluster} members:")
        print(cluster_members)
        print("\n")

    # Extend the auxiliary dataset to match the target dataset row count
    additional_rows = len(file1) - len(file2)
    if additional_rows > 0:
        additional_data = pd.DataFrame({'bmi': [0] * additional_rows, 'freq': [0] * additional_rows, 'cluster': [None] * additional_rows})
        file2_extended = pd.concat([file2, additional_data], ignore_index=True)
    else:
        file2_extended = file2.copy()

    # Calculate the cost matrix using p-norm
    cost_matrix = np.power(np.abs(file1['freq'].values[:, None] - file2_extended['freq'].values), p_norm)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Output the matched BMI values and the corresponding frequencies
    matched_bmi_1 = file1['bmi'].iloc[row_ind].values
    matched_bmi_2 = file2_extended['bmi'].iloc[col_ind].values
    matched_distance = cost_matrix[row_ind, col_ind].sum()

    # Calculate the matching accuracy
    matched_count = np.sum(matched_bmi_1 == matched_bmi_2)
    total_matches = len(file2)
    match_accuracy = matched_count / total_matches * 100
    results[ratio] = match_accuracy

    # Print results for the current ratio
    print(f"{ratio} Matching results:")
    print(f"Matched BMI values in target dataset: {matched_bmi_1}")
    print(f"Matched BMI values in auxiliary dataset: {matched_bmi_2}")
    print(f"Matching distance: {matched_distance}")
    print(f"Matching accuracy: {match_accuracy:.2f}%")
    print("-" * 50)

# Output summary of matching accuracy and CH Index for all ratios
print("Matching accuracy and CH Index summary for all ratios:")
for ratio in sample_ratios:
    print(f"Ratio {ratio}: Matching accuracy = {results.get(ratio, 0):.2f}%, CH Index = {ch_indices.get(ratio, 0):.2f}")
