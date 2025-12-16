# Django RAG Chatbot API

## Project Overview
Django RAG Chatbot API is a backend-only REST service built with Django and Django Rest Framework.  
It implements a Retrieval-Augmented Generation (RAG) pipeline using LangChain and FAISS to answer user questions from a private knowledge base.

This project is headless and can be integrated with any frontend (Web, Mobile, etc.).

---

## Key Features
- Retrieval-Augmented Generation (RAG) using FAISS
- Domain-specific answers from local documents
- API-first architecture (DRF)
- JWT authentication (SimpleJWT)
- Persistent chat history
- Automated cleanup of old chat logs
- Stateless and secure backend

---

## Technologies Used
- Django 5.x
- Django Rest Framework
- SimpleJWT (JWT Authentication)
- LangChain
- OpenAI API or Google Gemini
- FAISS (Vector Store)
- APScheduler
- SQLite (default)
- Python 3.10+
- python-dotenv

---

## RAG Pipeline Overview
1. User sends a message via API
2. Message is converted into vector embeddings
3. FAISS retrieves relevant chunks from faq.txt
4. Retrieved context is injected into the LLM prompt
5. LLM generates a context-aware response
6. Response is returned as JSON

---

## Database Design
- SQLite database
- ChatMessage model linked to Django User model
- Ensures user-specific chat history
- ACID-compliant storage

---

## Authentication (JWT)
- Implemented using djangorestframework-simplejwt
- Access token (short-lived)
- Refresh token (long-lived)
- All chat endpoints require authentication
- No server-side sessions

---

## Background Tasks
- APScheduler runs automatically with Django
- Deletes chat messages older than 30 days
- No Celery or external worker required

---

## API Base URL
http://127.0.0.1:8000/api/

---

## Authentication Endpoints

### Register
POST /signup/

Request Body:
{
  "username": "user1",
  "password": "password123"
}

Response:
201 Created

---

### Login
POST /login/

Request Body:
{
  "username": "user1",
  "password": "password123"
}

Response:
{
  "refresh": "eyJ0eX...",
  "access": "eyJ0eX..."
}

---

## Chat Endpoints (Bearer Token Required)

### Send Message
POST /chat/

Headers:
Authorization: Bearer <access_token>

Request Body:
{
  "message": "How do I reset my password?"
}

Response:
{
  "response": "To reset your password, go to settings..."
}

---

### Get Chat History
GET /chat-history/

Headers:
Authorization: Bearer <access_token>

Response:
[
  {
    "message": "How do I reset my password?",
    "response": "To reset your password..."
  }
]

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- OpenAI API Key or Google Gemini API Key

---

### Installation

Clone the repository:
git clone <repository-url>
cd <project-folder>

Create virtual environment (Windows):
python -m venv env
env\Scripts\activate

Install dependencies:
pip install -r requirements.txt

---

### Environment Configuration
Create a .env file in the project root:

OPENAI_API_KEY=sk-xxxx
OR
GOOGLE_API_KEY=AIza...

---

### Knowledge Base Setup
Create the following structure:

knowledge_base/
faq.txt

Add your domain-specific data inside faq.txt.

---

### Database Setup
python manage.py makemigrations
python manage.py migrate

---

### Run Server
python manage.py runserver

---

## Future Improvements
- WebSocket streaming with Django Channels
- Multi-session chat support
- Vector DB persistence
- Admin analytics dashboard

---

## requirements.txt
Django>=5.0
djangorestframework
djangorestframework-simplejwt
django-cors-headers
apscheduler
openai
langchain
langchain-community
langchain-openai
langchain-text-splitters
faiss-cpu
python-dotenv
pydantic


### How did you integrate the RAG pipeline for the chatbot, and what role does document retrieval play in the response generation?

The chatbot uses a Retrieval-Augmented Generation (RAG) pipeline implemented with LangChain.  
When a user sends a message:

1. The query is converted into vector embeddings.
2. FAISS performs a similarity search over the local knowledge base file (`faq.txt`).
3. The most relevant text chunks are retrieved.
4. These retrieved chunks are injected into the LLM prompt as contextual information.

This ensures that responses are grounded in domain-specific data rather than relying solely on the LLM’s general knowledge.

---

### What database and model structure did you use for storing user and chat history, and why did you choose this approach?

The application uses SQLite as the database for development simplicity and portability.

A `ChatMessage` model is linked to Django’s built-in `User` model using a ForeignKey.  
This approach was chosen because:

- It ensures strict user-level data isolation
- Relational databases provide ACID compliance
- Chat history can be easily queried, filtered, and maintained
- It scales well to production databases like PostgreSQL

---

### How did you implement user authentication using JWT? What security measures did you take for handling passwords and tokens?

Authentication is implemented using `djangorestframework-simplejwt`.

- Users authenticate with a username and password
- Upon login, the API issues an access token (short-lived) and a refresh token
- All protected endpoints require a valid Bearer token

Security measures include:
- Passwords are hashed using Django’s default password hashing system
- Tokens are stateless and not stored server-side
- Access tokens have a short expiration time
- Sensitive credentials are stored in environment variables

---

### How does the chatbot generate responses using the AI model (GPT-3) after retrieving documents?

After document retrieval:

1. The retrieved context is combined with the user query into a structured prompt
2. The prompt follows this format:

   Answer using the following context:
   [Retrieved Documents]

   Question:
   [User Query]

3. This prompt is sent to the OpenAI GPT model (or Google Gemini)
4. The generated response is returned as a JSON payload

This process ensures answers remain relevant, accurate, and aligned with the knowledge base.

---

### How did you schedule and implement background tasks for cleaning up old chat history, and how often do these tasks run?

Background tasks are implemented using APScheduler.

- A scheduled job runs automatically when the Django app starts
- The task deletes chat messages older than 30 days using Django ORM queries
- The scheduler runs once every 24 hours

This approach avoids the need for external workers like Celery while still ensuring automated database maintenance.

---

### What testing strategies did you use to ensure the functionality of the chatbot, authentication, and background tasks?

Multiple testing strategies were used:

- API testing using Postman and cURL
- Manual verification of authentication flows (login, token refresh, protected endpoints)
- Django shell testing for:
  - RAG retrieval accuracy
  - FAISS similarity search results
  - Background task execution logic

These tests ensured correctness across API behavior, authentication, and scheduled jobs.

---

### What external services (APIs, databases, search engines) did you integrate, and how did you set up and configure them?

External integrations include:

- OpenAI API (or Google Gemini) for language model inference
- FAISS as a local vector similarity search engine
- SQLite as the default database

All API keys and sensitive configurations are managed using environment variables loaded via `python-dotenv`.

---

### How would you expand this chatbot to support more advanced features, such as real-time knowledge base updates or multi-user chat sessions?

Future enhancements could include:

- Real-time knowledge base updates by re-indexing documents dynamically
- Multi-session chat support by adding a `session_id` field to chat messages
- WebSocket-based real-time streaming using Django Channels
- Persistent vector storage for large-scale document collections
- Role-based access control and admin analytics dashboards

These improvements would make the chatbot more scalable and production-ready.
