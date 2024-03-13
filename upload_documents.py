"""
FILE: upload_documents.py

DESCRIPTION:
    This sample demonstrates how to upload labeled data to your Azure Blob Storage container and build a custom classifier model.

    More details on building a classifier and labeling your data can be found here:
    https://aka.ms/azsdk/formrecognizer/buildclassifiermodel

USAGE:
    python upload_documents.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_STORAGE_CONNECTION_STRING - The connection string for your Azure Storage Account
    2) AZURE_STORAGE_CONTAINER_NAME - The name of your Azure Blob Storage container
    3) TRAINING_DOCUMENTS - The local directory containing your training documents
"""
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os, json
from dotenv import load_dotenv
from PIL import Image
load_dotenv()  # take environment variables from .env.

def upload_documents():

    # Define your Azure Storage connection string
    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]

    # Define the local directory containing your files
    local_directory = os.environ["TRAINING_DOCUMENTS"]

    # Define the name of the Azure Storage container
    container_name = os.environ["AZURE_STORAGE_CONTAINER_NAME"]

    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Create a ContainerClient for the specified container
    container_client = blob_service_client.get_container_client(container_name)
    # Create the container if it does not already exist
    if not container_client.exists():
        print(f"Container {container_name} does not exist. Creating container...")
        container_client.create_container()
        print(f"\tContainer {container_name} created!")

    # Create arrays to store the incompatible files
    incompatible_files = []

    # List all files in the local directory
    for root, dirs, files in os.walk(local_directory):
        for dir in dirs:
            jsonl_data = []
            dir_path = os.path.join(root, dir)
            for file in os.listdir(dir_path):
                local_file_path = os.path.join(dir_path, file)
                if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".heif")):
                    # Check that image files are not corrupt and are at least 50x50 pixels
                    try:
                        img = Image.open(local_file_path)
                        if img.height >= 50 and img.width >= 50:
                            upload_file_to_blob(local_file_path, local_directory, container_client, jsonl_data, container_name)
                        else:
                            incompatible_files.append(local_file_path)
                    # If the file is corrupt, add it to the list of incompatible files
                    except:
                        incompatible_files.append(local_file_path)
                # Check that the file is a supported file type
                elif file.endswith((".pdf", ".docx", ".xlsx", ".pptx")):
                    upload_file_to_blob(local_file_path, local_directory, container_client, jsonl_data, container_name)
                # If the file is not a supported file type, add it to the list of incompatible files
                else:
                    incompatible_files.append(local_file_path)

            # Write the .jsonl file
            jsonl_file_path = os.path.join(local_directory, f"{dir}.jsonl")
            with open(jsonl_file_path, "w") as f:
                for item in jsonl_data:
                    f.write(json.dumps(item) + "\n")

            # Upload the .jsonl file to Azure Blob Storage
            blob_name = os.path.relpath(jsonl_file_path, local_directory).replace("\\", "/")
            blob_client = container_client.get_blob_client(blob_name)
            with open(jsonl_file_path, "rb") as data:
                blob_client.upload_blob(data)
            print(f"Uploaded {jsonl_file_path} to {blob_name} in container {container_name}")

    # Print the list of incompatible files
    if len(incompatible_files) > 0:
        print("\nThe following files are incompatible and were not uploaded:")
        for local_file_path in incompatible_files:
            print(f"\t{local_file_path}")
        print("Please visit the following link for more information on supported file types and sizes. \nhttps://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-custom-classifier?view=doc-intel-4.0.0#input-requirements")
    
    print("Batch upload completed!")

def upload_file_to_blob(local_file_path, local_directory, container_client, jsonl_data, container_name):
    blob_name = os.path.relpath(local_file_path, local_directory).replace("\\", "/")
    jsonl_data.append({"file": f"{blob_name}"})
    blob_client = container_client.get_blob_client(blob_name)
    # Upload the file to Azure Blob Storage
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data)
    print(f"Uploaded {local_file_path} to {blob_name} in container {container_name}")

if __name__ == "__main__":
    upload_documents()