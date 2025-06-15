from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()


from dataclasses import dataclass

@dataclass
class TickerFetcherDeps:
    universe: str

class Ticker(BaseModel):
    ticker: str

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

model = GeminiModel(
    'gemini-2.0-flash', provider=GoogleGLAProvider(api_key=GEMINI_API_KEY)
)

ticker_agent = Agent(model, system_prompt="You are a helpful assistant that fetches tickers for a given universe. Return an array of string tickers that are found in the universe you are given", output_type=list[str])


result = ticker_agent.run_sync("What are the tickers for the S&P 500?", deps=TickerFetcherDeps(universe="S&P 500"))


print(result.output)

    




