FROM python:3.11-slim

WORKDIR /app

# Copy the requirements.txt file from the server directory (relative to the Dockerfile)
COPY requirements.txt .

# Install the dependencies from the server's requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the client directory files (e.g., home.py) to the container
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Run the Streamlit app when the container starts
CMD ["streamlit", "run", "home.py", "--server.port=8501", "--server.headless=true"]


