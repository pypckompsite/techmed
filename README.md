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









This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

Aplikacja stworzona w Next.js, która może służyć jako baza do dalszego rozwoju projektu.

## Wymagania

- [Node.js](https://nodejs.org/) (wersja 14 lub nowsza)
- (opcjonalnie) [npm](https://www.npmjs.com/) lub [yarn](https://yarnpkg.com/) (menedżer pakietów)

## Instalacja

Sklonuj repozytorium:

    ```bash
    git clone https://github.com/twoj-profil/nazwa-repozytorium.git
    cd nazwa-repozytorium
    ```

2. Zainstaluj zależności:

   Jeśli używasz npm:

    ```bash
    npm install
    ```

   Jeśli używasz yarn:

    ```bash
    yarn install
    ```
Struktura plików w repozytorium
Poniżej lista kluczowych plików i katalogów, które warto dołączyć do repozytorium:

- pages/ - Główne widoki aplikacji Next.js
- components/ - Komponenty wielokrotnego użytku
- public/ - Zasoby statyczne (np. obrazy)
- styles/ - Pliki ze stylami aplikacji
- package.json - Lista zależności i skrypty uruchamiające aplikację
- next.config.js - Konfiguracja Next.js
- .gitignore - Lista plików i katalogów ignorowanych przez git (np. node_modules, .env.local)

Skrypty
- dev - Uruchamia aplikację w trybie deweloperskim
- build - Buduje aplikację do wdrożenia
- start - Uruchamia aplikację produkcyjną po zbudowaniu

Użycie ESLint
Projekt jest skonfigurowany z ESLint, aby zapewnić wysoką jakość kodu. Możesz uruchomić lintowanie, używając:

bash
Skopiuj kod
npm run lint
Aby automatycznie naprawić błędy, możesz użyć:

bash
Skopiuj kod
npm run lint -- --fix

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.js`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

