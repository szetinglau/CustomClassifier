"""
FILE: upload_documents.py

DESCRIPTION:
    This sample demonstrates how to upload labeled data to your Azure Blob Storage container and build a custom classifier model.

    More details on building a classifier and labeling your data can be found here:
    https://aka.ms/azsdk/formrecognizer/buildclassifiermodel

USAGE:
    python upload_documents.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_FORM_RECOGNIZER_ENDPOINT - the endpoint to your Form Recognizer resource.
    2) AZURE_FORM_RECOGNIZER_KEY - your Form Recognizer API key
    3) CLASSIFIER_CONTAINER_SAS_URL - The shared access signature (SAS) Url of your Azure Blob Storage container
"""
def upload_documents():
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
    import os, json

    # Define your Azure Storage connection string
    connection_string = "BlobEndpoint=https://klauml5892965663.blob.core.windows.net/;QueueEndpoint=https://klauml5892965663.queue.core.windows.net/;FileEndpoint=https://klauml5892965663.file.core.windows.net/;TableEndpoint=https://klauml5892965663.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-03-19T23:01:40Z&st=2024-03-05T16:01:40Z&spr=https&sig=SmDCD8UWC%2F7qQDwcXMAoWyvEqa1NDvXC4li4EFcJZ6A%3D"

    # Define the local directory containing your files
    local_directory = "C:\\Users\\szetinglau\\Documents\\Github\\EE_MS"

    # Define the name of the Azure Storage container
    container_name = "adp2"

    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Create a ContainerClient for the specified container
    container_client = blob_service_client.get_container_client(container_name)
    
    # List all files in the local directory
    
    for root, dirs, files in os.walk(local_directory):
        for dir in dirs:
            jsonl_data = []
            dir_path = os.path.join(root, dir)
            for file in os.listdir(dir_path):
                local_file_path = os.path.join(dir_path, file)
                blob_name = os.path.relpath(local_file_path, local_directory).replace("\\", "/")
                jsonl_data.append({"file": f"{blob_name}"})

                blob_client = container_client.get_blob_client(blob_name)
                # Upload the file to Azure Blob Storage
                with open(local_file_path, "rb") as data:
                    blob_client.upload_blob(data)

                print(f"Uploaded {local_file_path} to {blob_name} in container {container_name}")

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

    print("Batch upload completed!")
        


if __name__ == "__main__":
    upload_documents()