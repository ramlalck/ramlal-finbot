from app.config import settings
import yfinance as yf
from langchain.tools import tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool


@tool
def get_stock_fundamentals(ticker: str) -> dict:
    """Get current stock fundamentals for a ticker."""
    stock = yf.Ticker(ticker)
    info = stock.info or {}
    return {
        "price": info.get("currentPrice"),
        "pe_ratio": info.get("trailingPE"),
        "market_cap": info.get("marketCap"),
        "revenue_growth": info.get("revenueGrowth"),
        "52w_high": info.get("fiftyTwoWeekHigh"),
        "52w_low": info.get("fiftyTwoWeekLow"),
    }


_SERPAPI_KEY = settings.serpapi_api_key


@tool
def search_news(query: str) -> str:
    """Search last-24h Google News via SerpAPI."""
    if not _SERPAPI_KEY:
        raise ValueError("SERPAPI_API_KEY is not set.")
    serp = SerpAPIWrapper(
        serpapi_api_key=_SERPAPI_KEY,
        params={"tbm": "nws", "tbs": "qdr:d"},
    )
    return serp.run(query)


wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
yahoo_news_tool = YahooFinanceNewsTool()

tools = [
    get_stock_fundamentals,
    yahoo_news_tool,
    wikipedia_tool,
    *([search_news] if _SERPAPI_KEY else []),
]