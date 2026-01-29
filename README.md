# forge-backend

**forge-backend** is a modular, backend-first infrastructure platform built in Python, focused on providing reusable core services.

Unlike traditional frameworks that treat authentication as application logic, **forge-backend** treats it as infrastructure. The goal is to provide a production-grade foundation that can be deployed once and shared across multiple applications, eliminating the need to reimplement core primitives inconsistently.

---

## 🎯 Purpose

Every product reimplements authentication, authorization, and background processing—often inconsistently and insecurely. This repository provides a clean, extensible foundation for:

- **Authentication & Identity:** Centralized user management.
- **Roles & Permissions:** Granular access control (RBAC).
- **Background Jobs:** Reliable asynchronous task processing.
- **Notifications:** Multi-channel communication logic.
- **Shared Utilities:** Common backend primitives.

**forge-backend** is service-oriented, backend-only, and designed for horizontal scalability.

---

## 🧠 Design Philosophy

The project adheres to strict architectural principles:

- **Thin HTTP Layer:** FastAPI handles requests/responses; business logic stays in the Service Layer.
- **Auth as Infrastructure:** Identity is decoupled from frontend concerns and UI frameworks.
- **Explicit Database Schema:** Managed exclusively via **Alembic** migrations; no implicit changes.
- **Stateless by Default:** Designed for horizontal scalability and containerized deployment.
- **Production-First:** Environment-driven configuration, Dockerized, and built with testable components.

---

## 🧱 Current Capabilities

- **Runtime:** Dockerized development environment with Python 3.11.
- **Persistence:** PostgreSQL database managed via **SQLAlchemy 2.0**.
- **Migrations:** Full Alembic integration for authoritative schema history.
- **Identity:** Minimalist User model focused on auth surface area.
- **Logic:** Service-layer driven workflows with clean error boundaries.
- **Infrastructure:** Redis integrated for future caching and task queuing.

---

## 🛠 Tech Stack

| Component            | Technology              |
| :------------------- | :---------------------- |
| **Language**         | Python 3.11+            |
| **Web Framework**    | FastAPI                 |
| **ORM**              | SQLAlchemy 2.0          |
| **Migrations**       | Alembic                 |
| **Database**         | PostgreSQL              |
| **Cache/Queue**      | Redis                   |
| **Containerization** | Docker & Docker Compose |
| **Testing**          | pytest                  |

---

## 📦 Project Structure

The project is organized by responsibility rather than framework defaults:

```text
forge-backend/
├── app/
│   ├── api/            # Request/Response handling (Routes & Schemas)
│   ├── services/       # Core business logic and workflows
│   ├── models/         # Domain entities and invariants
│   ├── core/           # Config, security utilities, and constants
│   └── db/             # Session management and migrations
├── migrations/         # Alembic version history
├── tests/              # Pytest suite
├── docker-compose.yml
└── Dockerfile
```

Running Locally
Prerequisites
Docker

Docker Compose

1. Initialize Environment
   Copy the example environment file and update values as needed:

Bash

```
cp .env.example .env 2. Start the Stack
Build and launch the containers:

```

Bash

```
docker compose up -d --build 3. Access the API
Once running, the interactive documentation is available at:
```

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

🔐 Authentication Scope
The authentication system is designed to be a standalone service:
Email-based Identity: Primary identifier for users.
Security: Industry-standard password hashing (Argon2/Bcrypt) and verification.
Stateless: Planned JWT-based access control (no session coupling).
Extensible: Built to support RBAC and token rotation incrementally.

🧭 Roadmap

[x] Dockerized Base Infrastructure
[x] Database & Migration Setup
[x] Email/Password Signup & Login Flows
[x] JWT-based Access Tokens & Refresh Tokens
[ ] Role-Based Access Control (RBAC)
[ ] Background Job Integration (Celery/Redis)
[ ] Notification Service Infrastructure
