import os
import sys
import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans

# Check if the correct number of command line arguments are passed
if len(sys.argv) != 3:
    print("Usage: python3 bmi_kmeans.py <n_clusters> <p_norm>")
    sys.exit(1)

# Read clustering number and p-norm from command line arguments
n_clusters = int(sys.argv[1])
p_norm = float(sys.argv[2])

# Define file path and sample ratios
base_path = "/home/username/data"  # Update to your correct file path
sample_ratios = ["0.001", "0.005", "0.01", "0.02", "0.05", "0.1", "0.3", "0.5"]

# Store the matching results for each ratio
results = {}

# Iterate over each ratio
for ratio in sample_ratios:
    # Read target and auxiliary datasets
    target_file_path = os.path.join(base_path, f'remaining_frequency_BMI_{ratio}.txt')  # Change the filename
    auxiliary_file_path = os.path.join(base_path, f'frequency_BMI_{ratio}.txt')
    
    # Read the files
    file1 = pd.read_csv(target_file_path, header=None, names=["bmi", "freq"])
    file2 = pd.read_csv(auxiliary_file_path, header=None, names=["bmi", "freq"])

    # Sort the target file by frequency in descending order
    file1 = file1.sort_values(by='freq', ascending=False)

    # Apply K-means clustering to group auxiliary file frequency values
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(file2[['freq']])
    file2['cluster'] = kmeans.labels_

    # Print members of each cluster
    print(f"Processing ratio {ratio}:")
    for cluster in range(kmeans.n_clusters):
        cluster_members = file2[file2['cluster'] == cluster]
        print(f"Cluster {cluster} members:")
        print(cluster_members)
        print("\n")

    # Extend the auxiliary file to match the target file's row count
    additional_rows = len(file1) - len(file2)
    if additional_rows > 0:
        additional_data = pd.DataFrame({'bmi': [0] * additional_rows, 'freq': [0] * additional_rows, 'cluster': [None] * additional_rows})
        file2_extended = pd.concat([file2, additional_data], ignore_index=True)
    else:
        file2_extended = file2.copy()

    # Calculate the cost matrix using p-norm
    cost_matrix = np.power(np.abs(file1['freq'].values[:, None] - file2_extended['freq'].values), p_norm)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Output the minimal distance and corresponding BMI arrangement
    matched_bmi_1 = file1['bmi'].iloc[row_ind].values
    matched_bmi_2 = file2_extended['bmi'].iloc[col_ind].values
    matched_distance = cost_matrix[row_ind, col_ind].sum()

    # Check the correctness of the matches based on file2's clustering results
    matched_cluster_2 = file2_extended['cluster'].iloc[col_ind]
    # Find the clusters for frequencies in file1
    file1_clusters = kmeans.predict(file1.iloc[row_ind][['freq']])
    matched_count = np.sum(file1_clusters == matched_cluster_2)

    # Calculate total matches and accuracy
    total_matches = len(file2)
    correct_rate = matched_count / total_matches

    print(f"{ratio} Matched target dataset BMI:", matched_bmi_1)
    print(f"{ratio} Matched auxiliary dataset BMI:", matched_bmi_2)
    print(f"{ratio} Auxiliary dataset - Minimum distance:", matched_distance)
    print(f"{ratio} Auxiliary dataset - Matched count:", matched_count)
    print(f"{ratio} Auxiliary dataset - Accuracy:", correct_rate)
    print("-" * 50)

    # Store the results
    results[ratio] = correct_rate

# Output the matching accuracy summary for all ratios
print("Matching accuracy summary for all ratios:")
for ratio, rate in results.items():
    print(f"Accuracy for {ratio} ratio: {rate:.2%}")
