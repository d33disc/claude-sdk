"""
Claude client for interacting with Anthropic's Claude AI models.
"""

import os
import json
import requests
from typing import Dict, List, Optional, Union, Any, Generator

from .exceptions import handle_api_error
from .utils import validate_api_key

class Claude:
    """
    Client for the Anthropic Claude API.
    
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
    
    def generate(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        stream: bool = False,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> Union[Dict[str, Any], Generator[str, None, None]]:
        """
        Generate a response from Claude.
        
        Args:
            model (str): The Claude model to use (e.g., "claude-3-7-sonnet-20250219").
            prompt (str): The user prompt to send to Claude.
            max_tokens (int, optional): Maximum number of tokens to generate.
            temperature (float, optional): Sampling temperature.
            system_prompt (str, optional): System prompt to guide Claude's behavior.
            stream (bool, optional): Whether to stream the response.
            tools (List[Dict[str, Any]], optional): List of tools for Claude to use.
            
        Returns:
            Union[Dict[str, Any], Generator[str, None, None]]: Response from Claude or a generator
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
        
        if stream:
            payload["stream"] = True
            response = requests.post(endpoint, json=payload, headers=self.headers, stream=True)
            
            if response.status_code >= 400:
                error_data = response.json()
                handle_api_error(response.status_code, error_data)
                
            return self._handle_streaming_response(response)
        else:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            response_data = response.json()
            
            if response.status_code >= 400:
                handle_api_error(response.status_code, response_data)
                
            return response_data
    
    def _handle_streaming_response(self, response) -> Generator[str, None, None]:
        """
        Handle streaming response from Claude.
        
        Args:
            response: Streaming response from requests.
            
        Yields:
            str: Response chunks.
        """
        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                if data.startswith("data: "):
                    data = data[6:]  # Remove "data: " prefix
                    if data != "[DONE]":
                        yield data
                        
    def messages_create(
        self,
        model: str,
        messages: List[Dict[str, Union[str, List[Dict[str, str]]]]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
    ) -> Union[Dict[str, Any], Generator[str, None, None]]:
        """
        Create a message using the Claude API.
        
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
            Union[Dict[str, Any], Generator[str, None, None]]: Response from Claude or a generator
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
        
        if stream:
            payload["stream"] = True
            response = requests.post(endpoint, json=payload, headers=self.headers, stream=True)
            
            if response.status_code >= 400:
                error_data = response.json()
                handle_api_error(response.status_code, error_data)
                
            return self._handle_streaming_response(response)
        else:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            response_data = response.json()
            
            if response.status_code >= 400:
                handle_api_error(response.status_code, response_data)
                
            return response_data
            
    def compute_use(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Use Claude's computer use feature to perform desktop automation.
        
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
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response_data = response.json()
        
        if response.status_code >= 400:
            handle_api_error(response.status_code, response_data)
            
        return response_data