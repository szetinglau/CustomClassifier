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
    https://aka.ms/azsdk/formrecognizer/buildclassifiermodel

USAGE:
    python classify_document.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_FORM_RECOGNIZER_ENDPOINT - the endpoint to your Form Recognizer resource
    2) AZURE_FORM_RECOGNIZER_KEY - your Form Recognizer API key
    3) CLASSIFIER_ID - the ID of your trained document classifier
"""

from dotenv import load_dotenv
import logging, json, os, time
from requests import post, get

load_dotenv()  # take environment variables from .env.

FORM_RECOGNIZER_KEY = os.environ["AZURE_FORM_RECOGNIZER_KEY"]
ENDPOINT = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
MODEL_ID = os.environ["CLASSIFIER_ID"]
API_TYPE = "documentClassifiers"
API_VERSION = "2024-02-29-preview"


def _post_to_classification_model(path_to_sample_documents) -> dict:
    """
    Using configured form recognizer key and model specifications from config,
    post the pdf to the and azure ai classification model for prediction.
    Returns the post response.
    """

    post_url = (
        ENDPOINT
        + f"/documentintelligence/{API_TYPE}/{MODEL_ID}:analyze?api-version={API_VERSION}"
    )
    params = {"includeTextDetails": True}

    
    with open(path_to_sample_documents, "rb") as f:
        im_bytes = f.read()        
        
    headers = {
        # Request headers
        "Content-Type": "application/pdf",
        "Ocp-Apim-Subscription-Key": FORM_RECOGNIZER_KEY,
    }
    logger = logging.getLogger(__name__)

    logger.debug(f"FORM REC KEY IS: {FORM_RECOGNIZER_KEY}")
    try:
        resp = post(
            url=post_url, data=im_bytes, headers=headers, params=params)
        
        if resp.status_code != 202:
            logger.warning(
                "POST analyze failed:\n%s" % json.dumps(resp.json())
            )
            quit()
        logger.info("POST analyze succeeded:\n%s" % resp.headers)
        return resp
        #get_url = resp.headers["operation-location"]
        
    except Exception as e:
        logger.warning("POST analyze failed:\n%s" % str(e))    


def _get_classification_results(post_response: dict) -> dict:
    """
    Given our response from our post request for classification,
    retrieve the classificaiton results. Returns the get response.
    """
    logger = logging.getLogger(__name__)
    get_url = post_response.headers["operation-location"]

    n_tries = 15
    n_try = 0
    wait_sec = 5
    max_wait_sec = 60
    resp_json = None

    while n_try < n_tries:
        try:
            resp = get(
                url=get_url,
                headers={
                    "Ocp-Apim-Subscription-Key": FORM_RECOGNIZER_KEY
                },
            )
            resp_json = resp.json()
            if resp.status_code != 200:
                logger.warning(
                    "GET analyze results failed:\n%s" % json.dumps(resp_json)
                )
                break
            status = resp_json["status"]
            if status == "succeeded":
                logger.info("Analysis succeeded:\n%s" % json.dumps(resp_json))
                break
            if status == "failed":
                logger.warning("Analysis failed:\n%s" % json.dumps(resp_json))
                break
            # Analysis still running. Wait and retry.
            time.sleep(wait_sec)
            n_try += 1
            wait_sec = min(2 * wait_sec, max_wait_sec)

        except Exception as e:
            msg = "GET analyze results failed:\n%s" % str(e)
            logger.warning(msg)
            break

    return resp_json

if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    
    try:
        for document in os.listdir(os.environ["TESTING_DOCUMENTS"]):
            doc_path = os.path.join(os.environ["TESTING_DOCUMENTS"], document)
            print(f"Classifying document {document}...")
            request = _post_to_classification_model(doc_path)
            #time.sleep(5)
        
            result = _get_classification_results(request)["analyzeResult"]
            print("----Classified documents----")
            for doc in result["documents"]:
               print(
                  f"Found document of type '{doc['docType'] or 'N/A'}' with a confidence of {doc['confidence']} contained on "
                 f"the following pages: {[region['pageNumber'] for region in doc['boundingRegions']]}"
                )
        # [END classify_document]


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