from enum import Enum
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from dotenv import load_dotenv
import os
from utils.models import Strategy

load_dotenv()

user_input = input("What do you wanna research about the stock market today? ")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

model = GeminiModel(
    'gemini-2.0-flash', provider=GoogleGLAProvider(api_key=GEMINI_API_KEY)
)

parser_agent = Agent(model)

result = parser_agent.run_sync(user_input, output_type=Strategy)

if not result:
    raise ValueError("Error generating a result from the agent call")

print(result.output)
