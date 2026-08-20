# 🚨 AI Disaster Response Platform

An AWS Serverless disaster response platform built with **AWS SAM,
Lambda, API Gateway, Docker, and DynamoDB Local**.

> **Status:** Fully working locally with AWS SAM + Docker + DynamoDB
> Local.

## Features

-   Interactive map (Leaflet + OpenStreetMap)
-   Incident reporting with severity levels
-   Local AWS-style development using SAM
-   Lambda-powered REST APIs
-   DynamoDB Local integration
-   Docker-based testing without AWS deployment

## Screenshots

### Live API Mode

![Live API Dashboard](assets/live-api-dashboard.png)

### Report Incident

![Report Incident](assets/report-incident-modal.png)

## Architecture

``` text
User
 │
 ▼
Frontend (Live Server :5500)
 │
 ▼
AWS SAM Local (:3000)
 │
 ├── List Lambda
 ├── Create Lambda
 └── Get Lambda
 │
 ▼
DynamoDB Local (:8000)
```

## Project Structure

``` text
backend/
  src/
    incidents/
      create.py
      list.py
      get.py
    alerts/
    image_analysis/
frontend/
  index.html
template.yaml
```

## Local Setup

### Prerequisites

-   Python 3.12
-   Docker Desktop
-   AWS SAM CLI
-   Live Server (Cursor)

### Start DynamoDB

``` bash
docker start disaster-dynamodb
```

First-time setup:

``` bash
docker run -d --name disaster-dynamodb -p 8000:8000 amazon/dynamodb-local
```

### Build

``` bash
sam build
```

### Start Local API

``` bash
sam local start-api
```

Expected:

``` text
Running on http://127.0.0.1:3000
```

### Start Frontend

Open `frontend/index.html` using **Live Server**.

Expected status:

``` text
Mode: connected to http://127.0.0.1:3000
```

## API Endpoints

  Method   Endpoint
  -------- ------------------------------
  GET      `/incidents`
  POST     `/incidents`
  GET      `/incidents/{id}`
  POST     `/incidents/{id}/upload-url`

## AWS Services

-   AWS SAM
-   AWS Lambda
-   API Gateway
-   DynamoDB
-   Docker
-   DynamoDB Local

## Resume Highlights

-   Built a serverless disaster response platform with AWS SAM.
-   Developed Lambda-based REST APIs.
-   Integrated DynamoDB for persistent incident storage.
-   Implemented Docker-based local AWS testing.
-   Created an interactive mapping interface with Leaflet.

## Production Deployment

``` bash
sam deploy --guided
```

## Tech Stack

-   HTML
-   CSS
-   JavaScript
-   Python
-   AWS SAM
-   Docker
-   DynamoDB
-   Leaflet
