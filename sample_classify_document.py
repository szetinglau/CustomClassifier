# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_classify_document.py

DESCRIPTION:
    This sample demonstrates how to classify a document using a trained document classifier.
    To learn how to build your custom classifier, see sample_build_classifier.py.

    More details on building a classifier and labeling your data can be found here:
    https://aka.ms/azsdk/formrecognizer/buildclassifiermodel

USAGE:
    python sample_classify_document.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_FORM_RECOGNIZER_ENDPOINT - the endpoint to your Form Recognizer resource
    2) AZURE_FORM_RECOGNIZER_KEY - your Form Recognizer API key
    3) CLASSIFIER_ID - the ID of your trained document classifier
        -OR-
       CLASSIFIER_CONTAINER_SAS_URL - The shared access signature (SAS) Url of your Azure Blob Storage container
       with your training files. A document classifier will be built and used to run the sample.
"""

import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import ( 
        DocumentAnalysisClient,
        DocumentModelAdministrationClient,
        ClassifierDocumentTypeDetails,
        BlobSource,
        BlobFileListSource
    )
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


def classify_document():
    path_to_sample_documents = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../SampleDocs/IMG_6793.jpg"
        )
    )


    # [START classify_document]
    endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
    key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]
    classifier_id = os.environ["CLASSIFIER_ID"]

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)    
    )                                                                                                                                                                                                                                                            
    # FROM A URL FILE
    # poller = document_analysis_client.begin_analyze_document_from_url(
    #       classifier_id, "https://formrecognizer.appliedai.azure.com/documents/samples/prebuilt/w2-multiple.png"
    #  )                                                     
                                                                                                                                                                                                                                                                 
    # FROM A LOCAL FILE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                                               
    with open(path_to_sample_documents, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            classifier_id, document=f
        )             
                                                                            
    result = poller.result()

    print("----Classified documents----")
    for doc in result.documents:
        print(
            f"Found document of type '{doc.doc_type or 'N/A'}' with a confidence of {doc.confidence} contained on "
            f"the following pages: {[region.page_number for region in doc.bounding_regions]}"
        )
    # [END classify_document]


if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError

    try:
        classify_document()
    except HttpResponseError as error:
        print(
            "For more information about troubleshooting errors, see the following guide: "
            "https://aka.ms/azsdk/python/formrecognizer/troubleshooting"
        )
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