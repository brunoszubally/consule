"""
AI Tanács - Agents Package
"""
from .base import BaseAgent
from .council import (
    StrategaAgent,
    KreativAgent,
    PraktikusAgent,
    FilozofusAgent,
    TechnikusAgent,
    SzkeptikusAgent,
    EmpatikusAgent,
    KiserletiAgent,
    TortenelemAgent,
    GyakorlatiAgent,
    ReszletesAgent,
    HumoristAgent,
    create_council
)

__all__ = [
    "BaseAgent",
    "StrategaAgent",
    "KreativAgent",
    "PraktikusAgent",
    "FilozofusAgent",
    "TechnikusAgent",
    "SzkeptikusAgent",
    "EmpatikusAgent",
    "KiserletiAgent",
    "TortenelemAgent",
    "GyakorlatiAgent",
    "ReszletesAgent",
    "HumoristAgent",
    "create_council",
]
