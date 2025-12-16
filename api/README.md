# Django RAG Chatbot API

## 1. Project Overview
This project is a **Backend REST API** built with **Django** and **LangChain** that serves as an intelligent chatbot engine. It does not rely on a simple LLM response; instead, it implements a **Retrieval-Augmented Generation (RAG)** pipeline to answer user queries based on a specific, private knowledge base.

Designed as a headless service, this API features secure **JWT Authentication**, persistent **Chat History**, and automated database maintenance, making it ready for integration with any frontend client (Web, Mobile, etc.).

### **Key Features**
* **RAG Pipeline:** Utilizes **FAISS** vector search to retrieve relevant context from local documents (`faq.txt`) before generating answers.
* **API-First Design:** Fully decoupled architecture using **Django Rest Framework (DRF)**.
* **Secure Auth:** Stateless authentication via **JSON Web Tokens (JWT)**.
* **Automated Maintenance:** A background scheduler (APScheduler) runs every 24 hours to delete old chat logs.

---

## 2. Technologies Used

* **Core Framework:** Django 5.x, Django Rest Framework
* **Authentication:** SimpleJWT
* **AI & NLP:** LangChain, OpenAI API (or Google Gemini), FAISS (Vector Store)
* **Task Scheduling:** APScheduler
* **Database:** SQLite (Development default)
* **Environment:** Python 3.10+, python-dotenv

---

## 3. Architecture & Implementation (Q&A)

### **How did you integrate the RAG pipeline for the chatbot, and what role does document retrieval play in the response generation?**
I integrated the RAG pipeline using **LangChain**. When an API request is received, the system first uses **FAISS** to scan the `faq.txt` knowledge base and retrieve the most relevant text chunks. These chunks are injected into the LLM's prompt as "context." This ensures the API provides answers rooted specifically in our domain data, rather than general knowledge.

### **What database and model structure did you use for storing user and chat history, and why did you choose this approach?**
I used **SQLite** for the database to ensure portability and ease of setup. The data model consists of a `ChatMessage` table linked to Django's built-in `User` model via a ForeignKey.
* **Why this approach?** Using a relational database allows for structured, ACID-compliant storage of conversation logs. Linking messages to `User` IDs ensures data isolation and easy retrieval of history for authenticated clients.

### **How did you implement user authentication using JWT? What security measures did you take?**
Authentication is handled via `djangorestframework-simplejwt`.
1.  **Flow:** Clients exchange credentials (`username`/`password`) for an `access` token (short-lived) and `refresh` token.
2.  **Security:** All chat endpoints are protected by the `IsAuthenticated` permission class. The API is stateless; no session data is stored on the server, and passwords are hashed securely using Django's default crypto modules.

### **How does the chatbot generate responses using the AI model after retrieving documents?**
The generation process is a two-step chain:
1.  **Retrieval:** The user's query is converted to a vector embedding to find matching documents in FAISS.
2.  **Generation:** A prompt is constructed: *"Answer based on this context: [Retrieval]... Question: [Query]"*. This is sent to the LLM (GPT or Gemini), and the returned text is serialized into a JSON response.

### **How did you schedule and implement background tasks for cleaning up old chat history?**
I implemented background tasks using **APScheduler** in `api/tasks.py`.
* **Logic:** A function `delete_old_chats()` runs a standard Django ORM query to delete records where `created_at < 30 days ago`.
* **Scheduling:** The scheduler is initialized in the `api/apps.py` `ready()` method, ensuring it starts automatically alongside the Django server without needing a separate worker process (e.g., Celery).

### **What testing strategies did you use to ensure the functionality of the chatbot?**
1.  **API Testing:** I used **Postman** (and/or cURL) to verify all endpoints, ensuring correct JSON structure and HTTP status codes (200 for success, 401 for unauthorized).
2.  **Logic Verification:** Used the **Django Shell** to manually test the RAG retrieval function and verify that the scheduler was correctly identifying old records.

### **What external services (APIs, databases, search engines) did you integrate?**
* **LLM Provider:** Integrated the **OpenAI API** (or Google Gemini) for the core intelligence.
* **Vector Engine:** Integrated **FAISS** as a local, in-memory search engine to handle document retrieval without needing an external database service like Pinecone.
* **Configuration:** All service keys are managed via environment variables (`.env`) to maintain security.

### **How would you expand this chatbot to support more advanced features?**
* **Real-time Streaming:** I would implement **Django Channels** (WebSockets) to stream the AI's response token-by-token to the client, reducing perceived latency.
* **Multi-user Sessions:** I would extend the `ChatMessage` model to include a `session_id` field. This would allow a single user to maintain multiple distinct conversation threads (e.g., "Support Ticket #1", "General Query") simultaneously.

---

## 4. API Documentation

**Base URL:** `http://127.0.0.1:8000/api/`

### **Authentication**
#### **1. Register**
* **URL:** `POST /signup/`
* **Body:** `{"username": "user1", "password": "password123"}`
* **Response:** `201 Created`

#### **2. Login**
* **URL:** `POST /api/login/`
* **Body:** `{"username": "user1", "password": "password123"}`
* **Response:**
  ```json
  {
      "refresh": "eyJ0eX...",
      "access": "eyJ0eX..."
  }

Chat Endpoints (Requires Bearer Token)
3. Send Message
URL: POST /chat/

Header: Authorization: Bearer <access_token>

Body: {"message": "How do I reset my password?"}

Response:

JSON

{
    "response": "To reset your password, go to settings..."
}
4. Get History
URL: GET /chat-history/

Header: Authorization: Bearer <access_token>

Response: JSON list of past conversations.

5. Setup Instructions
Prerequisites
Python 3.10 or higher.

An API Key (OpenAI or Google Gemini).

Installation
Clone the Repository:

Bash

git clone <repository-url>
cd <project-folder>
Create Virtual Environment:

Bash

# Windows
python -m venv env
.\env\Scripts\activate
Install Dependencies:

Bash

pip install -r requirements.txt
Configure Environment: Create a .env file in the root directory:

Code snippet

# Add your API Key here
OPENAI_API_KEY=sk-... 
# OR if using Google:
GOOGLE_API_KEY=AIza...
Knowledge Base Setup: Ensure you have a folder knowledge_base with a file named faq.txt containing your source data.

Run Migrations:

Bash

python manage.py makemigrations
python manage.py migrate
Start Server:

Bash

python manage.py runserver
Appendix: requirements.txt
Ensure these packages are installed:

Plaintext

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