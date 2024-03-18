# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from requests import post, get
import logging, json, os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

FORM_RECOGNIZER_KEY = os.environ["AZURE_FORM_RECOGNIZER_KEY"]
ENDPOINT = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
MODEL_ID = os.environ["CLASSIFIER_ID"]
API_TYPE = "documentClassifiers"
API_VERSION = "2024-02-29-preview"
SAS_URL = os.environ["AZURE_STORAGE_CONTAINER_SAS_URL"]



def _build_classification_model() -> dict:
    """
    Using configured form recognizer key and model specifications from config,
    post the pdf to the and azure ai classification model for prediction.
    Returns the post response.
    """

    post_url = (
        ENDPOINT
        + f"/documentintelligence/{API_TYPE}:build?api-version={API_VERSION}"
    )

    params = {"includeTextDetails": True}      
        
    headers = {
        # Request headers
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": FORM_RECOGNIZER_KEY,
    }
    logger = logging.getLogger(__name__)
    body = {
    "description": "ADP document classifier",
    "classifierid": MODEL_ID,
    "docTypes": {
        "DrivingLicense": {
            "azureBlobSource": {
                "containerUrl": SAS_URL,
                "prefix": "DrivingLicense/"
            }
        },
        "W9": {
            "azureBlobSource": {
                "containerUrl": SAS_URL,
                "prefix": "W9/"
            }
        },
        "Email": {
            "azureBlobSource": {
                "containerUrl": SAS_URL,
                "prefix": "Email/"
            }
        },
        "W4": {
            "azureBlobSource": {
                "containerUrl": SAS_URL,
                "prefix": "W4/"
            }
        },
        "Paystubs": {
            "azureBlobSource": {
                "containerUrl": SAS_URL,
                "prefix": "Paystubs/"
            }
        },
        "I9": {
            "azureBlobSource": {
                "containerUrl": SAS_URL,
                "prefix": "I9/"
            }
        },
        "Resume": {
            "azureBlobSource": {
                "containerUrl": SAS_URL,
                "prefix": "Resume/"
                }
            },
        "ContactCard": {
            "azureBlobSource": {
                "containerUrl": SAS_URL,
                "prefix": "ContactCard/"
            }
        },
        "StickyNotes": {
            "azureBlobSource": {
                "containerUrl": SAS_URL,
                "prefix": "StickyNotes/"
            }
        }
    }
    }
    
    try:
        resp = post(
            url=post_url, json=body, headers=headers, params=params)
        
        if resp.status_code != 202:
            logger.warning(
                "POST build failed:\n%s" % json.dumps(resp.json())
            )
            quit()
        logger.info("POST build succeeded:\n%s" % resp.headers)
        return resp
        
    except Exception as e:
        logger.warning("POST build failed:\n%s" % str(e))    



if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    
    try:
        _build_classification_model()
        
        # [END classify_document]


    except HttpResponseError as error:
        print(
            "For more information about troubleshooting errors, see the following guide: "
            "https://aka.ms/azsdk/python/formrecognizer/troubleshooting"
        )
        
        