"""
Example demonstrating computer use with the Claude SDK.
"""

import os
from claude_sdk import Claude

# Initialize the client
api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Claude(api_key=api_key)

def main():
    print("Claude Computer Use Example")
    print("--------------------------")
    print("Note: This requires the Claude 3.5 or 3.7 model with computer use capability enabled.")
    print("You also need to have the Docker container running with the computer use environment.")
    
    # Get a task from the user
    task = input("\nWhat would you like Claude to do on your computer? ")
    
    # Send the task to Claude
    try:
        response = client.compute_use(
            model="claude-3-7-sonnet-20250219",
            prompt=task,
            max_tokens=4000,
            temperature=0.7,
        )
        
        print("\nClaude is now executing your task.")
        print("Check the web interface at http://localhost:8080 to see Claude operating your computer.")
        print("\nResponse:", response)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the computer use Docker container is running and properly configured.")

if __name__ == "__main__":
    main()
