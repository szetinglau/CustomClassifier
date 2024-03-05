## Configuration

Before running the scripts, you need to set up your environment variables in a `.envs.txt` file. This file should include the following variables:

- `AZURE_FORM_RECOGNIZER_ENDPOINT`: The endpoint to your Form Recognizer resource.
- `AZURE_FORM_RECOGNIZER_KEY`: Your Form Recognizer API key.
- `CLASSIFIER_CONTAINER_SAS_URL`: The shared access signature (SAS) URL of your Azure Blob Storage container.

Please replace the placeholders with your actual values.

## Running the Scripts

### upload_documents.py

This script uploads labeled data to your Azure Blob Storage container.

```bash
python upload_documents.py
```

### sample_build_classifier.py

This scripts demonstrates how to build a classifier model. More details on building a classifier and labeling your data can be found here: https://aka.ms/azsdk/formrecognizer/buildclassifiermodel

```bash
python sample_build_classifier.py
```

### sample_classify_document.py

This scripts demonstrates how to classify a document using a trained document classifier.

```bash
python sample_classify_document.py
```
