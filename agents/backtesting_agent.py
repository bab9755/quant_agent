from enum import Enum
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.models import Strategy
from langgraph.prebuilt import create_react_agent

load_dotenv()


backtesting_agent = create_react_agent(
    model='google_genai:gemini-2.0-flash',
    tools=[],
    system_prompt="",
    name="backtesting"
)

