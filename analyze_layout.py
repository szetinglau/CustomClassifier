# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: analyze_layout.py

DESCRIPTION:
    This script will extract text, selection marks, and layout information from files in your TRAINING_DOCUMENTS directory.
    The results of the analysis will be saved in a .ocr.json file in the same location alongside the original files. This
    script will skip files that are not supported or are corrupted and notify the user of those specific files at the end 
    of the batch process. This script should be run before using the upload_documents.py script to upload documents to your
    azure storage container.


USAGE:
    python analyze_layout.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_FORM_RECOGNIZER_ENDPOINT - the endpoint to your Form Recognizer resource.
    2) AZURE_FORM_RECOGNIZER_KEY - your Form Recognizer API key
    3) TRAINING_DOCUMENTS - The local directory containing your training documents to be analyzed
"""

import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]
local_directory = os.environ["TRAINING_DOCUMENTS"]

def analyze_layout():
# [START analyze_layout]
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.exceptions import HttpResponseError

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Create arrays to store the incompatible files
    incompatible_files = []

    # Iterate through files in the local directory and analyze each document
    for root, dirs, files in os.walk(local_directory):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            for file in os.listdir(dir_path):
                document_file_path = os.path.join(dir_path, file)
                if not file.endswith((".json", ".jsonl")):
                    print(f"Analyzing document in {document_file_path}")
                    ocr_json_file_path = document_file_path + ".ocr.json"
                    try:
                        with open(document_file_path, "rb") as f:
                            # Use begin_analyze_document to start the analysis process, and use a callback in order to recieve the raw response
                            poller = document_intelligence_client.begin_analyze_document(
                                "prebuilt-layout", analyze_request=f, content_type="application/octet-stream", cls=lambda raw_response, _, headers: create_ocr_json(ocr_json_file_path, raw_response)
                            )
                    except HttpResponseError as error:
                        print(f"Analysis of {file} failed: {error.error}\n\nSkipping to next file...")
                        incompatible_files.append(document_file_path)
                        continue 
                    result = poller.result()

    # Print the list of incompatible files
    if len(incompatible_files) > 0:
        print("\nThe following files were skipped as they are corrupted or the format is unsupported:")
        for file in incompatible_files:
            print(f"\t{file}")
        print("Please visit the following link for more information on supported file types and sizes. \nhttps://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-custom-classifier?view=doc-intel-4.0.0#input-requirements")
    
    print("Batch upload completed!")
# [END analyze_layout]

def create_ocr_json(ocr_json_file_path, raw_response):
# [START create_ocr_json]
    with open(ocr_json_file_path, "w") as f:
        f.write(raw_response.http_response.body().decode("utf-8"))
        print(f"\tOutput saved to {ocr_json_file_path}")
# [END create_ocr_json]

if __name__ == "__main__":
    analyze_layout()