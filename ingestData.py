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

data = ["string", "two", "three"]
attributes = [
    {"attribute1": "sdsdsads"},
    {"attribute1": "dua"},
    {"attribute1": "tiga"}
]

# data = [io.StringIO(hadith_id) for hadith_id in hadith_df['hadith_id'].astype(str).tolist()]

formatted_data = [io.StringIO(item) for item in data]
# for hadith_row in hadith_df.itertuples(index=False, name=None):
#     attribute_dict = {attribute_names[i]: hadith_row[i] for i in range(len(attribute_names))}
#     attributes.append(attribute_dict)
print(data, attributes)
# Ingest data
# vs.ingest_all_text(data, attributes, batch_size=128)

query = "materials to make cake"
top_k = 6
f = io.StringIO(query)
response = vs.lookup_text_from_str(query, top_k)
print(response)