"""
FILE: upload_documents.py

DESCRIPTION:
    This sample demonstrates how to upload labeled data to your Azure Blob Storage container and build a custom classifier model.

    More details on building a classifier and labeling your data can be found here:
    https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/documentintelligence/azure-ai-documentintelligence/samples/sample_classify_document.py

USAGE:
    python upload_documents.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_STORAGE_CONNECTION_STRING - The connection string for your Azure Storage Account
    2) AZURE_STORAGE_CONTAINER_NAME - The name of your Azure Blob Storage container
    3) TRAINING_DOCUMENTS - The local directory containing your training documents
"""
import os, json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

connect_str = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
local_directory = os.environ["TRAINING_DOCUMENTS"]
container_name = os.environ["AZURE_STORAGE_CONTAINER_NAME"]

# Create a BlobServiceClient using the connection string
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
# Create a ContainerClient for the specified container
container_client = blob_service_client.get_container_client(container_name)
# Create the container if it does not already exist
if not container_client.exists():
    print(f"Container {container_name} does not exist. Creating container...")
    container_client.create_container()
    print(f"\tContainer {container_name} created!")

def upload_documents():
# [START upload_documents]
    # Create arrays to store the incompatible files
    incompatible_files = []

    # List all files in the local directory
    for root, dirs, files in os.walk(local_directory):
        for dir in dirs:
            jsonl_data = []
            dir_path = os.path.join(root, dir)
            for file in os.listdir(dir_path):
                local_file_path = os.path.join(dir_path, file)
                ocr_json_file_path = local_file_path + ".ocr.json"
                if ( file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".heif", ".pdf", ".docx", ".xlsx", ".pptx")) 
                    and os.path.isfile(ocr_json_file_path)):
                        upload_file_to_blob(local_file_path, jsonl_data)
                        upload_file_to_blob(ocr_json_file_path)
                elif not file.endswith((".ocr.json", ".jsonl")):
                    incompatible_files.append(local_file_path)

            # Write the .jsonl file as long as there are at least 5 training files per document type
            if len(jsonl_data) >= 5:
                jsonl_file_path = os.path.join(local_directory, f"{dir}.jsonl")
                with open(jsonl_file_path, "w") as f:
                    for item in jsonl_data:
                        f.write(json.dumps(item) + "\n")
                upload_file_to_blob(jsonl_file_path)

    # Print the list of incompatible files
    if len(incompatible_files) > 0:
        print("\nThe following files are not of a supported file type, missing a corresponding .ocr.json file, or both:")
        for local_file_path in incompatible_files:
            print(f"\t{local_file_path}")
        print("Please ensure you run analyze_layout.py to create .ocr.json files before uploading documents. \nVisit the following link for more information on supported file types and sizes. \nhttps://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-custom-classifier?view=doc-intel-4.0.0#input-requirements")
    
    print("Batch upload completed!")
# [END upload_documents]
    
def upload_file_to_blob(local_file_path, jsonl_data=None):
# [START upload_file_to_blob]
    blob_name = os.path.relpath(local_file_path, local_directory).replace("\\", "/")
    if jsonl_data is not None:
        jsonl_data.append({"file": f"{blob_name}"})
    blob_client = container_client.get_blob_client(blob_name)
    # Upload the file to Azure Blob Storage
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {local_file_path} to {blob_name} in container {container_name}")
# [END upload_file_to_blob]

if __name__ == "__main__":
    upload_documents()