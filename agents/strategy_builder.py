from enum import Enum
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from utils.models import Strategy
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

load_dotenv()

strategy_decision_agent = create_react_agent(
    model='google_genai:gemini-2.0-flash',
    tools=[],
    system_prompt="",
    name="strategy_decision"
)