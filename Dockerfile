# Base image
FROM python:3.10

# Set the working directory
WORKDIR /NiftyBridge_AI_assistant

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY app.py .
COPY api.py .
COPY auth.py .
COPY config.py .
COPY service_terms.pdf .
COPY .env .

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api:app --reload", "--host", "0.0.0.0", "--port", "8000"]
