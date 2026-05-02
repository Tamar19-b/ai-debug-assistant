# AI Debug Assistant

AI Debug Assistant is a small full-stack web application that helps developers understand failing code faster. A developer can paste a code snippet, add the exact error message, choose the programming language, and receive:

- A clear explanation of the error
- A practical fix recommendation
- A corrected code example

The project is intentionally simple to run, but structured like a real product with a clean backend/frontend split, friendly UX, and room for future AI integration.

## Tech Stack

### Backend
- Python
- Flask
- Flask-CORS
- REST API

### Frontend
- React
- React Hooks
- Fetch API
- Plain CSS

## Project Structure

```text
AI Debug Assistant/
├── client/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── InputForm.jsx
│   │   │   └── ResultDisplay.jsx
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   └── styles.css
│   └── package.json
├── server/
│   ├── routes/
│   │   └── analyze.py
│   ├── services/
│   │   └── ai_service.py
│   ├── .env.example
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## What the Project Does

The backend exposes a single REST endpoint: `POST /analyze`.

It accepts:

```json
{
  "code": "string",
  "error": "string",
  "language": "string"
}
```

The server builds an AI-oriented prompt and returns:

```json
{
  "explanation": "string",
  "fix": "string",
  "fixed_code": "string"
}
```

If no API key is configured, the app uses a mock AI response so the full experience still works out of the box.

## Why It Is Useful

Developers often lose time jumping between stack traces, documentation, and partial fixes. This tool centralizes the first debugging pass into one focused workflow and presents the result in a readable format that supports faster iteration.

## How to Run

### 1. Start the backend

```bash
cd server
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The Flask API runs on `http://localhost:5000`.

Optional environment variables:

```env
OPENAI_API_KEY=
PORT=5000
CLIENT_ORIGIN=http://localhost:3000
```

### 2. Start the frontend

```bash
cd client
npm install
npm start
```

The React app runs on `http://localhost:5173`.

Optional frontend environment variable:

```env
VITE_API_URL=http://localhost:5000
```

## Deploy Online

The easiest way to share the project publicly is to deploy it as a single web service on Render. In this setup:

- Flask serves the API
- Vite builds the React app
- The built frontend is served by the same Flask server
- You get one public URL to share

This repository already includes a [render.yaml](</c:/Users/tamar/Downloads/לימודים/AI Debug Assistant/render.yaml>) file for that setup.

### Deploy on Render

1. Push this project to a GitHub repository.
2. Create a Render account and connect your GitHub account.
3. In Render, create a new Blueprint or Web Service from the repo.
4. Render will use:
   `buildCommand`: `pip install -r server/requirements.txt && npm --prefix client install && npm --prefix client run build`
5. Render will use:
   `startCommand`: `cd server && gunicorn app:app`
6. When the deploy finishes, Render gives you a public `onrender.com` URL that anyone can open without installing anything.

Render’s official docs say a Flask app can be deployed as a web service with a build command and a Gunicorn start command, and every service gets a public URL:

- https://render.com/docs/deploy-flask
- https://render.com/docs/web-services

### Important Note

I can prepare everything for deployment, but I cannot publish it from here unless you give me access to your hosting/GitHub account in some external way. The codebase is now ready for that path.

## API Example

### Request

```http
POST /analyze
Content-Type: application/json
```

```json
{
  "language": "Python",
  "code": "def greet_user():\nprint(name)",
  "error": "NameError: name 'name' is not defined"
}
```

### Response

```json
{
  "explanation": "In Python, this error often happens when indentation, variable names, or function usage do not match the interpreter's expectations.",
  "fix": "Define missing variables before use, keep indentation consistent, and ensure the entry-point code calls the function correctly.",
  "fixed_code": "def greet():\n    name = \"Developer\"\n    print(name)\n\n\nif __name__ == \"__main__\":\n    greet()"
}
```

## Notes for Future Improvements

- Replace the mock AI service with a real model provider call
- Add request history for repeated debugging sessions
- Support syntax highlighting for multiple languages
- Add authentication for team usage
