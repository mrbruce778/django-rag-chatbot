## Design & Implementation Questions

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
