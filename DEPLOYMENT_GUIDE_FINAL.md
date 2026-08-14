# COMPLETE DEPLOYMENT GUIDE - COPY PASTE READY

## Quick Instructions

1. **Login to GitHub** at: https://github.com/login
2. **Go to your repo**: https://github.com/sanviesingh/StaySense-AI
3. **For each file below**: Click the file → Click pencil icon → Paste content → Commit

---

## FILE 1: requirements.txt

**Location in repo**: `/requirements.txt`

**Content to paste** (copy everything below):

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

**Commit message**: `Add Flask-CORS for production support`

---

## FILE 2: app.py

**Location in repo**: `/app.py`

**Key changes** (add after line 10):
```python
from flask_cors import CORS
```

**And add after CORS setup** (around line 30):
```python
# Enable CORS for all routes
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-app.vercel.app", "http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:3000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

**Note**: If app.py already has these changes, skip this file.

**Commit message**: `Configure CORS for production`

---

## FILE 3: templates/login.html

**Location in repo**: `/templates/login.html`

**Content to paste**:

```
{% extends 'base.html' %}
{% block content %}
<section class="auth-card"><h1>Login</h1><form id="loginForm"><input id="email" type="email" placeholder="Email" required><input id="password" type="password" placeholder="Password" minlength="8" required><button class="btn" type="submit">Sign In</button></form><div id="message"></div><div class="oauth"><a class="oauth-btn" href="/auth/google">Sign in with Google</a><a class="oauth-btn" href="/auth/github">Sign in with GitHub</a></div><p>New user? <a class="dark-link" href="/register">Create an account</a></p></section>
{% endblock %}
{% block scripts %}<script>
document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = document.getElementById('message');
  const backendUrl = localStorage.getItem('backendUrl') || 'https://your-app-backend.herokuapp.com';
  const res = await fetch(`${backendUrl}/api/auth/login`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({email:email.value,password:password.value})});
  const data = await res.json();
  if(res.ok){ localStorage.setItem('access_token', data.access_token); message.textContent='Login successful!'; message.className='success'; setTimeout(()=>location.href='/dashboard',600); }
  else { message.textContent=data.error || 'Login failed'; message.className='error'; }
});
</script>{% endblock %}
```

**Commit message**: `Update login to use production backend`

---

## FILE 4: templates/register.html

**Location in repo**: `/templates/register.html`

**Content to paste**:

```
{% extends 'base.html' %}
{% block content %}
<section class="auth-card"><h1>Create Account</h1><form id="registerForm"><input id="email" type="email" placeholder="Email" required><input id="password" type="password" placeholder="Password (8+ characters)" minlength="8" required><button class="btn" type="submit">Register</button></form><div id="message"></div><p>Already registered? <a class="dark-link" href="/login">Login</a></p></section>
{% endblock %}
{% block scripts %}<script>
const backendUrl = localStorage.getItem('backendUrl') || 'https://your-app-backend.herokuapp.com';
document.getElementById('registerForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = document.getElementById('message');
  const res = await fetch(`${backendUrl}/api/auth/register`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({email:email.value,password:password.value})});
  const data = await res.json();
  message.textContent = data.message || data.error;
  message.className = res.ok ? 'success' : 'error';
  if(res.ok) setTimeout(()=>location.href='/login',800);
});
</script>{% endblock %}
```

**Commit message**: `Update register to use production backend`

---

## FILE 5: templates/dashboard.html

**Location in repo**: `/templates/dashboard.html`

**Content to paste**:

```
{% extends 'base.html' %}
{% block content %}
<section class="page protected-page"><h1>Protected Dashboard</h1><p id="userInfo">Loading account...</p><button class="btn" onclick="logout()">Logout</button><div id="reviews" class="review-list"></div></section>
{% endblock %}
{% block scripts %}<script>
const backendUrl = localStorage.getItem('backendUrl') || 'https://your-app-backend.herokuapp.com';
(async()=>{const token=localStorage.getItem('access_token');if(!token){location.href='/login';return;}const r=await fetch(`${backendUrl}/api/auth/me`,{headers:{Authorization:'Bearer '+token}});if(!r.ok){localStorage.removeItem('access_token');location.href='/login';return;}const d=await r.json();document.getElementById('userInfo').textContent='Logged in as '+d.user.email;const rr=await fetch(`${backendUrl}/api/reviews`,{headers:{Authorization:'Bearer '+token}});const rd=await rr.json();document.getElementById('reviews').innerHTML=rd.reviews.map(x=>`<article><b>${x.sentiment}</b> · ${x.theme}<p>${x.review}</p></article>`).join('')||'<p>No reviews yet.</p>';})();
async function logout(){const token=localStorage.getItem('access_token');if(token) await fetch(`${backendUrl}/api/auth/logout`,{method:'POST',headers:{Authorization:'Bearer '+token}});localStorage.removeItem('access_token');location.href='/login';}
</script>{% endblock %}
```

**Commit message**: `Update dashboard to use production backend`

---

## FILE 6: templates/analysis.html

**Location in repo**: `/templates/analysis.html`

**Content to paste**:

```
{% extends 'base.html' %}
{% block content %}
<section class="page protected-page"><h1>Review Analysis</h1><form id="reviewForm"><textarea id="review" rows="5" placeholder="Write a guest review..."></textarea><br><button class="btn" type="submit">Analyze & Save</button></form><div id="result"></div></section>
{% endblock %}
{% block scripts %}<script>
const backendUrl = localStorage.getItem('backendUrl') || 'https://your-app-backend.herokuapp.com';
(async()=>{const token=localStorage.getItem('access_token');if(!token){location.href='/login';return;}const r=await fetch(`${backendUrl}/api/auth/me`,{headers:{Authorization:'Bearer '+token}});if(!r.ok){localStorage.removeItem('access_token');location.href='/login';}})();
document.getElementById('reviewForm').addEventListener('submit',async(e)=>{e.preventDefault();const token=localStorage.getItem('access_token');const r=await fetch(`${backendUrl}/api/reviews`,{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+token},body:JSON.stringify({review:review.value})});const d=await r.json();document.getElementById('result').innerHTML=r.ok?`<div class="result"><h2>${d.review.sentiment}</h2><p>Theme: ${d.review.theme}</p></div>`:`<p class="error">${d.error}</p>`;});
</script>{% endblock %}
```

**Commit message**: `Update analysis to use production backend`

---

## Summary of Changes

✅ Added Flask-CORS==5.0.1 to handle cross-origin requests
✅ Configured CORS in app.py for production URLs
✅ Updated all frontend API calls to use production backend
✅ Login/Register now target https://your-app-backend.herokuapp.com

## After Deployment

1. Wait 1-2 minutes for Vercel to auto-deploy
2. Visit https://your-app.vercel.app
3. Test Register → Login → Dashboard flow
4. Everything should work! ✅

---

**Need help?** Each file edit is independent. You can do them one at a time.
