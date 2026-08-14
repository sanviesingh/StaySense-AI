# GitHub Web Interface Deployment Guide

## Step-by-Step Instructions

### Prerequisites:
- You need access to your GitHub repository
- Navigate to: https://github.com/your-username/your-repo (replace with your actual repo)

---

## FILE 1: requirements.txt

1. Click on `requirements.txt` in your repo
2. Click the **pencil icon** (Edit this file)
3. **Replace everything** with this:

```
Flask==3.1.1
Flask-CORS==5.0.1
Flask-JWT-Extended==4.7.1
Flask-Limiter==3.12
bcrypt==4.3.0
python-dotenv==1.1.0
Authlib==1.6.1
email-validator==2.2.0
```

4. Scroll to bottom and click "Commit changes"
5. Enter commit message: `Add Flask-CORS for production`
6. Click "Commit"

---

## FILE 2: templates/login.html

1. Click on `templates/login.html` 
2. Click the **pencil icon**
3. **Replace everything** with the code in FILE_login.html

4. Commit with message: `Update login to use production backend URL`

---

## FILE 3: templates/register.html

1. Click on `templates/register.html`
2. Click the **pencil icon**
3. **Replace everything** with the code in FILE_register.html

4. Commit with message: `Update register to use production backend URL`

---

## FILE 4: templates/dashboard.html

1. Click on `templates/dashboard.html`
2. Click the **pencil icon**
3. **Replace everything** with the code in FILE_dashboard.html

4. Commit with message: `Update dashboard to use production backend URL`

---

## FILE 5: templates/analysis.html

1. Click on `templates/analysis.html`
2. Click the **pencil icon**
3. **Replace everything** with the code in FILE_analysis.html

4. Commit with message: `Update analysis to use production backend URL`

---

## After All Changes:

✅ Wait 1-2 minutes for Vercel to auto-deploy
✅ Go to https://your-app.vercel.app
✅ Test the login/register functionality

The app should now work on the production URL!
