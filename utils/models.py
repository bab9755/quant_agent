from pydantic import BaseModel
from enum import Enum
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

class Frequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class Strategy(BaseModel):
    strategy_type: str
    universe: str
    frequency: Frequency
    lookback: int

