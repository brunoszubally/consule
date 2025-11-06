"""
AI Tanács - Base Agent Class
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
import asyncio
from datetime import datetime


class BaseAgent(ABC):
    """Base class for all AI Council agents"""

    def __init__(
        self,
        name: str,
        short_name: str,
        color: str,
        bio: str,
        expertise: list[str],
        speed_multiplier: float = 1.0,
        provider: str = "openai",
        model: str = "gpt-4"
    ):
        self.name = name
        self.short_name = short_name
        self.color = color
        self.bio = bio
        self.expertise = expertise
        self.speed_multiplier = speed_multiplier
        self.provider = provider
        self.model = model
        self.status = "idle"
        self.progress = 0
        self.response_text = ""
        self.confidence_score = 0.0

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get the system prompt that defines this agent's personality

        Must be implemented by each agent subclass
        """
        pass

    def get_base_prompt_prefix(self) -> str:
        """Common prefix for all agents"""
        return f"""Te egy AI Tanács tagja vagy. A neved: {self.name} ({self.short_name}).

Személyiséged: {self.bio}
Szakértői területeid: {', '.join(self.expertise)}

A feladatod, hogy a kérdésre válaszolj a saját egyedi perspektívádból.
Légy rövid, lényegre törő, de informatív (max 2-3 mondat).
Add meg a válasz végén egy 1-10-es bizalmi értéket is [CONFIDENCE: X.X] formátumban.
"""

    async def think(
        self,
        question: str,
        context: Optional[Dict[str, Any]] = None,
        api_client = None
    ) -> Dict[str, Any]:
        """
        Process a question and return response

        Args:
            question: The question to answer
            context: Optional context (previous responses, etc.)
            api_client: API client instance (OpenAI, Anthropic, etc.)

        Returns:
            Dict with response, confidence, timing info
        """
        start_time = datetime.now()
        self.status = "thinking"
        self.progress = 0

        try:
            # Simulate thinking time based on speed multiplier
            thinking_delay = 0.5 / self.speed_multiplier
            await asyncio.sleep(thinking_delay)
            self.status = "responding"
            self.progress = 50

            # Get full prompt
            system_prompt = self.get_system_prompt()
            full_prompt = f"{self.get_base_prompt_prefix()}\n\n{system_prompt}\n\nKérdés: {question}"

            # Call AI API (implementation depends on provider)
            if api_client:
                response_text, confidence = await self._call_api(
                    full_prompt,
                    question,
                    api_client
                )
            else:
                # Fallback: mock response for testing
                response_text = f"[{self.name}] Mock válasz a kérdésre: {question[:50]}..."
                confidence = 7.5

            self.response_text = response_text
            self.confidence_score = confidence
            self.progress = 100
            self.status = "complete"

            end_time = datetime.now()
            elapsed = (end_time - start_time).total_seconds()

            return {
                "agent": self.name,
                "short_name": self.short_name,
                "text": response_text,
                "confidence": confidence,
                "score": confidence,  # For voting
                "elapsed_seconds": elapsed,
                "color": self.color,
                "bio": self.bio
            }

        except Exception as e:
            self.status = "error"
            self.progress = 0
            return {
                "agent": self.name,
                "short_name": self.short_name,
                "text": f"Hiba történt: {str(e)}",
                "confidence": 0.0,
                "score": 0.0,
                "elapsed_seconds": 0,
                "color": self.color,
                "bio": self.bio,
                "error": str(e)
            }

    async def _call_api(
        self,
        system_prompt: str,
        user_message: str,
        api_client
    ) -> tuple[str, float]:
        """
        Call the appropriate AI API based on provider

        Returns: (response_text, confidence_score)
        """
        # This will be implemented based on the actual API client
        # For now, return mock data
        await asyncio.sleep(0.2 / self.speed_multiplier)
        return f"[{self.name} gondolat]", 7.5

    def to_dict(self) -> Dict[str, Any]:
        """Serialize agent state for WebSocket updates"""
        return {
            "name": self.name,
            "short_name": self.short_name,
            "color": self.color,
            "bio": self.bio,
            "expertise": self.expertise,
            "status": self.status,
            "progress": self.progress,
            "speed_multiplier": self.speed_multiplier,
            "response_text": self.response_text,
            "confidence_score": self.confidence_score
        }
