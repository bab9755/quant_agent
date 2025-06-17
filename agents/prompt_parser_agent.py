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

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

def parse_strategy_prompt(user_input: str) -> Strategy:
    """
    Parse user input into a Strategy object.
    Example input: "I want to create a momentum strategy for S&P 500 stocks with daily frequency and 20-day lookback"
    """
    # Use the agent to extract strategy components
    result = prompt_parser_agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"""Extract strategy components from this input: {user_input}
            Return a JSON with these fields:
            - strategy_type: type of strategy (e.g., momentum, mean_reversion)
            - universe: trading universe (e.g., S&P 500, NASDAQ)
            - frequency: trading frequency (daily, weekly, monthly, quarterly, yearly)
            - lookback: number of periods to look back (integer)
            """
        }]
    })
    
    # Parse the response into a Strategy object
    try:
        strategy_data = result.output
        return Strategy(
            strategy_type=strategy_data["strategy_type"],
            universe=strategy_data["universe"],
            frequency=Frequency[strategy_data["frequency"].upper()],
            lookback=int(strategy_data["lookback"])
        )
    except Exception as e:
        raise ValueError(f"Failed to parse strategy from input: {e}")

prompt_parser_agent = create_react_agent(
    model='google_genai:gemini-2.0-flash',
    tools=[parse_strategy_prompt],
    prompt="You are a strategy parser that extracts trading strategy components from natural language input.",
    name="prompt_parser"
)

# Test the prompt parser
if __name__ == "__main__":
    test_inputs = [
        "I want to create a momentum strategy for S&P 500 stocks with daily frequency and 20-day lookback",
        "Create a mean reversion strategy for NASDAQ-100 using weekly data with 10-week lookback period",
        "Build a trend following strategy for Russell 2000 with monthly frequency and 6-month lookback"
    ]
    
    print("Testing Prompt Parser Agent...")
    print("-" * 50)
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\nTest {i}:")
        print(f"Input: {test_input}")
        try:
            strategy = parse_strategy_prompt(test_input)
            print("Parsed Strategy:")
            print(f"- Type: {strategy.strategy_type}")
            print(f"- Universe: {strategy.universe}")
            print(f"- Frequency: {strategy.frequency}")
            print(f"- Lookback: {strategy.lookback}")
        except Exception as e:
            print(f"Error: {str(e)}")
        print("-" * 50)


