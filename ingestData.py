import os
import logging
import pandas as pd
from vecto import Vecto
from pprint import pprint
from tqdm.notebook import tqdm
from dotenv import load_dotenv
import io

load_dotenv()

# Load the dataset
csv_file_path = 'path_to_your_csv_file.csv'  # Replace with the actual path to your CSV file
hadith_df = pd.read_csv("clean_hadiths.csv")

# Initialize Vecto
# token = os.getenv("vecto_api_token")  # Replace with your Vecto API token
# vector_space_id = os.getenv("vector_space_id")  # Replace with your vector space ID
token = ""
vector_space_id = 
import logging

# Configure logging
logging.basicConfig(filename='new_ingestion_errors.log', level=logging.INFO)

def ingest_data_with_retry(vs, data, attribute, initial_batch_size=128, max_retries=5):
    batch_size = initial_batch_size
    start_idx = 0
    total_entries = len(data)
    
    while start_idx < total_entries:
        end_idx = min(start_idx + batch_size, total_entries)
        current_data_batch = data[start_idx:end_idx]
        current_attribute_batch = attribute[start_idx:end_idx]
        
        try:
            vs.ingest_all_text(current_data_batch, current_attribute_batch, batch_size=batch_size)
            logging.info(f'Successfully ingested entries from {start_idx} to {end_idx}')
            print(f'Successfully ingested entries from {start_idx} to {end_idx}')
            start_idx = end_idx  # Move to the next batch
            batch_size = initial_batch_size  # Reset batch size after successful ingestion
        except Exception as e:
            logging.error(f'Batch ingestion failed for entries {start_idx} to {end_idx}: {e}')
            if batch_size > 1:
                batch_size = max(1, batch_size // 2)  # Halve the batch size
            else:
                # If already at minimum batch size, log individual entries and retry
                for i in range(start_idx, end_idx):
                    try:
                        vs.ingest_all_text([data[i]], [attribute[i]], batch_size=1)
                        logging.info(f'Successfully ingested individual entry {i}')
                        print(f'Successfully ingested individual entry {i}')
                    except Exception as e:
                        logging.error(f'Individual entry ingestion failed for entry {i}: {e}')
                        print(f'Skipping faulty entry {i}')
                start_idx = end_idx  # Move to the next batch
                batch_size = initial_batch_size  # Reset batch size after skipping faulty entry


vs = Vecto(token, vector_space_id)

# Format data for ingestion
data = hadith_df['hadith_id'].tolist()
attribute_names = hadith_df.columns.tolist()
attributes = [{attribute_names[i]: attribute for i, attribute in enumerate(hadith_row)} for hadith_row in hadith_df.values]

# Print the first 3 elements of data and attributes
# print(data[:3])
# from pprint import pprint
# pprint(attributes[:3])

# Create the data list with the specified columns
data = hadith_df[['source', 'text_en', 'chapter_no', 'hadith_no']].values.tolist()

# Create the attribute list with all columns as dictionaries
attribute = hadith_df.to_dict(orient='records')

# Ingest data with retry mechanism
ingest_data_with_retry(vs, data[10001:33537], attribute[10001:33537])

# Optionally, delete all entries
# vs.delete_vector_space_entries()






