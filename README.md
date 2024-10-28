# Medical Appointment Streamlining WebApp

## Overview
This web application is designed to streamline the medical appointment process. The app's main feature is the use of **speech-to-text (STT)** technology to transcribe appointments in real-time, and AI to transform those transcripts into a detailed appointment report. It also includes features for managing prescriptions, scheduling appointments, and a patient panel.

## Features
- **Speech-to-Text (STT)**: Automatically transcribe conversations during medical appointments using **Google STT**.
- **AI-Powered Reports**: Generate appointment reports based on transcriptions using AI processing.
- **Prescription Management**: Doctors can create and manage prescriptions directly through the system.
- **Scheduling System**: Integrated system for scheduling and managing appointments.
- **Patient Panel**: A dedicated patient dashboard for managing personal data, appointments, and prescriptions.

## Tech Stack

### Backend
- **FastAPI**: High-performance API framework for the backend.
- **SQLModel**: Database models using **SQLModel** for a simple yet powerful ORM solution.
- **Poetry**: Dependency management and packaging.
- **SQLite3**: Lightweight relational database used for development purposes.
- **Google Speech-to-Text**: API for real-time transcription during appointments.

### Frontend
- **React**: A modern frontend framework for building the user interface.

## Installation

### Backend Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   # CREATE VENV AND SET PYTHON INTERPRETER
   # MAKE SURE YOU ARE IN (venv) 
   # UPDATE PIP  python.exe -m pip install --upgrade pip
   
   pip install poetry

   poetry install
   poetry lock [--no-update]
   poetry install

   
   # Run the backend
   cd api
   fastapi dev main.py --reload

2. If you want to get the db to a fresh state, delete the db file and run the insert_mock_data.py
   ```bash
   rm orm.db
   python3 insert_mock_data.py
