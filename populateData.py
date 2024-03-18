import os
import requests
from zipfile import ZipFile
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")  # Adjust as necessary
collection_name = os.getenv("COLLECTION_NAME")  # Adjust as necessary

# Download setup
zip_files_urls = {
    "LogTops.zip": "https://www.dmr.nd.gov/oilgas/feeservices/flatfiles/LogTops.zip",
    "LogTops_Information.zip": "https://www.dmr.nd.gov/oilgas/feeservices/flatfiles/LogTops_Information.zip",
    "Well_Index.zip": "https://www.dmr.nd.gov/oilgas/feeservices/flatfiles/Well_Index.zip"
}
auth = (os.getenv("WEB_LOGIN"), os.getenv("WEB_PASSWORD"))  # Basic Auth for downloading

# Columns to extract from Well_Index.zip CSV files
columns_to_extract = [
    "APINo", "FileNo", "CurrentOperator", "CurrentWellName", "OriginalOperator", "OriginalWellName", "SpudDate", "TD",
    "CountyName", "Township", "Range", "Section", "QQ", "Footages", "FieldName", "ProducedPools", "OilWaterGasCums",
    "IPTDateOilWaterGas", "Wellbore", "Latitude", "Longitude", "WellType", "WellStatus", "WellStatusDate"
]

def download_and_extract_zip(zip_url, auth=None):
    """Download and unzip data into a unique folder for each zip."""
    file_name = zip_url.split('/')[-1]
    folder_name = file_name.replace('.zip', '')
    os.makedirs(folder_name, exist_ok=True)  # Create a folder for the zip file

    print(f"Downloading {file_name}...")
    response = requests.get(zip_url, auth=auth)
    zip_path = os.path.join(folder_name, file_name)
    with open(zip_path, "wb") as file:
        file.write(response.content)
    
    print(f"Extracting {file_name}...")
    with ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(folder_name)

def process_csv_and_upload(folder_name, columns=None):
    """Process CSV files from a specific folder and upload data to MongoDB."""
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    for root, dirs, files in os.walk(folder_name):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")

                # Conditionally delete existing records based on folder or file criteria
                if 'Well_Index' in folder_name or 'LogTops' in folder_name:
                    print("Deleting existing records in the collection...")
                    collection.delete_many({})

                # Use columns parameter if specified, else load all columns
                if columns and 'Well_Index' in file_path:
                    data = pd.read_csv(file_path, usecols=columns)
                else:
                    data = pd.read_csv(file_path)
                records = data.to_dict("records")

                if records:
                    collection.insert_many(records)
                    print(f"Inserted {len(records)} records from {file_path}.")
                else:
                    print(f"No data to insert from {file_path}.")

if __name__ == "__main__":
    for zip_file, url in zip_files_urls.items():
        download_and_extract_zip(url, auth)
        folder_name = zip_file.replace('.zip', '')
        process_csv_and_upload(folder_name, columns_to_extract if 'Well_Index' in folder_name else None)
