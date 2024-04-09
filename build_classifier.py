# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: build_classifier.py

DESCRIPTION:
    This sample demonstrates how to build a classifier model. For this sample, you can use the training
    documents found in https://aka.ms/azsdk/formrecognizer/sampleclassifierfiles

    More details on building a classifier and labeling your data can be found here:
    https://aka.ms/azsdk/formrecognizer/buildclassifiermodel

USAGE:
    python build_classifier.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_FORM_RECOGNIZER_ENDPOINT - the endpoint to your Form Recognizer resource.
    2) AZURE_FORM_RECOGNIZER_KEY - your Form Recognizer API key
    3) AZURE_STORAGE_CONNECTION_STRING - The connection string for your Azure Storage Account
    4) AZURE_STORAGE_CONTAINER_NAME - The name of your Azure Blob Storage container
    5) [OPTIONAL] CLASSIFIER_DESCRIPTION - A description for your trained document classifier
"""

import os
from azure.ai.documentintelligence import DocumentIntelligenceAdministrationClient
from azure.ai.documentintelligence.models import (
                AzureBlobFileListContentSource,
                ClassifierDocumentTypeDetails,
                BuildDocumentClassifierRequest,
            )
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient, ContainerSasPermissions, generate_container_sas
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import uuid
load_dotenv()  # take environment variables from .env.

def build_classifier():
# [START build_classifier]
    document_model_admin_client, container_client = create_clients()
    container_sas_url = create_container_sas_url(container_client)

    poller = document_model_admin_client.begin_build_classifier(
        BuildDocumentClassifierRequest(
            classifier_id=str(uuid.uuid4()),
            doc_types= get_doctypes(container_client, container_sas_url),
        )
        #description=os.environ["CLASSIFIER_DESCRIPTION"]
    )
    result = poller.result()
    print_classifier_results(result)
# [END build_classifier]

def create_clients():
# [START create_clients]
    endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
    key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]
    connect_str = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    container_name = os.environ["AZURE_STORAGE_CONTAINER_NAME"]

    document_model_admin_client = DocumentIntelligenceAdministrationClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
    
    return document_model_admin_client, container_client
# [END create_clients]

def get_doctypes(container_client, container_sas_url):
# [START get_doctypes]
    doc_types = {}
    doc_types_list = []

    blob_list = container_client.walk_blobs()
    for blob in blob_list:
        if blob.name.endswith(".jsonl"):
            doc_type = os.path.splitext(blob.name)[0]
            doc_types_list.append(doc_type)

    for doc_type in doc_types_list:
        doc_types[doc_type] = ClassifierDocumentTypeDetails(
            azure_blob_file_list_source=AzureBlobFileListContentSource(
                container_url=container_sas_url, 
                file_list=f"{doc_type}.jsonl"
            )
        )
    return doc_types
# [END get_doctypes]

def create_container_sas_url(container_client):
# [START create_container_sas_url]
    # Define the SAS token permissions
    sas_permissions=ContainerSasPermissions(read=True, list=True)

    # Define the expiry time and start time for the SAS token
    start_time = datetime.now(timezone.utc) - timedelta(minutes=1)
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=5)

    # Generate the container SAS token
    container_sas_token = generate_container_sas(
        container_client.account_name,
        container_client.container_name,
        account_key=container_client.credential.account_key,
        permission=sas_permissions,
        expiry=expiry_time,
        start=start_time,
    )
    # Create the container sas URL by appending the token to the container url
    container_sas_url = f"{container_client.url}?{container_sas_token}"

    return container_sas_url
# [END create_container_sas_url]

def print_classifier_results(result):
# [START print_classifier_results]
    print(f"Classifier ID: {result.classifier_id}")
    print(f"API version used to build the classifier model: {result.api_version}")
    print(f"Classifier description: {result.description}")
    print(f"Document classes used for training the model:")
    for doc_type in result.doc_types.items():
        print(f"Document type: {doc_type}")
        \
# [START print_classifier_results]
        
if __name__ == "__main__":
    build_classifier()
