# StaySense AI

## Project Title 
StaySense AI — An AI-powered guest review analysis platform for understanding customer feedback.

Intern ID: TBI-26100053

## GitHub Repository
https://github.com/sanviesingh/StaySense-AI

## Features
- Guest review analysis
- Sentiment analysis
- Theme detection
- AI-assisted feedback analysis
- Authentication
- Dashboard
- CRUD functionality
- Responsive frontend

## Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Python, Flask
Database: SQLite / configured project database
AI: Configured AI API
Deployment: Vercel / Render (as applicable)

## Architecture / Folder Structure
<img width="430" height="500" alt="image" src="https://github.com/user-attachments/assets/9d82e833-8421-40c4-8a6c-0e5f784fd264" />
## Deploy on Render

1. Push this repository to GitHub.
2. In Render, choose **New > Blueprint** and select this repository.
3. Render will use `render.yaml`, install the dependencies, generate the secret keys, and start the app with Gunicorn.
4. Open the URL Render provides. The app uses same-origin API requests, so no frontend URL changes are required.

SQLite is included for simple deployment. On Render's free tier, its data is ephemeral and can reset when the service is redeployed or restarted. Use a persistent database or disk for production data.

## OAuth
Create OAuth applications at Google/GitHub and put their credentials in `.env`. For local development use callback URLs:
- Google: `http://127.0.0.1:5000/auth/google/callback`
- GitHub: `http://127.0.0.1:5000/auth/github/callback`
For hosted OAuth, set the provider callback URLs to `https://YOUR-RENDER-DOMAIN/auth/google/callback` and `https://YOUR-RENDER-DOMAIN/auth/github/callback`.

## Protected API example
`Authorization: Bearer <access_token>`

