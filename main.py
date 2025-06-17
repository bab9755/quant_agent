from enum import Enum
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.models import Strategy
from langgraph_supervisor import create_supervisor
from agents import prompt_parser_agent, asset_searcher_agent, strategy_decision_agent, strategy_code_executor_agent, backtesting_agent

load_dotenv()



strategy_supervisor = create_supervisor(
    agents=[
        prompt_parser_agent,
        asset_searcher_agent,
        strategy_decision_agent,
        strategy_code_executor_agent,
        backtesting_agent
    ],
    model='google_genai:gemini-2.0-flash',
    prompt="",
).compile() # compile the agents




user_input = input("What do you wanna research about the stock market today?\n")


for chunk in strategy_supervisor.stream(
    {
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }
):
    print(chunk)
    print('\n')

