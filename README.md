# FinBot — Analyst Research Assistant

**🚀 Live Demo: [https://witty-stone-0e9fa850f.6.azurestaticapps.net](https://witty-stone-0e9fa850f.6.azurestaticapps.net)**

FinBot is a full-stack financial research tool built with FastAPI and Next.js, deployed on Azure. It uses LangGraph and Groq to produce structured analyst briefs for stocks.


## Project Structure

- **`/app`**: FastAPI backend code. Handle LLM logic, tool execution, and state management.
- **`/frontend`**: Next.js (Tailwind CSS) frontend. The user interface for the AI chat.
- **`.github/workflows`**: Automated deployment scripts for Azure Static Web Apps.

## Deployment Details

### 🐍 Backend (Azure App Service)
The backend is hosted at `https://ramlal-finbot-api.azurewebsites.net`.
- **Logic**: Python 3.13
- **Deployment**: Manual via `az webapp up --name ramlal-finbot-api`

### ⚛️ Frontend (Azure Static Web Apps)
The frontend is hosted at `https://ramlal-finbot-app.azurestaticapps.net`.
- **Framework**: Next.js 15
- **Deployment**: **Automatic via GitHub Actions**. Any change pushed to the `main` branch of this repository will trigger a fresh build and deployment.

## How to Share & Run
If someone wants to run this project:
1. **Clone** the repo.
2. **Backend**: Install dependencies from `requirements.txt` and run `python run.py`.
3. **Frontend**: Navigate to `/frontend`, run `npm install` and `npm run dev`.
4. **Environment**: Ensure `.env` (backend) and `.env.local` (frontend) are configured with API keys.

