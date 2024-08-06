# Clinical bert webapp

## Overview

This project is a web application that integrates Optical Character Recognition (OCR) and Named Entity Recognition (NER) functionalities. It includes a FastAPI backend for handling API requests and a Streamlit frontend for user interaction.

## Folder Structure

The project directory is organized as follows:

```
mvp
│
├── backend/ # Backend directory containing FastAPI application
│ ├── app/
│ │ ├── api/
│ │ │ ├── v1/
│ │ │ │ ├── endpoints/
│ │ │ │ │ ├── ocr.py # OCR endpoint for handling image uploads and text extraction
│ │ │ │ │ └── ner.py # NER endpoint for handling clinical text and bert model
│ │ │ │ │ └── auth.py # the endpoint for handling authentication and 
│ │ │ │ │ └── translate.py # the endpoint for handling text translation
│ │ │ │ │ └── admin.py # the endpoint for handling user creation, deletion, logging...
│ │ │ └── api.py # API router setup, add all endpoint py files to this file
│ │ │ │ │ └── auth.py # the endpoint for handling authentication and
│ │ │ │ │ └── translate.py # the endpoint for handling text translation
│ │ │ └── api.py # API router setup
│ │ ├── core/
│ │ │ └── security.py # Security utilities such as password hashing
│ │ ├── models/
│ │ │ └── user.py # Database models
│ │ │ └── schemas.py # Database connection and 
│ │ │ └── database.py # Database connection and setup
│ │ ├── schemas/
│ │ │ └── user.py # Pydantic schemas for request and response validation
│ │ ├── main.py # FastAPI application entry point, here you should include all the endpoints paths
│ │
│ └── requirements.txt # Python dependencies for the backend
│
├── frontend/ # Frontend directory containing Streamlit application
│ ├── pages/
│ │ ├── home.py # Home page with functionality for uploading images and testing endpoints
│ │ ├── entity_detail.py # Page for displaying entity details (if applicable)
│ │ ├── user_profile.py # Page for user profile management (if applicable)
│ │ ├── admin.py # Page for admin functionalities (if applicable)
│ │ └── alerts.py # Page for displaying alerts (if applicable)
│ ├── app.py # Entry point for the Streamlit application, should include all pages here
│ 
├── .gitignore # Git ignore file to exclude files from version control
├── README.md # This README file
└── docker-compose.yml # Docker Compose configuration (if applicable)
└── requirements.txt # Python dependencies for the backend, run pip install
```

## Folder Details
**backend:** Contains the FastAPI application.

- `app/api/v1/endpoints/:` Holds endpoints for OCR, NER, authentication, translation, and admin functionalities.
- `app/core/security.py:` Contains security utilities like password hashing.
- `app/models/:` Includes database models and connection setup.
- `app/schemas/:` Contains Pydantic schemas for request and response validation.
- `app/main.py:` The entry point for the FastAPI application.
- `requirements.txt:` Python dependencies for the backend.
- `frontend:` Contains the Streamlit application.

pages/: Holds different pages for the Streamlit application including home, entity details, user profile, admin functionalities, and alerts.
app.py: The entry point for the Streamlit application.



1. **Install dependencies:**
Navigate to mvp directory and run: `pip install -r requirements.txt`

2. **Setup postgresql database:**
To set up the PostgreSQL database for the project, follow these steps:

* **Installation:**

   - Go to `[PostgreSQL Download Page]`(https://www.postgresql.org/download/) and download the appropriate installer for your operating system.
   - Follow the on-screen installation instructions.
   - During installation, you will be prompted to create a new admin password.
   - Leave the connection port as `5432`.

* **Create a New PostgreSQL Server:**

   - Open `pgAdmin 4.`
   - Enter the admin password you input during installation.
   - Create a new server named `action_learning_dsa3`.
   - In the Connection tab, enter the Host name/address as `localhost` and keep the port as `5432`.
   - Default username: `postgres`
   - Password: admin password specified during installation.
   - Save the settings.

* **Create a New Database:**

   - Right-click on Databases under the `clinicalbert_app` and choose Create -> Database.
   - Name the database: `clinicalbert_app`.
   - Save the settings.

* *Create Tables:*
Execute the sql script in folder `backend/models/create_tables.sql` using pgAdmin query tool.


3. To run fastapi server, navigate to backend directory and run:
`uvicorn app.main:app --reload`

4. To run streamlit server, navigate to frontend directory and run:
`streamlit run app.py`

