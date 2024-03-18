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
    3) CLASSIFIER_CONTAINER_SAS_URL - The shared access signature (SAS) Url of your Azure Blob Storage container
"""


def build_classifier():
    # [START build_classifier]
    import os
    from azure.ai.formrecognizer import (
        DocumentModelAdministrationClient,
        ClassifierDocumentTypeDetails,
        BlobSource,
        BlobFileListSource,
    )
    from azure.core.credentials import AzureKeyCredential
    from dotenv import load_dotenv

    load_dotenv()  # take environment variables from .env.


    endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
    key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]
    container_sas_url = os.environ["CONTAINER_SAS_URL"]

    document_model_admin_client = DocumentModelAdministrationClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_model_admin_client.begin_build_document_classifier(
        doc_types={
    # Commented out because of unsupported files
           "IDCards": ClassifierDocumentTypeDetails(
               source=BlobFileListSource(
                   container_url=container_sas_url, 
                   file_list="IDCards.jsonl"
               )
           ),
           "DrivingLicense": ClassifierDocumentTypeDetails(
               source=BlobFileListSource(
                   container_url=container_sas_url, 
                   file_list="DrivingLicense.jsonl"
               )
           ),
            "W9": ClassifierDocumentTypeDetails(
                source=BlobFileListSource(
                    container_url=container_sas_url, 
                    file_list="W9.jsonl"
                )
            ),
            "Email": ClassifierDocumentTypeDetails(
                        source=BlobFileListSource(
                            container_url=container_sas_url,
                            file_list="Email.jsonl"
                        )
                    ),
            "W4": ClassifierDocumentTypeDetails(
                source=BlobFileListSource(
                    container_url=container_sas_url, 
                    file_list="W4.jsonl"
                )
            ),
            "Paystubs": ClassifierDocumentTypeDetails(
                source=BlobFileListSource(
                    container_url=container_sas_url, 
                    file_list="Paystubs.jsonl"
                )
            ),
            "I9": ClassifierDocumentTypeDetails(
                source=BlobFileListSource(
                    container_url=container_sas_url, 
                    file_list="I9.jsonl"
                )
            ),
            "Resume": ClassifierDocumentTypeDetails(
                source=BlobFileListSource(
                    container_url=container_sas_url, 
                    file_list="Resume.jsonl"
                )
            ),
            "ContactCard": ClassifierDocumentTypeDetails(
                source=BlobFileListSource(
                    container_url=container_sas_url, 
                    file_list="ContactCard.jsonl"
                )
            ),
            "StickyNotes": ClassifierDocumentTypeDetails(
                source=BlobFileListSource(
                    container_url=container_sas_url, 
                    file_list="StickyNotes.jsonl"
                )
            ),
        },
        description="ADP document classifier",
    )
    result = poller.result()
    print(f"Classifier ID: {result.classifier_id}")
    print(f"API version used to build the classifier model: {result.api_version}")
    print(f"Classifier description: {result.description}")
    print(f"Document classes used for training the model:")
    for doc_type, details in result.doc_types.items():
        print(f"Document type: {doc_type}")
        print(f"Container source: {details.source.container_url}\n")
    # [END build_classifier]


if __name__ == "__main__":
    build_classifier()
