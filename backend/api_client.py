"""
AI Tanács - API Client for OpenAI and Anthropic
"""
import asyncio
import re
from typing import Tuple, Optional
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from config import settings


class AIApiClient:
    """
    Unified API client for multiple AI providers
    """

    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None

        # Initialize clients if API keys are available
        if settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

        if settings.anthropic_api_key:
            self.anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def call_openai(
        self,
        system_prompt: str,
        user_message: str,
        model: str = "gpt-4",
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Tuple[str, float]:
        """
        Call OpenAI API

        Returns: (response_text, confidence_score)
        """
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")

        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=settings.timeout_seconds
            )

            text = response.choices[0].message.content or ""
            confidence = self._extract_confidence(text)

            return text, confidence

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return f"Hiba az OpenAI hívásban: {str(e)}", 0.0

    async def call_anthropic(
        self,
        system_prompt: str,
        user_message: str,
        model: str = "claude-3-sonnet-20240229",
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Tuple[str, float]:
        """
        Call Anthropic API

        Returns: (response_text, confidence_score)
        """
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")

        try:
            response = await self.anthropic_client.messages.create(
                model=model,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=settings.timeout_seconds
            )

            text = response.content[0].text if response.content else ""
            confidence = self._extract_confidence(text)

            return text, confidence

        except Exception as e:
            print(f"Anthropic API error: {e}")
            return f"Hiba az Anthropic hívásban: {str(e)}", 0.0

    async def call_api(
        self,
        provider: str,
        model: str,
        system_prompt: str,
        user_message: str,
        max_tokens: int = None,
        temperature: float = None
    ) -> Tuple[str, float]:
        """
        Unified API call - routes to correct provider

        Args:
            provider: 'openai' or 'anthropic'
            model: Model name
            system_prompt: System prompt
            user_message: User message
            max_tokens: Max tokens (default from settings)
            temperature: Temperature (default from settings)

        Returns:
            (response_text, confidence_score)
        """
        max_tokens = max_tokens or settings.max_tokens
        temperature = temperature or settings.temperature

        if provider == "openai":
            return await self.call_openai(
                system_prompt,
                user_message,
                model,
                max_tokens,
                temperature
            )
        elif provider == "anthropic":
            return await self.call_anthropic(
                system_prompt,
                user_message,
                model,
                max_tokens,
                temperature
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def _extract_confidence(self, text: str) -> float:
        """
        Extract confidence score from agent response

        Looks for [CONFIDENCE: X.X] pattern in text
        """
        pattern = r'\[CONFIDENCE:\s*(\d+\.?\d*)\]'
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            try:
                confidence = float(match.group(1))
                return min(10.0, max(0.0, confidence))  # Clamp to 0-10
            except ValueError:
                pass

        # Default confidence if not found
        return 7.0


# Global API client instance
api_client = AIApiClient()


# Update BaseAgent to use real API client
from agents.base import BaseAgent

# Monkey-patch the _call_api method
async def _call_api_real(
    self,
    system_prompt: str,
    user_message: str,
    client
) -> Tuple[str, float]:
    """
    Real API call implementation
    """
    if client is None:
        # Fallback to mock if no client
        await asyncio.sleep(0.2 / self.speed_multiplier)
        return f"[{self.name}] Mock válasz", 7.5

    try:
        return await client.call_api(
            provider=self.provider,
            model=self.model,
            system_prompt=system_prompt,
            user_message=user_message
        )
    except Exception as e:
        print(f"API call error for {self.name}: {e}")
        return f"[{self.name}] API hiba: {str(e)}", 0.0


# Apply the patch
BaseAgent._call_api = _call_api_real
