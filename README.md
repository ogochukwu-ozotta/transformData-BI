![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Python Version](https://img.shields.io/badge/python-3.11-blue)

# DataOps ETL Pipeline

This project automates the process of downloading, extracting, processing CSV files, and updating a MongoDB database with the extracted data. It is particularly useful for tasks involving regular data updates from external sources and provides a seamless way to ensure the most current data is available for analysis or application use.

## Description

This script is designed to automatically fetch datasets from specified URLs, extract the content from zip files, process CSV files by selecting specific columns (if necessary), and update a MongoDB database with the new data. It is ideal for continuous integration workflows, such as using GitHub Actions to periodically update a database with the latest information.

## Getting Started

### Dependencies

- Python 3.9 or higher
- Requests
- Pandas
- PyMongo
- Python-dotenv (for managing environment variables)

### Installation

Clone the repository and install the required Python packages:

```bash
git clone https://github.com/ogochukwu-ozotta/transformData-BI.git
cd the-project-name
pip install -r requirements.txt
```

### Configuration

#### MongoDB Network Access

1. Log in to MongoDB Atlas and navigate to the "Network Access" section under the "Security" tab.
2. To allow GitHub Actions to interact with the database, add `0.0.0.0/0` as an allowed IP address. This setting enables access from any IP address. For production environments, see the [Security Considerations](#security-considerations) section.

#### Environment Variables

Create a `.env` file in the root directory of your project and define the following variables:

- `MONGO_URI`: Your MongoDB connection string.
- `DB_NAME`: The name of the MongoDB database.
- `COLLECTION_NAME`: The name of the collection where data will be stored.

### Script Workflow

The main Python script (`populateData.py`) executes the following steps:

1. **Download Data**: Fetches zip files from specified URLs using the `requests` library.
2. **Extract Data**: Extracts the content of the zip files to a designated folder for each file.
3. **Process Data**: For each CSV file in the extracted folders, the script optionally filters out specific columns (configured for the `Well_Index` dataset) and converts the data into a format suitable for MongoDB insertion.
4. **Update MongoDB**: Before inserting new data, existing records in the specified collection are deleted to prevent duplication. The script then inserts the new data into the MongoDB collection.

### Running the Script

Execute the script from the command line:

```bash
python populateData.py
```

## Features

- Automated data download and extraction.
- Data filtering and processing for MongoDB compatibility.
- MongoDB database update with new, processed data.

## Security Considerations

Adding `0.0.0.0/0` to MongoDB's network access list can expose your database. For development purposes or environments without sensitive data, this might be acceptable. However, for production environments, consider:

- Using more restricted IP addresses for access.
- Implementing additional authentication and encryption measures.
- Regularly auditing access patterns and adjusting security settings accordingly.

## Contributing

We welcome contributions to this project! Please consider the following steps for contributing:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with meaningful messages.
4. Push your changes to the branch.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
