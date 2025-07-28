# 🚀 **HACKATHON DEPLOYMENT GUIDE**
## **Team 0verr1de - ICS Cybersecurity Dashboard**

---

## 🎯 **DEPLOYMENT OPTIONS** (All FREE!)

### **🌟 OPTION 1: VERCEL (RECOMMENDED)**
*Full-stack deployment in 5 minutes*

### **🌟 OPTION 2: NETLIFY + RAILWAY**  
*Separate frontend/backend deployment*

### **🌟 OPTION 3: RENDER**
*Single platform full-stack*

---

# 🚀 **OPTION 1: VERCEL DEPLOYMENT** ⭐

## **Step 1: Prepare Your Code**
```bash
# Ensure you're in the project directory
cd ics-dashboard/

# Create/update package.json scripts
npm install

# Build test (optional)
npm run build
```

## **Step 2: Push to GitHub**
```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Team 0verr1de - ICS Cybersecurity Dashboard with WADI integration"

# Create GitHub repo and push
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## **Step 3: Deploy to Vercel**
1. **Go to:** https://vercel.com
2. **Sign up** with GitHub account (FREE)
3. **Click:** "New Project"
4. **Import** your GitHub repository
5. **Configure:**
   - Framework Preset: `Vite`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

6. **Environment Variables** (Add these):
   ```
   PYTHON_VERSION=3.9
   ```

7. **Click "Deploy"**

## **Step 4: Configure Backend**
Vercel will automatically handle the backend using the `vercel.json` file we created.

**✅ LIVE URLS:**
- **Frontend:** `https://your-repo-name.vercel.app`
- **Backend API:** `https://your-repo-name.vercel.app/api/health`

---

# 🚀 **OPTION 2: NETLIFY + RAILWAY**

## **Frontend on Netlify**

### **Step 1: Build Frontend**
```bash
# Build the React app
npm run build

# This creates a 'dist' folder
```

### **Step 2: Deploy to Netlify**
1. **Go to:** https://netlify.com
2. **Sign up** (FREE)
3. **Drag and drop** the `dist` folder to Netlify
4. **Or connect GitHub:**
   - New site from Git → GitHub → Select repo
   - Build command: `npm run build`
   - Publish directory: `dist`

**✅ Frontend URL:** `https://your-site-name.netlify.app`

## **Backend on Railway**

### **Step 1: Prepare Backend**
```bash
# Create Procfile for Railway
echo "web: cd backend && python server.py" > Procfile
```

### **Step 2: Deploy to Railway**
1. **Go to:** https://railway.app
2. **Sign up** with GitHub (FREE)
3. **New Project** → Deploy from GitHub repo
4. **Select:** backend folder (or configure path)
5. **Environment Variables:**
   ```
   PORT=5000
   PYTHON_VERSION=3.11.0
   ```

**✅ Backend URL:** `https://your-app.railway.app`

### **Step 3: Update Frontend Config**
Update your frontend to use the Railway backend URL instead of localhost.

---

# 🚀 **OPTION 3: RENDER DEPLOYMENT**

## **Step 1: Create render.yaml**
```yaml
services:
  - type: web
    name: ics-frontend
    env: node
    buildCommand: npm install && npm run build
    startCommand: npm run preview
    envVars:
      - key: NODE_ENV
        value: production

  - type: web  
    name: ics-backend
    env: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && python server.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        value: 5000
```

## **Step 2: Deploy to Render**
1. **Go to:** https://render.com
2. **Sign up** (FREE)
3. **New** → Web Service
4. **Connect** GitHub repository
5. **Configure:**
   - Environment: `Python`
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python server.py`

**✅ URLs:**
- **Frontend:** `https://your-app.onrender.com`
- **Backend:** `https://your-backend.onrender.com`

---

# 🔧 **DEPLOYMENT CONFIGURATION FILES**

## **Update package.json**
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview --port 4173 --host",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  }
}
```

## **Create .env.production**
```bash
# Frontend production config
VITE_API_URL=https://your-backend-url.com/api
```

## **Update vite.config.ts for production**
```typescript
export default defineConfig({
  plugins: [react()],
  css: {
    postcss: './postcss.config.js',
  },
  server: {
    port: 5173,
    host: true
  },
  preview: {
    port: 4173,
    host: true
  }
})
```

---

# 🎯 **HACKATHON DEPLOYMENT CHECKLIST**

## **Before Presentation:**
- [ ] Code pushed to GitHub repository
- [ ] Frontend deployed and accessible
- [ ] Backend deployed and API working
- [ ] WADI data integration working (if available)
- [ ] All API endpoints responding
- [ ] Mobile responsive design tested
- [ ] Demo URLs bookmarked
- [ ] Screenshots taken as backup

## **Test Your Deployment:**
```bash
# Test frontend
curl https://your-frontend-url.com

# Test backend health
curl https://your-backend-url.com/api/health

# Test power data API
curl https://your-backend-url.com/api/power-data

# Test WADI integration (if available)
curl https://your-backend-url.com/api/wadi-info
```

## **Demo URLs to Prepare:**
1. **Main Dashboard:** `https://your-app.com`
2. **System Health:** `https://your-app.com/api/health`
3. **Power Monitoring:** `https://your-app.com/api/power-data`
4. **WADI Information:** `https://your-app.com/api/wadi-info`

---

# 🔍 **TROUBLESHOOTING**

## **Common Issues:**

### **"Build Failed"**
```bash
# Check node version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

### **"API Not Working"**
```bash
# Check backend logs in deployment platform
# Verify environment variables are set
# Test API endpoints individually
```

### **"CORS Errors"**
Update backend CORS settings:
```python
# In server.py
from flask_cors import CORS
CORS(app, origins=['https://your-frontend-url.com'])
```

### **"404 Not Found"**
Add `_redirects` file for Netlify:
```
/*    /index.html   200
```

---

# 🎁 **BONUS: CUSTOM DOMAIN** (Optional)

## **For Professional Demo:**
1. **Buy domain** (optional): namecheap.com, godaddy.com
2. **Configure DNS** in your deployment platform
3. **Enable HTTPS** (usually automatic)

Example: `https://team0verride-ics.com`

---

# 🏆 **PRESENTATION READY URLS**

After deployment, you'll have:

**Primary Demo:**
- **Dashboard:** `https://your-app-name.vercel.app`
- **Backend API:** `https://your-app-name.vercel.app/api`

**Backup Options:**
- **Netlify:** `https://your-site.netlify.app`
- **Railway:** `https://your-app.railway.app`
- **Render:** `https://your-app.onrender.com`

**Mobile Demo:** All URLs work on phones/tablets!

---

**🎯 Your hackathon demo is now bulletproof with multiple live URLs!** 