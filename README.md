# X Fake Account Detection

This project is a production-ready MVP for detecting suspicious/anomalous X (Twitter) accounts using the official X API, feature engineering, and a machine learning model. It provides an Account Risk Score and an AI-generated explanation of the behavioral signals that contributed to the score.

## Prerequisites

Before you begin, ensure you have the following installed:
*   [Python 3.9+](https://www.python.org/downloads/)
*   [Node.js 18+](https://nodejs.org/)
*   [Git](https://git-scm.com/)

## 1. Backend Setup (FastAPI)

The backend handles the X API integration, feature engineering, and ML model inference.

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    *   **Windows (PowerShell):**
        ```powershell
        python -m venv venv
        .\venv\Scripts\Activate.ps1
        ```
    *   **Mac/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *(Note: If you get a script execution policy error on Windows, temporarily bypass it by running `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` before activating).*

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**
    Create a `.env` file in the `backend` directory (you can copy `.env.example` if it exists) and add your API keys:
    ```env
    X_BEARER_TOKEN=your_x_api_bearer_token
    GEMINI_API_KEY=your_gemini_api_key
    ```
    *Note: The X API requires an appropriate access tier (Basic/Pro) to use the endpoints without hitting 402 Payment Required errors.*

5.  **Run the server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend will start at `http://127.0.0.1:8000`. You can view the interactive API documentation at `http://127.0.0.1:8000/docs`.

## 2. Frontend Setup (Next.js)

The frontend provides a sleek, modern UI to interact with the detection system.

1.  **Open a new terminal and navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The frontend will start at `http://localhost:3000`. Open this URL in your browser to use the application.

## 3. ML Model (Optional)

The machine learning model (`x_account_risk_model.pkl`) is loaded automatically by the backend. If you wish to retrain or explore the data:

1. Navigate to the `ml/notebooks` directory.
2. Open the Jupyter notebooks to view the exploratory data analysis, feature engineering, and model training pipelines.

## Common Issues

*   **`402 Payment Required` from X API:** This means the `X_BEARER_TOKEN` you provided belongs to a Free tier app that does not have access to the specific v2 endpoints used by the backend. You will need a Basic tier or higher.
*   **Next.js Hydration Mismatch:** If you see hydration errors in the browser console, it is often caused by browser extensions (like ColorZilla or Grammarly). The app is configured to suppress body mismatches, but others may still appear in development.
