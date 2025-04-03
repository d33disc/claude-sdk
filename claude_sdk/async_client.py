"""
Asynchronous client for interacting with Anthropic's Claude AI models.
"""

import os
import json
import aiohttp
from typing import Dict, List, Optional, Union, Any, AsyncGenerator

from .exceptions import handle_api_error
from .utils import validate_api_key

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
        self.api_key = validate_api_key(api_key)
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
        Asynchronously generate a response from Claude.
        
        Args:
            model (str): The Claude model to use (e.g., "claude-3-7-sonnet-20250219").
            prompt (str): The user prompt to send to Claude.
            max_tokens (int, optional): Maximum number of tokens to generate.
            temperature (float, optional): Sampling temperature.
            system_prompt (str, optional): System prompt to guide Claude's behavior.
            stream (bool, optional): Whether to stream the response.
            tools (List[Dict[str, Any]], optional): List of tools for Claude to use.
            
        Returns:
            Union[Dict[str, Any], AsyncGenerator[str, None]]: Response from Claude or a generator
                that yields streamed responses.
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
                    if response.status >= 400:
                        error_data = await response.json()
                        handle_api_error(response.status, error_data)
                    
                    return self._handle_streaming_response(response)
            else:
                async with session.post(endpoint, json=payload, headers=self.headers) as response:
                    response_data = await response.json()
                    
                    if response.status >= 400:
                        handle_api_error(response.status, response_data)
                        
                    return response_data
    
    async def _handle_streaming_response(self, response: aiohttp.ClientResponse) -> AsyncGenerator[str, None]:
        """
        Handle streaming response from Claude.
        
        Args:
            response: Streaming response from aiohttp.
            
        Yields:
            str: Response chunks.
        """
        async for line in response.content:
            line = line.decode("utf-8").strip()
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
        Asynchronously create a message using the Claude API.
        
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
            Union[Dict[str, Any], AsyncGenerator[str, None]]: Response from Claude or a generator
                that yields streamed responses.
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
                    if response.status >= 400:
                        error_data = await response.json()
                        handle_api_error(response.status, error_data)
                    
                    return self._handle_streaming_response(response)
            else:
                async with session.post(endpoint, json=payload, headers=self.headers) as response:
                    response_data = await response.json()
                    
                    if response.status >= 400:
                        handle_api_error(response.status, response_data)
                        
                    return response_data