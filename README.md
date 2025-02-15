# LLM Pre-Processing Pipeline

## Overview

This project is a FastAPI-based application that implements a **configurable and dynamic pre-processing pipeline** before calling an LLM API. The pipeline consists of multiple steps, such as validation, anonymization, tokenization, and token limit checks. Each step can be conditionally executed, supports error handling, and can be reordered dynamically.

## Features

- **Dynamic Pipeline Execution**: Steps can be enabled/disabled via a JSON configuration file.
- **Conditional Execution**: Each step runs based on conditions defined in the configuration.
- **Error Handling**: Steps can either halt execution or continue on failure.
- **FastAPI Integration**: Exposes an endpoint to process text before sending it to an LLM.

## Project Structure

```
llm_preprocessing_pipeline/
│── app/
│   │── main.py                # FastAPI entry point
│   │── pipeline.py            # Pre-processing pipeline logic
│   │── steps/                 # Processing steps
│   │   │── __init__.py
│   │   │── base.py            # Base class for steps
│   │   │── validation.py       # Validation step
│   │   │── anonymization.py    # Anonymization step
│   │   │── tokenization.py     # Tokenization step
│   │   │── token_limit.py      # Token limit check
│── config/
│   │── pipeline_config.json    # Pipeline configuration
│── requirements.txt            # Python dependencies
│── README.md                   # Project documentation
│── .gitignore                   # Ignore unnecessary files
```

## Installation

### **1. Clone the Repository**

```sh
git clone <your-repo-url>
cd llm_preprocessing_pipeline
```

### **2. Install Dependencies**

```sh
pip install -r requirements.txt
```

## Configuration

The pipeline is controlled via `config/pipeline_config.json`:

```json
{
  "steps": [
    {"name": "ValidationStep", "enabled": true, "on_error": "halt"},
    {"name": "AnonymizationStep", "enabled": true, "on_error": "continue", "condition": "is_valid == True"},
    {"name": "TokenizationStep", "enabled": true, "on_error": "continue", "condition": "anonymized == True"},
    {"name": "TokenLimitCheckStep", "enabled": true, "on_error": "halt", "condition": "tokenized == True", "params": {"max_tokens": 100}}
  ]
}
```

- `enabled`: Enables/disables the step.
- `on_error`: Defines whether the pipeline **halts** or **continues** on failure.
- `condition`: Executes the step **only if the condition is met**.

## Running the Application

```sh
uvicorn app.main:app --reload
```

Visit `` for the interactive API documentation.

## API Endpoint

### **POST /process**

#### **Request**

```json
{
  "query": "Hello, my name is John Doe."
}
```

#### **Response**

```json
{
  "processed_data": {
    "query": "Hello, my name is [REDACTED].",
    "is_valid": true,
    "anonymized": true,
    "tokens": ["Hello,", "my", "name", "is", "[REDACTED]."],
    "tokenized": true,
    "token_check_passed": true,
    "errors": []
  }
}
```

## Deployment

To deploy the service, push the code to GitHub and use a cloud service like **AWS Lambda, Google Cloud Run, or Azure Functions**.

```sh
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Future Enhancements

- **Logging & Monitoring**
- **Asynchronous Processing**
- **Database Support for Storing Errors**
- **UI Dashboard for Pipeline Management**

## License

This project is licensed under the MIT License.

