"""
Example demonstrating async usage with the Claude SDK.
"""

import os
import asyncio
from claude_sdk import AsyncClaude

async def main():
    # Initialize the async client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = AsyncClaude(api_key=api_key)

    # Generate a response asynchronously
    response = await client.generate(
        model="claude-3-7-sonnet-20250219",
        prompt="What is the capital of Germany?",
        max_tokens=100,
        temperature=0.7,
    )

    print("Async Response:", response)

    # Using the messages API asynchronously
    messages_response = await client.messages_create(
        model="claude-3-7-sonnet-20250219",
        messages=[
            {"role": "user", "content": "What is the capital of Spain?"}
        ],
        max_tokens=100,
        temperature=0.7,
    )

    print("Async Messages API Response:", messages_response)

    # Multiple requests in parallel
    tasks = [
        client.generate(
            model="claude-3-7-sonnet-20250219",
            prompt=f"What is the capital of {country}?",
            max_tokens=100,
            temperature=0.7,
        )
        for country in ["France", "Italy", "Japan", "Brazil", "Australia"]
    ]
    
    parallel_responses = await asyncio.gather(*tasks)
    
    for i, response in enumerate(parallel_responses):
        print(f"Parallel response {i+1}:", response)

if __name__ == "__main__":
    asyncio.run(main())
