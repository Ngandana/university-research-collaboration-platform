# University Research Collaboration Platform — Frontend

React frontend for the University Research Collaboration Platform.
Connects to the FastAPI backend (Assignment 12).

## Pages

| Page | Route | Description |
|---|---|---|
| Login | `/login` | Sign in with email or use demo buttons |
| Dashboard | `/dashboard` | Stats overview, recent projects and tasks |
| Projects | `/projects` | List, create, complete, and delete projects |
| Tasks | `/tasks` | List, create, assign, start, and complete tasks |
| Users | `/users` | List users; admins can register, suspend, reactivate |

## Setup

### 1. Start the backend first

```bash
# In your backend project folder
uvicorn api.main:app --reload
```

Backend must be running on `http://localhost:8000`.

### 2. Install and run the frontend

```bash
cd frontend
npm install
npm start
```

Opens at `http://localhost:3000`.

### 3. First time setup

Since the backend uses in-memory storage, register users first:
1. Go to `http://localhost:8000/docs`
2. Use `POST /api/users` to create a supervisor and a student
3. Come back to the frontend and log in

Or use the **demo login buttons** on the login page to auto-login
as the first user of each role (if they exist).

## Environment

To point to a different backend URL, create a `.env` file:

```
REACT_APP_API_URL=http://your-backend-url
```

## Tech Stack

- React 18
- React Router v6
- Axios
- CSS custom properties (no UI library)
