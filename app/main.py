from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import BriefRequest, BriefResponse
from app.agent import run_agent
from dotenv import load_dotenv

_ = load_dotenv()
app = FastAPI(title="FinBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
    "https://finbot-api.azurewebsites.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/brief", response_model=BriefResponse)
def brief(payload: BriefRequest):
    result = run_agent(payload.query, payload.thread_id)
    return BriefResponse(result=result)