import os
import sqlite3
from pathlib import Path

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langsmith import traceable
from app.config import settings
from app.tools import tools


SYSTEM_PROMPT = """
You are FinBot, an expert equity research analyst with deep knowledge of financial markets,
valuation methodologies, and macroeconomic trends.

## Task
Given a stock ticker or company name, produce a concise, structured analyst brief that helps users evaluate the investment. Do not give buy/sell advice. Present data-driven signals only.

## Rules
1. Gather data before analysis. Never rely on memory for numbers.
2. If a tool fails or returns empty data, state it and proceed.
3. Never fabricate prices, ratios, or news.
4. Always follow the output format.
5. Flag notable risks or red flags.

## Output Format

**[TICKER] — Analyst Brief**
- **Fundamentals:** price, P/E, market cap, revenue growth (one line)
- **Valuation Signal:** OVERVALUED / FAIRLY VALUED / UNDERVALUED + reason
- **News Sentiment:** bullish / neutral / bearish + key headline
- **Key Risks:** 1–2 bullets
- **Outlook:** 1–2 sentence synthesis, no advice
"""


os.environ["GROQ_API_KEY"] = settings.groq_api_key
os.environ["SERPAPI_API_KEY"] = settings.serpapi_api_key

llm = ChatGroq(
    model=settings.groq_model,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

Path(settings.sqlite_db_path).parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(settings.sqlite_db_path, check_same_thread=False)
checkpointer = SqliteSaver(conn)
checkpointer.setup()

agent = create_agent(
    llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)


@traceable(name="FinBot: Full Stock Brief", run_type="chain")
def run_agent(query: str, thread_id: str) -> str:
    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config={"configurable": {"thread_id": thread_id}},
    )

    messages = response.get("messages", [])
    if not messages:
        return "No response returned."

    last = messages[-1]
    content = getattr(last, "content", "")

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                texts.append(item.get("text", ""))
        return "\n".join(texts).strip()

    return str(content)