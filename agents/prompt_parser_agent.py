import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from enum import Enum
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from utils.models import Strategy, Frequency
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

print(GEMINI_API_KEY)
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

prompt_parser_agent = create_react_agent(
    model='google_genai:gemini-2.0-flash',
    tools=[],
    prompt="You are a strategy parser that extracts trading strategy components from natural language input.",
    name="prompt_parser",
    response_format=Strategy
)

# Test the prompt parser
if __name__ == "__main__":
    print("Running the agent")
    response = prompt_parser_agent.invoke({
        "messages": [{
            "role": "user",
            "content": "I want to create a momentum strategy for S&P 500 stocks with daily frequency and 20-day lookback"
        }]
    })

    strategy = response['structured_response']
    print(strategy.strategy_type)
    print(strategy.universe)
    print(strategy.frequency)
    print(strategy.lookback)


