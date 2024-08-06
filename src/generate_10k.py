import pandas as pd

# Load the dataset
file_path = '../data/processed/medical_ner.tsv'
data = pd.read_csv(file_path, delimiter='\t')  # Adjust delimiter if needed

# Select the first 10,000 rows
subset_data = data.head(10000)

# Specify the output path
output_path = '../data/processed/small_medical_ner_first_10k.tsv'

# Save the subset data to the specified path
subset_data.to_csv(output_path, sep='\t', index=False)
