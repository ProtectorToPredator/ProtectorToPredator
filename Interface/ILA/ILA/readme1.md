1. Install Dependencies：

   - Ensure that you have Python 3 installed. You can check by running `python3 --version`.

   - Install the necessary libraries using pip3:

     ```
     pip3 install pandas numpy scipy scikit-learn
     ```

2. **Run the Script**. Open a terminal and run the script with the required parameters:

   ```bash
   python3 bmi_kmeans.py 30 2
   ```

   Replace `30` with the number of clusters (`n_clusters`) and `2` with the desired p-norm value (`p_norm`).

3. **Output**. The script will print out matching results for each sample ratio, including the BMI matched, the minimum distance, and the accuracy for each ratio.