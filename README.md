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
- **Persistence:** PostgreSQL with **SQLAlchemy 2.0** ORM.
- **Migrations:** Authoritative schema history via **Alembic**.
- **Authentication:** Email/password login with access & refresh tokens.
- **Session Control:** Refresh token rotation, single-session logout, and global logout.
- **RBAC Foundation:** Roles modeled at the database level and embedded into JWT claims.
- **Infrastructure:** Redis integrated for caching and future async workflows.

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

## 🚀 Running Locally

### Prerequisites
- Docker
- Docker Compose

### 1. Initialize Environment

Copy the example environment file and update values as needed:

Bash

```
cp .env.example .env 

```
### 2. Start the Stack

Build and launch the containers:

Bash

```
docker compose up -d --build

```
### 3. Access the API

Once the stack is running, the API is available locally with interactive documentation:

- **Swagger UI:** http://localhost:8000/docs  
- **ReDoc:** http://localhost:8000/redoc  

These interfaces can be used to explore endpoints, inspect schemas, and manually test authentication flows.

---

## 🔐 Authentication Scope

The authentication system is designed as a **standalone service**:

- **Email-based Identity:** Users are uniquely identified by email.
- **Security:** Industry-standard password hashing and verification.
- **Stateless Access:** JWT-based access tokens with refresh token rotation.
- **Session Control:** Per-session revocation and global logout support.
- **RBAC:** Role-based access enforced at the service layer and reflected in tokens.

---

## 🧭 Roadmap

- [x] Dockerized Base Infrastructure  
- [x] Database & Migration Setup  
- [x] Email/Password Signup & Login  
- [x] JWT Access Tokens & Refresh Token Rotation  
- [x] Session Revocation (Single & Global Logout)  
- [ ] Fine-grained Permissions on top of RBAC  
- [ ] Background Job Integration (Celery / Redis)  
- [ ] Notification Service Infrastructure  
- [ ] Admin / System Management APIs  

---

## 🤝 Open to Collaboration

**forge-backend** is an evolving infrastructure project, and collaboration is welcome.

If you are interested in:
- Backend architecture
- Authentication & authorization systems
- Distributed systems foundations
- Infra-first backend design

feel free to open issues, propose improvements, or submit pull requests.  
Thoughtful contributions, design discussions, and code reviews are encouraged.

Additionally, contributors interested in building a **React-based dashboard**
(e.g. admin or consumer UI) that acts as a client of forge-backend are
welcome. The frontend is intentionally scoped as a separate project to maintain
clear service boundaries, not to limit collaboration.

This is a learning-driven project. If you’re curious about backend systems,
auth infrastructure, or full-stack architecture and want to build and learn
together, contributions and discussions are very welcome.


## 📄 License

This project is licensed under the MIT License.

