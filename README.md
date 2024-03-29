# Implementing Custom Classification Model in Document Intelligence

This codebase provides an example implementation of a custom classification model in 4 steps:

- Document Preparation (_analyze_layout.py_)
- Document Upload (_upload_documents.py_)
- Build Classifier (_build_classifier.py_)
- Classify Documents (_classify_document.py_)

## Prerequisites

In order to complete this workshop, you will need to the following:

- Python 3.11 or higher (recommended using an Anaconda environment)
- Visual Studio Code
  - Python and Jupyter extensions
- Access to Azure Cognitive Services
- Access to an Azure Storage Container

## Configuration

Before running the scripts, you need to set up your environment variables. Rename the `.env.txt` to `.env` file and include the following variables:

- `AZURE_FORM_RECOGNIZER_ENDPOINT`: The endpoint to your Form Recognizer resource.
- `AZURE_FORM_RECOGNIZER_KEY`: Your Form Recognizer API key.
- `AZURE_STORAGE_CONNECTION_STRING`: The connection string to your Azure Storage service
- `AZURE_STORAGE_CONTAINER_NAME`: The name of your Azure Blob Storage container
- `TRAINING_DOCUMENTS`: The path to your training documents
- `TESTING_DOCUMENTS`: The path to your testing documents
- `CLASSIFIER_ID`: The model ID of your Form Recognizer

Please replace the placeholders with your actual values.  
<br/>
Your `TRAINING_DOCUMENTS` folder should be structured as shown below:
```
📂TRAINING_DOCUMENTS
 ┣ 📂DocumentType1
 ┃ ┣ 📜trainingFile1.ext
 ┃ ┣ 📜trainingFile2.ext
 ┃ ┣ 📜trainingFile3.ext
 ┃ ┣ 📜trainingFile4.ext
 ┃ ┣ 📜trainingFile5.ext
 ┃ ┗ 📜...
 ┣ 📂DocumentType2
 ┣ 📂...
```
> You must include **AT LEAST** 5 training files for each type of document you wish to train the model on.

## Install packages

Install the required modules
```bash
pip install -r requirements.txt
```

### analyze_layout.py

This script uses the Document Intelligence layout model to analyze your training files and create corresponding .ocr.json files.
These files are saved locally alongside your training data files and will be uploaded when running the upload_documents.py script.

```bash
python analyze_layout.py
```

### upload_documents.py

This script uploads labeled data to your Azure Blob Storage container.

```bash
python upload_documents.py
```

### build_classifier.py

This scripts demonstrates how to build a classifier model. More details on building a classifier and labeling your data can be found here: https://aka.ms/azsdk/formrecognizer/buildclassifiermodel

```bash
python build_classifier.py
```

### classify_document.py

This scripts demonstrates how to classify a folder of documents using a trained document classifier via 

```bash
python classify_document.py
```

## Resources
- Azure Form Recognizer service: https://azure.microsoft.com/en-us/services/form-recognizer/

- Documentation: https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/

- Additional examples: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/formrecognizer/azure-ai-formrecognizer/samples
