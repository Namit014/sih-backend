# X Account Risk Detection (Frontend + Backend)

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app) that connects to a **FastAPI** backend for X account analysis.

## Getting Started

You need to run both the Backend and the Frontend servers simultaneously.

### 1. Backend Setup (FastAPI)

Open a new terminal and navigate to the backend folder:
```bash
cd backend
```

Create and activate a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

Set up Environment Variables (API Keys):
Create a file named `.env` inside the `backend` folder and add your X API and Gemini API keys:
```env
X_BEARER_TOKEN=your_x_api_bearer_token
GEMINI_API_KEY=your_gemini_api_key
```

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The backend will run on `http://127.0.0.1:8000`. You can view the API documentation at `http://127.0.0.1:8000/docs`.

---

### 2. Frontend Setup (Next.js)

Open a second terminal window and navigate to the frontend folder (where this README is located).

Install dependencies:
```bash
npm install
# or yarn install / pnpm install
```

Run the development server:
```bash
npm run dev
# or yarn dev / pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result. The frontend will automatically make requests to the FastAPI backend running on port 8000.
