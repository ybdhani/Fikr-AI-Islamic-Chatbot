import pandas as pd

# Load the dataset
csv_file_path = 'all_hadiths_clean.csv'  # Replace with the actual path to your CSV file
hadith_df = pd.read_csv(csv_file_path)

# Identify rows with null values
null_rows = hadith_df[hadith_df.isnull().any(axis=1)]

# Identify rows with empty strings
empty_string_rows = hadith_df[(hadith_df == '').any(axis=1)]

# Combine null and empty string rows
error_rows = pd.concat([null_rows, empty_string_rows]).drop_duplicates()

# Save error rows to a new CSV file
error_csv_file_path = 'hadith_errors.csv'
error_rows.to_csv(error_csv_file_path, index=False)

# Remove error rows from the original dataset
clean_hadith_df = hadith_df.drop(error_rows.index)

# Save the clean dataset to a new CSV file
clean_csv_file_path = 'clean_hadiths.csv'
clean_hadith_df.to_csv(clean_csv_file_path, index=False)

# Print a summary of the cleaning process
print(f"Total rows in original dataset: {len(hadith_df)}")
print(f"Total rows with errors: {len(error_rows)}")
print(f"Total rows in clean dataset: {len(clean_hadith_df)}")
