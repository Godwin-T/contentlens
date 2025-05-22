# Use a Python base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

RUN chmod +x prepare_db.sh && \
    ./prepare_db.sh 

# Expose the port Uvicorn will run on (default is 8000)
EXPOSE 8000

# Command to run Uvicorn (adjust app name accordingly)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
