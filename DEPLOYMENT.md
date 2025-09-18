# 🚀 Live Demo Deployment Guide

This guide will help you deploy your Full-Stack LLM Agent to make it live for your portfolio website.

## 🎯 Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)

**Steps:**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository: `Anshitaa/Full-Stack-LLM-Agent-with-a-Dynamic-Knowledge-Base`
5. Railway will automatically detect the `railway.json` and deploy
6. Add environment variables:
   - `OPENAI_API_KEY`: Your actual OpenAI API key
   - `CHROMA_PERSIST_DIRECTORY`: `/app/chroma_db`
7. Your app will be live at: `https://your-app-name.railway.app`

**Advantages:**
- ✅ One-click deployment
- ✅ Automatic HTTPS
- ✅ Free tier available
- ✅ Easy environment variable management

### Option 2: Render

**Steps:**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Render will detect `render.yaml` and configure automatically
6. Add environment variables in the dashboard
7. Deploy!

**Advantages:**
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Built-in monitoring

### Option 3: Vercel + Railway (Split Deployment)

**For Frontend (Vercel):**
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set build command: `cd frontend && npm run build`
4. Set output directory: `frontend/build`
5. Deploy!

**For Backend (Railway):**
1. Deploy backend to Railway (Option 1)
2. Update `vercel.json` with your Railway backend URL
3. Redeploy frontend

## 🔧 Pre-Deployment Setup

### 1. Update Environment Variables

Before deploying, update your `docker-compose.yml` with your actual API key:

```yaml
environment:
  - OPENAI_API_KEY=your_actual_openai_api_key_here
  - CHROMA_PERSIST_DIRECTORY=/app/chroma_db
```

### 2. Test Locally First

```bash
# Make sure everything works locally
docker-compose up --build

# Test the endpoints
curl http://localhost:8000/health
curl http://localhost:3000
```

### 3. Push to GitHub

```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

## 🌐 Post-Deployment

### 1. Get Your Live URL
After deployment, you'll get a URL like:
- Railway: `https://your-app-name.railway.app`
- Render: `https://your-app-name.onrender.com`
- Vercel: `https://your-app-name.vercel.app`

### 2. Test Your Live Demo
- Visit your live URL
- Test the chat functionality
- Upload a document
- Verify everything works

### 3. Add to Portfolio
Add this to your portfolio website:

```html
<div class="project-demo">
  <h3>Full-Stack LLM Agent with Dynamic Knowledge Base</h3>
  <p>AI-powered chat application with document upload and RAG capabilities</p>
  <a href="https://your-live-url.com" target="_blank" class="demo-button">
    🚀 Live Demo
  </a>
  <a href="https://github.com/Anshitaa/Full-Stack-LLM-Agent-with-a-Dynamic-Knowledge-Base" target="_blank">
    📁 Source Code
  </a>
</div>
```

## 🎨 Portfolio Integration

### Demo Features to Highlight:
- ✅ **Real-time AI Chat** - Powered by OpenAI GPT
- ✅ **Document Upload** - PDF processing and indexing
- ✅ **RAG Pipeline** - Retrieval-Augmented Generation
- ✅ **Modern UI** - React with responsive design
- ✅ **Full-Stack** - FastAPI backend + React frontend
- ✅ **Dockerized** - Production-ready containerization
- ✅ **Vector Database** - ChromaDB for similarity search

### Screenshots to Take:
1. Main chat interface
2. Document upload functionality
3. AI responses with sources
4. Mobile responsive design
5. API documentation page

## 🔧 Troubleshooting

### Common Issues:

**1. Environment Variables Not Set**
- Check your deployment platform's environment variable settings
- Ensure `OPENAI_API_KEY` is properly configured

**2. Build Failures**
- Check the build logs in your deployment platform
- Ensure all dependencies are properly specified

**3. CORS Issues**
- The nginx configuration should handle this
- Check if your frontend can reach the backend

**4. Memory Issues**
- Some platforms have memory limits
- Consider upgrading to a paid plan if needed

## 📊 Monitoring

### Health Checks:
- Backend: `https://your-url.com/health`
- Frontend: `https://your-url.com/`
- API Docs: `https://your-url.com/docs`

### Performance:
- Monitor response times
- Check memory usage
- Track error rates

## 🎉 Success!

Once deployed, your Full-Stack LLM Agent will be live and accessible to anyone on the internet. This makes for an impressive portfolio piece that demonstrates:

- Full-stack development skills
- AI/ML integration
- Modern web technologies
- Production deployment experience
- Real-world problem solving

**Your live demo URL will be perfect for:**
- Portfolio websites
- Resume links
- LinkedIn projects
- Job applications
- Technical interviews

---

**Need help?** Check the deployment platform's documentation or create an issue in your GitHub repository.
