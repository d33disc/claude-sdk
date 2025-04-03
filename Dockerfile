FROM python:3.11-slim

WORKDIR /app

# Copy the package files
COPY claude_sdk ./claude_sdk
COPY setup.py README.md ./

# Install the package
RUN pip install -e .

# Install additional dependencies
RUN pip install uvicorn fastapi

# Copy the API server code
COPY api_server.py ./

# Expose the API server port
EXPOSE 8000

# Start the API server
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
