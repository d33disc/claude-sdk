"""
Asynchronous Claude client for interacting with Anthropic's Claude AI models.
"""

import os
import aiohttp
import json
from typing import Dict, List, Optional, Union, Any, AsyncGenerator

class AsyncClaude:
    """
    Asynchronous client for the Anthropic Claude API.
    
    Args:
        api_key (str, optional): Anthropic API key. If not provided, it will be read from
            the ANTHROPIC_API_KEY environment variable.
        base_url (str, optional): Base URL for the Anthropic API.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.anthropic.com",
    ):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or through the ANTHROPIC_API_KEY environment variable."
            )
        self.base_url = base_url
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
    
    async def generate(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        stream: bool = False,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> Union[Dict[str, Any], AsyncGenerator[str, None]]:
        """
        Generate a response from Claude asynchronously.
        
        Args:
            model (str): The Claude model to use (e.g., "claude-3-7-sonnet-20250219").
            prompt (str): The user prompt to send to Claude.
            max_tokens (int, optional): Maximum number of tokens to generate.
            temperature (float, optional): Sampling temperature.
            system_prompt (str, optional): System prompt to guide Claude's behavior.
            stream (bool, optional): Whether to stream the response.
            tools (List[Dict[str, Any]], optional): List of tools for Claude to use.
            
        Returns:
            Union[Dict[str, Any], AsyncGenerator[str, None]]: Response from Claude.
        """
        messages = [{"role": "user", "content": prompt}]
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        if tools:
            payload["tools"] = tools
            
        endpoint = f"{self.base_url}/v1/messages"
        
        async with aiohttp.ClientSession() as session:
            if stream:
                payload["stream"] = True
                async with session.post(endpoint, json=payload, headers=self.headers) as response:
                    response.raise_for_status()
                    return self._handle_streaming_response(response)
            else:
                async with session.post(endpoint, json=payload, headers=self.headers) as response:
                    response.raise_for_status()
                    return await response.json()
    
    async def _handle_streaming_response(self, response):
        """
        Handle streaming response from Claude asynchronously.
        
        Args:
            response: Streaming response from aiohttp.
            
        Returns:
            AsyncGenerator yielding response chunks.
        """
        async for line in response.content:
            line = line.decode("utf-8").strip()
            if line:
                if line.startswith("data: "):
                    data = line[6:]  # Remove "data: " prefix
                    if data != "[DONE]":
                        yield data
                        
    async def messages_create(
        self,
        model: str,
        messages: List[Dict[str, Union[str, List[Dict[str, str]]]]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
    ) -> Union[Dict[str, Any], AsyncGenerator[str, None]]:
        """
        Create a message using the Claude API asynchronously.
        
        This method is compatible with the official Anthropic API format.
        
        Args:
            model (str): The Claude model to use.
            messages (List[Dict]): The messages to send to Claude.
            max_tokens (int, optional): Maximum number of tokens to generate.
            temperature (float, optional): Sampling temperature.
            system (str, optional): System prompt to guide Claude's behavior.
            tools (List[Dict], optional): List of tools for Claude to use.
            stream (bool, optional): Whether to stream the response.
            
        Returns:
            Union[Dict[str, Any], AsyncGenerator[str, None]]: Response from Claude.
        """
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        if system:
            payload["system"] = system
            
        if tools:
            payload["tools"] = tools
            
        endpoint = f"{self.base_url}/v1/messages"
        
        async with aiohttp.ClientSession() as session:
            if stream:
                payload["stream"] = True
                async with session.post(endpoint, json=payload, headers=self.headers) as response:
                    response.raise_for_status()
                    return self._handle_streaming_response(response)
            else:
                async with session.post(endpoint, json=payload, headers=self.headers) as response:
                    response.raise_for_status()
                    return await response.json()
                    
    async def compute_use(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Use Claude's computer use feature to perform desktop automation asynchronously.
        
        Args:
            model (str): The Claude model to use (must support computer use).
            prompt (str): The user prompt instructing Claude what to do.
            max_tokens (int, optional): Maximum number of tokens to generate.
            temperature (float, optional): Sampling temperature.
            system_prompt (str, optional): System prompt to guide Claude's behavior.
            
        Returns:
            Dict[str, Any]: Response from Claude.
        """
        messages = [{"role": "user", "content": prompt}]
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "computer_use": True,
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        endpoint = f"{self.base_url}/v1/messages"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload, headers=self.headers) as response:
                response.raise_for_status()
                return await response.json()
