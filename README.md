# NiftyBridge_AI_assistant
### FastAPI Application

This app is an AI assistant that answers questions related to the Terms of Service(PDF).

## Prerequisites
- Python 3.10 or higher
- security API_KEY 
- OpenAI API key

## Getting Started

1. Clone this repository:

   ```shell
   git clone git@github.com:GavdzinskyiVeacheslav/NiftyBridge_AI_assistant.git

2. Change to the project directory:
   
   ```shell
   cd NiftyBridge_AI_assistant

3. Install the dependencies:

   ```shell
   pip install -r requirements.txt

## .env

```shell
API_KEY=
OPENAI_API_KEY=
```

## Launch

To start the application you need to generate an API key
```shell
python3 utils.py
```
Then copy the key and paste it into the API_KEY variable in the .env
After that we start the server for the API

## Running the Application

### Using Docker

1. Build the Docker image:

   ```shell
   docker build -t my-fastapi-app .

2. Run a Docker container based on the image:

   ```shell
   docker run -p 8000:8000 --env OPENAI_API_KEY=$OPENAI_API_KEY my-fastapi-app

The application will be accessible at http://localhost:8000/api/send.

### Without Docker

1. Start the application using uvicorn:

   ```shell
   uvicorn api:app --reload

The application will be accessible at http://localhost:8000/api/send.

## API Documentation

Once the application is running, you can access the Swagger UI documentation at http://localhost:8000/docs to explore
the available endpoints and interact with the API.

