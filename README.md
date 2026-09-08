# API Documentation for Frontend Team

This project exposes a FastAPI backend with authentication and chat endpoints.

Base URL:
- Local development: http://127.0.0.1:8000
- Or: http://localhost:8000

Authentication:
- Use JWT Bearer token for protected endpoints.
- Include this header:
  Authorization: Bearer <access_token>

---

## 1) Health Check

### GET /
Returns a simple server status response.

Request:
- No body
- No auth required

Response example:
```json
{
  "message": "API is running"
}
```

---

## 2) Authentication

### POST /auth/register
Create a new user account.

Method: POST
Auth: Not required

Request body:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "your_password"
}
```

Success response: 201 Created
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

Possible error:
- 400 Bad Request if username or email already exists

---

### POST /auth/login
Login to get an access token.

Method: POST
Auth: Not required

Request body:
```json
{
  "username": "john_doe",
  "password": "your_password"
}
```

Success response: 200 OK
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Possible error:
- 401 Unauthorized for invalid username or password

Use the returned access_token in the Authorization header for protected routes.

---

## 3) Chat Endpoints

### GET /chat/sessions
Get all chat sessions for the authenticated user.

Method: GET
Auth: Required

Headers:
```http
Authorization: Bearer <access_token>
```

Success response: 200 OK
```json
[
  {
    "id": 1,
    "thread_id": "thread_123",
    "title": "My first chat",
    "created_at": "2026-09-02T10:30:00"
  },
  {
    "id": 2,
    "thread_id": "thread_456",
    "title": "Another conversation",
    "created_at": "2026-09-02T11:00:00"
  }
]
```

Purpose:
- Used to populate the chat history/sidebar on the frontend.

Possible error:
- 401 Unauthorized if token is missing or invalid

---

### POST /chat
Send a message to the AI agent in an existing chat thread.

Method: POST
Auth: Required

Headers:
```http
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "question": "What is the weather in Lahore?",
  "thread_id": "thread_123"
}
```

Response:
- The response is returned by the agent service.
- It can vary based on the chat logic and AI tool output.

Example shape:
```json
{
  "response": "The weather in Lahore is sunny and 31°C.",
  "thread_id": "thread_123"
}
```

Possible error:
- 401 Unauthorized if token is missing or invalid

---

### POST /new/chat
Create a new chat session and start the conversation immediately.

Method: POST
Auth: Required

Headers:
```http
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "question": "Hello, start a new chat session."
}
```

Response:
- This endpoint creates a new chat session and sends the first question.
- The exact response depends on the chat service implementation.

Example shape:
```json
{
  "chat_id": "abc123",
  "message": "New chat created successfully"
}
```

Possible error:
- 401 Unauthorized if token is missing/invalid
- 201 Created on success

---

## 4) Frontend Usage Notes

### Login flow
1. Call POST /auth/register if the user is new.
2. Call POST /auth/login with username and password.
3. Save the returned access_token.
4. Add it to every protected request:
```http
Authorization: Bearer <access_token>
```

### Protected route behavior
These endpoints require authentication:
- GET /chat/sessions
- POST /chat
- POST /new/chat

### JSON examples
All request bodies are JSON.

Example header:
```http
Content-Type: application/json
Authorization: Bearer <access_token>
```

---

## 5) Quick cURL Examples

Register:
```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "your_password"
  }'
```

Login:
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "your_password"
  }'
```

Get chat sessions:
```bash
curl -X GET "http://127.0.0.1:8000/chat/sessions" \
  -H "Authorization: Bearer <access_token>"
```

Chat:
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "question": "What is the weather in Lahore?",
    "thread_id": "thread_123"
  }'
```

New chat:
```bash
curl -X POST "http://127.0.0.1:8000/new/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "question": "Hello, start a new chat session."
  }'
```

---

## 6) Summary Table

| Method | Endpoint | Auth Required | Purpose |
|---|---|---:|---|
| GET | / | No | Health check |
| POST | /auth/register | No | Register user |
| POST | /auth/login | No | Login and get token |
| GET | /chat/sessions | Yes | Fetch all chat sessions |
| POST | /chat | Yes | Send message in chat thread |
| POST | /new/chat | Yes | Create new chat session |

This is the current API contract for frontend integration.
