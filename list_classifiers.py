from importlib.metadata import version
from azure.ai.documentintelligence import DocumentIntelligenceAdministrationClient
from azure.core.credentials import AzureKeyCredential

# SET VARIABLES
endpoint = "https://<YOUR-DOCUMENT-INTELLIGENCE-RESOURCE-NAME>.cognitiveservices.azure.com/"
key = "<YOUR-DOCUMENT-INTELLIGENCE-RESOURCE-KEY>"

def list_classifiers():
    document_model_admin_client = DocumentIntelligenceAdministrationClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    classifiers = document_model_admin_client.list_classifiers()
    print("We have the following classifiers with IDs and descriptions:")
    for page in classifiers.by_page():
        for classifier in page:
            print(f"{classifier.classifier_id} | {classifier.description}")

def print_package_versions():
    print("azure-ai-documentintelligence version: ", version("azure-ai-documentintelligence"))
    print("azure-core version: ", version("azure-core"))

if __name__ == "__main__":
    print_package_versions()
    list_classifiers()