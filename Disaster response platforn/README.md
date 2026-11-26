# 🚨 AI Disaster Response Platform

An AWS Serverless disaster response platform built with **AWS SAM,
Lambda, API Gateway, Docker, and DynamoDB Local**.

> **Status:** Fully working locally with AWS SAM + Docker + DynamoDB
> Local.

## 📑 Features

-   Interactive map (Leaflet + OpenStreetMap)
-   Incident reporting with severity levels
-   Local AWS-style development using SAM
-   Lambda-powered REST APIs
-   DynamoDB Local integration
-   Docker-based testing without AWS deployment

## 📷 Screenshots

### Live API Mode

<img width="1874" height="884" alt="Screenshot 2026-08-20 010148" src="https://github.com/user-attachments/assets/1ea16e55-ce25-4c09-aea0-33e7559fe084" />


### Report Incident

<img width="1873" height="879" alt="image" src="https://github.com/user-attachments/assets/00c29e40-f8ff-4620-b66f-198113fa37fc" />


## 🛠️ Architecture

``` text
               USER
                │
                ▼
     ┌─────────────────────┐
     │ Frontend (HTML/JS)  │
     │ Live Server :5500   │
     └──────────┬──────────┘
                │ HTTP
                ▼
     ┌─────────────────────┐
     │ AWS SAM Local       │
     │ API Gateway :3000   │
     └──────────┬──────────┘
                │
      ┌─────────┴─────────┐
      ▼                   ▼
┌──────────────┐   ┌──────────────┐
│ List Lambda  │   │ Create Lambda│
└──────┬───────┘   └──────┬───────┘
       │                  │
       └────────┬─────────┘
                ▼
     ┌─────────────────────┐
     │ DynamoDB Local      │
     │ disaster-incidents  │
     └─────────────────────┘
```

## ⚙️ Project Structure

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

## 🔬 Local Setup

``` text
Browser
   │
   ▼
Live Server (:5500)
   │
   ▼
SAM Local (:3000)
   │
   ▼
Lambda Functions
   │
   ▼
DynamoDB Local (:8000)
```

### Prerequisites

-   Python 3.12
-   Docker Desktop
-   AWS SAM CLI
-   Live Server (VS code extension)

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

## 🗜️ API Endpoints

  Method   Endpoint
  -------- ------------------------------
  GET      `/incidents`
  POST     `/incidents`
  GET      `/incidents/{id}`
  POST     `/incidents/{id}/upload-url`

## 📦 AWS Services

-   AWS SAM
-   AWS Lambda
-   API Gateway
-   DynamoDB
-   Docker
-   DynamoDB Local


## 📟 Production Deployment

``` bash
sam deploy --guided
```

## 📠 Tech Stack

-   HTML
-   CSS
-   JavaScript
-   Python
-   AWS SAM
-   Docker
-   DynamoDB
-   Leaflet
