# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: classify_document.py

DESCRIPTION:
    This sample demonstrates how to classify a document using a trained document classifier.
    To learn how to build your custom classifier, see sample_build_classifier.py.

    More details on building a classifier and labeling your data can be found here:
    https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/documentintelligence/azure-ai-documentintelligence/samples/sample_classify_document.py

USAGE:
    python classify_document.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT - the endpoint to your Form Recognizer resource
    2) AZURE_DOCUMENT_INTELLIGENCE_KEY - your Form Recognizer API key
    3) CLASSIFIER_ID - the ID of your trained document classifier
"""

from dotenv import load_dotenv
import logging, json, os, time
from requests import post, get

load_dotenv()  # take environment variables from .env.

DOCUMENT_INTELLIGENCE_KEY = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
ENDPOINT = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
CLASSIFIER_ID = os.environ["CLASSIFIER_ID"]
API_TYPE = "documentClassifiers"
API_VERSION = "2024-02-29-preview"
TESTING_DATA = os.environ["TESTING_DOCUMENTS"]

def classify_document(classifier_id, doc_path):
    
    # [START classify_document]
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import AnalyzeResult

    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    classifier_id = os.getenv("CLASSIFIER_ID", classifier_id)

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(doc_path, "rb") as f:
        poller = document_intelligence_client.begin_classify_document(
            classifier_id, classify_request=f, content_type="application/pdf"
        )
    result: AnalyzeResult = poller.result()

    print("----Classified documents----")
    if result.documents:
        for doc in result.documents:
            if doc.bounding_regions:
                print(
                    f"Found document of type '{doc.doc_type or 'N/A'}' with a confidence of {doc.confidence} contained on "
                    f"the following pages: {[region.page_number for region in doc.bounding_regions]}"
                )
    # [END classify_document]

if __name__ == "__main__":
    import uuid
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv

    try:
        load_dotenv(find_dotenv())

        for document in os.listdir(os.environ["TESTING_DOCUMENTS"]):
            doc_path = os.path.join(os.environ["TESTING_DOCUMENTS"], document)
            print(f"Classifying document {document}...")
            request = classify_document(CLASSIFIER_ID, doc_path)

        
    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise