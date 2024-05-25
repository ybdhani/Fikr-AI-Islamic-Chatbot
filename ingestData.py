import os
import pandas as pd
from vecto import Vecto
from pprint import pprint
from tqdm.notebook import tqdm
from dotenv import load_dotenv
import io

load_dotenv()

# Load the dataset
csv_file_path = 'path_to_your_csv_file.csv'  # Replace with the actual path to your CSV file
hadith_df = pd.read_csv("all_hadiths_clean.csv")

# Initialize Vecto
token = os.getenv("vecto_api_token")  # Replace with your Vecto API token
vector_space_id = os.getenv("vector_space_id")  # Replace with your vector space ID
print(token)
print(vector_space_id)
vs = Vecto(token, vector_space_id)

# Format data for ingestion
data = hadith_df['hadith_id'].tolist()
attribute_names = hadith_df.columns.tolist()
attributes = [{attribute_names[i]: attribute for i, attribute in enumerate(hadith_row)} for hadith_row in hadith_df.values]

# Print the first 3 elements of data and attributes
print(data[:3])
pprint(attributes[:3])

# Create the data list with the specified columns
data = hadith_df[['source', 'text_en', 'chapter_no', 'hadith_no']].values.tolist()

# Create the attribute list with all columns as dictionaries
attribute = hadith_df.to_dict(orient='records')

vs.ingest_all_text(data[:100], attribute[:100], batch_size=128)

# Print the results
print("Data List:")
print(data[:5])  # Print the first 5 records for verification

print("\nAttribute List:")
print(attribute[:5])  # Print the first 5 records for verification

# data = [io.StringIO(hadith_id) for hadith_id in hadith_df['hadith_id'].astype(str).tolist()]


