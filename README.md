# StaySense AI — Week 6 Authentication & Security

## Features implemented
- User registration with bcrypt password hashing (12 salt rounds).
- User login with JWT access tokens valid for 7 days.
- JWT-protected APIs and two protected frontend pages (`/dashboard`, `/analysis`).
- Logout with JWT revocation stored in SQLite.
- Input validation for authentication and review endpoints.
- Rate limiting on registration and login: 5 requests/minute per client address.
- Optional Google and GitHub OAuth using Authlib.
- CRUD review APIs plus search.

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```
Open `http://127.0.0.1:5000/register`.

## OAuth
Create OAuth applications at Google/GitHub and put their credentials in `.env`. For local development use callback URLs:
- Google: `http://127.0.0.1:5000/auth/google/callback`
- GitHub: `http://127.0.0.1:5000/auth/github/callback`

OAuth cannot be genuinely completed until provider credentials are supplied; the code and routes are ready for them.

## Protected API example
`Authorization: Bearer <access_token>`

## Postman
Import `W6_AuthAPICollection_InternID.json`. Change `baseUrl` if needed. Run Register first, then Login; the login test stores the JWT in the `jwt` collection variable.
