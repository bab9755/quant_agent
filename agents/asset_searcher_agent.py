import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))
from enum import Enum
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from utils.models import Strategy
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from typing import List

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

print(GEMINI_API_KEY)
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY


def generate_tickers(universe: str) -> list[str]:
    pass


class TickerList(BaseModel):
    tickers: List[str]


asset_searcher_agent = create_react_agent(
    model='google_genai:gemini-2.0-flash',
    tools=[],
    prompt="You are a helpful asset searcher that finds tickers for a given universe. Return an array of string tickers that are found in the universe you are given.",
    name="asset_searcher",
    response_format=TickerList
)


if __name__ == "__main__":
    print("Running the agent")
    response = asset_searcher_agent.invoke({
        "messages": [{
            "role": "user",
            "content": "What are the tickers for the S&P 500?"
        }]
    })

    tickers = response['structured_response'].tickers
    print(tickers)