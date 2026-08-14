# StaySense AI - Vercel Deployment Guide

## Quick Deployment Checklist

### Files Modified for Production:
- ✅ `app.py` - Added Flask-CORS support
- ✅ `requirements.txt` - Added Flask-CORS==5.0.1
- ✅ `templates/login.html` - Updated to use https://your-app-backend.herokuapp.com
- ✅ `templates/register.html` - Updated to use https://your-app-backend.herokuapp.com
- ✅ `templates/dashboard.html` - Updated to use https://your-app-backend.herokuapp.com
- ✅ `templates/analysis.html` - Updated to use https://your-app-backend.herokuapp.com

### Backend Configuration:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-app.vercel.app", "http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:3000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

## Deployment Steps

### Option A: GitHub Web Upload (Recommended)
1. Go to: https://github.com/your-username/your-repo
2. Click "Add file" → "Upload files"
3. Select modified files from your local directory
4. Commit changes with message: "Add CORS support and fix production backend URLs"
5. Vercel will automatically redeploy

### Option B: Using npm/Vercel CLI
```powershell
npm install -g vercel
vercel login
cd "c:\Users\Sanvie Singh\OneDrive\Desktop\app.py"
vercel --prod
```

### Option C: Vercel Dashboard Manual Redeploy
1. https://vercel.com/dashboard
2. Select "your-app" project
3. Deployments tab → Redeploy

## Production URLs
- **Frontend**: https://your-app.vercel.app
- **Backend**: https://your-app-backend.herokuapp.com

## Test After Deployment
1. Visit https://your-app.vercel.app
2. Go to Login page
3. Create an account
4. Login with your credentials
5. You should see the dashboard

## If Login Still Fails
- Check browser console (F12) for errors
- Verify backend is running on Heroku
- Confirm CORS headers are being sent
- Check that API URLs are correct
