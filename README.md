A serverless function example built for DigitalOcean Functions that retrieves droplet information from the DigitalOcean API. This function demonstrates how to create API-connected serverless functions that can be integrated with GenAI platforms for function calling capabilities. Built using Python 3.11, it leverages the [pydo](https://pypi.org/project/pydo/) client to interact with DigitalOcean services.

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
  - [GenAI Integration Use Cases](#genai-integration-use-cases)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup \& Installation](#setup--installation)
  - [Environment Variables](#environment-variables)
  - [Python Dependencies](#python-dependencies)
- [Deployment](#deployment)
  - [Deploying to DigitalOcean Functions](#deploying-to-digitalocean-functions)
- [Sample Package](#sample-package)

---

## Introduction

The **do-api** function is a practical example of creating serverless functions on [DigitalOcean Functions](https://docs.digitalocean.com/products/functions/). It retrieves droplet information from the DigitalOcean API and is structured to be easily integrated as a function calling endpoint for GenAI platforms and Large Language Models (LLMs).

This function supports fetching details for a specific droplet by supplying a `droplet_id` or listing droplets filtered by an optional tag. The function returns key details such as droplet ID, name, status, creation time, memory, vCPUs, disk, region, image, associated public IP address, and tags in a format suitable for AI consumption.

### GenAI Integration Use Cases

This function can be used as:
- A function calling endpoint for LLMs to retrieve real-time infrastructure information
- An API connector for AI agents managing cloud resources
- A data source for AI-powered cloud management dashboards

> **Note:** The DigitalOcean API token must be provided via the `DO_API_TOKEN` environment variable.

---

## Features

- **Retrieve Specific Droplet:** Get information on a single droplet using its `droplet_id`.
- **List Droplets:** Retrieve a list of droplets with optional filtering using a `tag` and pagination via the `limit` parameter.
- **JSON Response:** Returns droplet details in a JSON formatted response.
- **Web-Enabled Function:** Configured to be deployed as a web-accessible function with an associated web secure token.

---

## Directory Structure

```
do-api/
├── project.yml                         # Project configuration file for deployment
└── packages/
    ├── do-api/
    │   └── api/
    │       ├── __main__.py             # Main API function script
    │       ├── build.sh                # Build script for dependency installation
    │       └── requirements.txt        # Python dependencies (pydo==0.8.0)
    └── sample/
        └── hello/
            └── hello.py                # Sample function for greeting
```

- **project.yml**
  Defines package parameters, function configuration (runtime, web settings, resource limits, etc.) including the secure token for web access.

- **packages/do-api/api/__main__.py**
  Contains the API logic to connect to DigitalOcean, retrieve droplet information, and format the API response.

- **packages/do-api/api/build.sh**
  A shell script to set up a virtual environment and install required Python packages targeting the correct runtime directory.

- **packages/sample/hello/hello.py**
  A simple sample function that returns a greeting message. Useful for testing basic function deployment.

---

## Setup & Installation

### Environment Variables

Before running the API function, you need to set the `DO_API_TOKEN` environment variable with your DigitalOcean API token. For example:

```bash
export DO_API_TOKEN="your_digitalocean_api_token"
```

### Python Dependencies

The function uses Python 3.11. The required dependency is specified in `packages/do-api/api/requirements.txt`:

```
pydo==0.8.0
```

To install the dependencies in your local environment, you can use the provided build script.

---

## Deployment

The project is configured via `project.yml` for deployment on [DigitalOcean Functions](https://docs.digitalocean.com/products/functions/). Key points from the configuration include:

- **Runtime:** Python 3.11 (supported by DigitalOcean Functions)
- **Function Name:** `api`
- **Web Accessible:** Enabled with a secure token (`webSecure: your-secure-token`)
- **Resource Limits:** Memory 512 MB, Timeout 5000 ms (within DigitalOcean Functions limits)

Make sure to integrate your deployment pipeline with the `project.yml` configuration. The environment variable `DO_API_TOKEN` is injected automatically into the function runtime.

### Deploying to DigitalOcean Functions

1. Install the DigitalOcean CLI (`doctl`)
2. Configure your DigitalOcean API token
3. Deploy the function:
   ```bash
   doctl serverless deploy . --remote-build
   ```

---

## Sample Package

A sample package is provided at `packages/sample/hello/hello.py` for quick testing and to demonstrate a simple function structure. It simply returns a greeting message based on the input.

Usage example:

```python
# Example payload to test hello function
args = {"name": "Alice"}
result = main(args)
print(result)
```

---

Happy coding!