# StaySense AI — Week 7 AI API Integration

Intern ID: TBI-26100053

## What this adds
- POST `/api/ai/analyze`
- Secure API-key loading from `.env`
- Input validation
- Loading/error handling on the frontend
- AI-generated review analysis
- Prompt variations documented in `PROMPTS.md`

## Setup
1. Install dependencies:
   `pip install -r requirements.txt`
2. Copy `.env.example` to `.env`.
3. Put your real API key in `.env`.
4. Make sure `.env` is listed in `.gitignore`.
5. Add `ai_service.py` to the project root.
6. Add the route code to your existing Flask `app.py`.
7. Add the frontend JavaScript to your analysis page.
8. Run Flask and test `/api/ai/analyze` from the frontend/Postman.

Never commit `.env` or a real API key.
