# Task Manager API

## Overview

This project is a test assignment for a Python backend web developer position. It implements a **REST API** for an advanced Task Manager application using **FastAPI**, **PostgreSQL**, and **SQLAlchemy** with async support. The API supports task management with role-based access control, integration with an external weather API, analytics, JWT authentication, rate limiting, and real-time notifications via WebSocket. The project is containerized using **Docker** and **Docker Compose** for easy setup and deployment.

---

## Task Description

The goal is to develop a REST API for a Task Manager application with the following features:

### Requirements
1. **Framework**: Use **FastAPI** for asynchronous request handling.
2. **Database**: Store data in **PostgreSQL** using **SQLAlchemy** with an async driver (`asyncpg`).
3. **CRUD Operations**: Implement asynchronous CRUD operations for tasks.
4. **Role-Based Access**:
   - Users with the `user` role can create and manage only their own tasks.
   - Users with the `admin` role can manage all tasks.
5. **External API Integration**: Fetch weather data (e.g., from OpenWeather API) when a task with a city is created.
6. **Analytics**: Provide task statistics by status and user for a specified time period.
7. **Pagination and Filtering**: Support filtering tasks by status, user, and creation date, with pagination and sorting.
8. **Authentication**: Implement **JWT-based authentication** for securing endpoints.
9. **Testing**: Write **unit tests** using `pytest` and `pytest-asyncio` with at least 80% code coverage.
10. **Containerization**: Package the application with **Docker** and **Docker Compose** (including PostgreSQL and optionally Redis).
11. **Logging**: Log all operations (create, update, delete) to a file and/or stdout.
12. **Rate Limiting**: Implement request rate limiting (e.g., using `fastapi-limiter` and Redis).
13. **Documentation**: Provide detailed API documentation (via FastAPI's Swagger UI and this README).

### Optional Features
- Cache weather API responses using Redis.
- Support file attachments for tasks (e.g., store in S3 or locally).
- Implement WebSocket for real-time task creation/update notifications.
- Set up a CI/CD pipeline (e.g., GitHub Actions) for automated testing and deployment.

### Data Models
- **User**:
  - `id`: Unique identifier (auto-increment).
  - `username`: Unique username (string).
  - `role`: Role (`user` or `admin`).
  - `password_hash`: Hashed password (string).
- **Task**:
  - `id`: Unique identifier (auto-increment).
  - `title`: Task title (string, required, max 100 characters).
  - `description`: Task description (string, optional).
  - `status`: Task status (`todo`, `in_progress`, `done`).
  - `created_at`: Creation timestamp (auto-set).
  - `city`: City for weather data (string, optional).
  - `weather`: Weather data at creation time (JSON, optional).
  - `user_id`: ID of the user who created the task (foreign key).

### API Endpoints
1. **POST /auth/register**: Register a new user.
2. **POST /auth/login**: Authenticate a user and return a JWT token.
3. **POST /tasks**: Create a new task (includes weather data if city is provided).
4. **GET /tasks**: List tasks with filtering (by status, user, date), pagination, and sorting.
5. **GET /tasks/{id}**: Retrieve a task by ID (accessible to task owner or admin).
6. **PUT /tasks/{id}**: Update a task (accessible to task owner or admin).
7. **DELETE /tasks/{id}**: Delete a task (accessible to task owner or admin).
8. **GET /analytics**: Retrieve task statistics by status and user for a given period.

### Example Requests
- **Create a Task**:
  ```bash
  curl -X POST "http://localhost:8000/tasks" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Prepare Report",
    "description": "Collect monthly data",
    "status": "todo",
    "city": "Moscow"
  }'
  ```
  **Response**:
  ```json
  {
    "id": 1,
    "title": "Prepare Report",
    "description": "Collect monthly data",
    "status": "todo",
    "city": "Moscow",
    "weather": {
      "temperature": 15.5,
      "condition": "Cloudy"
    },
    "user_id": 1,
    "created_at": "2025-05-24T14:35:00Z"
  }
  ```

- **Get Analytics**:
  ```bash
  curl -X GET "http://localhost:8000/analytics?start_date=2025-05-01&end_date=2025-05-24" \
  -H "Authorization: Bearer <JWT_TOKEN>"
  ```
  **Response**:
  ```json
  {
    "by_status": {
      "todo": 10,
      "in_progress": 5,
      "done": 3
    },
    "by_user": {
      "user1": 12,
      "user2": 6
    }
  }
  ```

---

## Setup Instructions

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- PostgreSQL (managed via Docker Compose)
- OpenWeather API key (sign up at [https://openweathermap.org/](https://openweathermap.org/))
- (Optional) Redis for rate limiting and caching

### Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd task-manager-api
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Required packages:
   - `fastapi`
   - `sqlalchemy[asyncio]`
   - `asyncpg`
   - `aiohttp`
   - `python-jose`
   - `pytest`
   - `pytest-asyncio`
   - `fastapi-limiter`
   - `python-dotenv`

3. **Set Environment Variables**:
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/task_manager
   OPENWEATHER_API_KEY=your-openweather-api-key
   SECRET_KEY=your-secret-key-for-jwt
   REDIS_URL=redis://localhost:6379
   ```

4. **Run Database Migrations**:
   Use Alembic to apply migrations:
   ```bash
   alembic upgrade head
   ```

5. **Start the Application with Docker**:
   ```bash
   docker-compose up --build
   ```
   This starts the FastAPI application, PostgreSQL, and (optionally) Redis.

6. **Access the API**:
   - API: `http://localhost:8000`
   - Swagger UI: `http://localhost:8000/docs`
   - Redoc: `http://localhost:8000/redoc`

### Running Tests
Run unit tests with coverage:
```bash
pytest --cov=app tests/
```

---

## Project Structure
```
task-manager-api/
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas for validation
│   ├── crud.py          # Database operations
│   ├── auth.py          # JWT authentication logic
│   ├── dependencies.py  # FastAPI dependencies (e.g., DB session, auth)
│   └── utils/
│       ├── weather.py   # Weather API integration
│       ├── logging.py   # Logging configuration
├── tests/
│   ├── test_auth.py     # Tests for authentication endpoints
│   ├── test_tasks.py    # Tests for task endpoints
│   ├── test_analytics.py # Tests for analytics endpoint
├── migrations/          # Alembic migrations
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── README.md            # This file
```

---

## Notes
- **Error Handling**: The API handles errors such as 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), and 429 (Too Many Requests).
- **Rate Limiting**: Configured to limit requests per user (e.g., 100 requests per minute).
- **Logging**: All operations are logged to `app.log` and stdout with timestamps and user details.
- **WebSocket**: Real-time notifications for task updates are available at `/ws` (optional feature).
- **Caching**: Weather data is cached in Redis for 1 hour to reduce external API calls (optional feature).

---

## Evaluation Criteria
- Correct implementation of all endpoints and integrations.
- Code quality (readability, modularity, adherence to async patterns).
- Test coverage (minimum 80%).
- Proper JWT authentication and role-based access control.
- Comprehensive documentation (this README and Swagger UI).
- Successful implementation of optional features (caching, WebSocket, CI/CD).

For any questions or clarifications, refer to the Swagger documentation at `http://localhost:8000/docs` or contact the project maintainer.

Happy coding!