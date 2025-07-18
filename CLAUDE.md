# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a dating website backend called "Matcha" implementing **Clean Architecture** with Domain-Driven Design principles. The project uses Python 3.11+ with FastAPI, Pydantic v2, SQLAlchemy 2.0, and follows async/await patterns throughout.

## Development Commands

### Quick Setup
```bash
# Setup complete development environment
./dev.sh setup

# Start all services (Docker Compose)
./dev.sh start

# Stop all services
./dev.sh stop
```

### Development Server
```bash
# Start only backend services (DB + Redis)
./dev.sh backend

# Start frontend development server
./dev.sh frontend

# Run backend manually (after ./dev.sh backend)
cd backend && uv run uvicorn src.main:app --reload

# Run frontend manually
cd frontend && npm run dev
```

### Testing
```bash
# Run all tests (backend + frontend)
./dev.sh test

# Run backend tests only
./dev.sh test-backend

# Run frontend tests only
./dev.sh test-frontend

# Run specific backend test
cd backend && uv run pytest tests/unit/core/test_entities.py

# Run quick entity validation
cd backend && uv run python test_entities.py
```

### Code Quality
```bash
# Lint all projects
./dev.sh lint

# Format all code
./dev.sh format

# Backend specific
cd backend && uv run ruff check src/
cd backend && uv run ruff format src/
cd backend && uv run mypy src/

# Frontend specific
cd frontend && npm run lint
cd frontend && npm run lint:fix
```

### Database
```bash
# Run migrations
./dev.sh migrate

# Reset database completely
./dev.sh reset-db

# Manual migration commands
cd backend && uv run alembic upgrade head
cd backend && uv run alembic revision --autogenerate -m "description"
```

### Docker & Services
```bash
# View logs
./dev.sh logs

# Clean up containers/volumes
./dev.sh clean

# Open backend shell
./dev.sh shell

# Manual Docker commands
docker-compose up -d
docker-compose down
docker-compose restart
```

## Architecture Overview

### Clean Architecture Layers

The codebase follows strict **Clean Architecture** with dependency inversion:

1. **Core Layer** (`src/core/`) - Pure business logic, no external dependencies
   - **Entities**: Rich domain models with business logic (`user.py`, `matching.py`, `chat.py`)
   - **Value Objects**: Immutable domain concepts (`email.py`, `location.py`, `age.py`, `fame_rating.py`)
   - **Repository Interfaces**: Abstract contracts for data access

2. **Application Layer** (`src/application/`) - Use cases and application services
   - **Use Cases**: Business workflows organized by domain (`auth/`, `matching/`, `chat/`, `profile/`)
   - **DTOs**: Data transfer objects for application boundaries
   - **Interfaces**: Application service contracts

3. **Infrastructure Layer** (`src/infrastructure/`) - External concerns
   - **Database**: SQLAlchemy models and repository implementations
   - **External Services**: Email, geolocation, social auth, storage (Cloudinary)
   - **Cache**: Redis implementation
   - **WebSocket**: Real-time communication

4. **Presentation Layer** (`src/presentation/`) - API and WebSocket endpoints
   - **API**: FastAPI REST endpoints in `/api/v1/`
   - **Schemas**: Pydantic request/response models
   - **Middleware**: Authentication, CORS, rate limiting
   - **WebSocket**: Real-time handlers

### Key Domain Concepts

- **User Management**: Registration, verification, profiles with fame rating system
- **Matching System**: Like/Super Like/Pass with mutual matching detection
- **Geolocation**: Distance-based matching using Haversine formula
- **Chat System**: Real-time messaging with status tracking
- **Fame Rating**: Dynamic 0-5.0 scale with levels (newcomer → legendary)

### Technology Stack

**Backend:**
- **Framework**: FastAPI + Uvicorn (async REST API)
- **Package Manager**: UV (ultra-fast dependency management)
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0 async
- **Cache**: Redis 7 for sessions and performance
- **Validation**: Pydantic v2 with modern type hints (`str | None`)
- **Migrations**: Alembic for database schema management
- **Real-time**: WebSocket + SocketIO for chat and notifications
- **Auth**: JWT with python-jose, bcrypt password hashing
- **External**: Cloudinary (images), Geopy (location), Celery (background tasks)

**Frontend:**
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite (ultra-fast development and build)
- **Styling**: Tailwind CSS (utility-first CSS framework)
- **State Management**: Zustand (lightweight state management)
- **API Client**: React Query (@tanstack/react-query) for cache/API management
- **Forms**: React Hook Form for form management
- **Real-time**: Socket.io-client for WebSocket communication
- **Maps**: Leaflet.js for interactive maps (bonus feature)
- **Animations**: Framer Motion for smooth animations

**Infrastructure:**
- **Containerization**: Docker + Docker Compose for development
- **Authentication**: JWT tokens
- **File Storage**: Cloudinary for image storage and processing
- **Maps**: Leaflet.js for interactive maps

**Development Tools:**
- **Backend Testing**: pytest with async support, coverage reporting
- **Frontend Testing**: Vitest with React Testing Library
- **Code Quality**: Ruff (Python linting/formatting), ESLint (JS/TS linting)
- **Pre-commit Hooks**: Automated code quality checks
- **Type Checking**: MyPy (Python), TypeScript (frontend)

## Development Patterns

### Pydantic Models
- Use `str | None` instead of `Optional[str]`
- Use `list[str]` instead of `List[str]`
- Use `@field_validator` instead of `@validator`
- Use `ConfigDict` instead of `class Config`

### Repository Pattern
- All data access goes through repository interfaces in `core/repositories/`
- Concrete implementations in `infrastructure/database/repositories/`
- Use dependency injection to provide implementations

### Testing Strategy
- **Unit Tests**: Test domain entities and value objects in isolation
- **Integration Tests**: Test repository implementations with database
- **E2E Tests**: Test complete API workflows
- Use `test_entities.py` for quick domain model validation

### Error Handling
- Domain exceptions in `core/exceptions/`
- Use appropriate HTTP status codes in presentation layer
- Validate inputs at domain boundaries

## Important Notes

- **Database Migrations**: Always use Alembic for schema changes
- **Async/Await**: All repository methods and use cases are async
- **Type Safety**: Full MyPy type checking enabled with strict mode
- **Clean Architecture**: Never import from outer layers to inner layers
- **Domain Logic**: Keep business rules in domain entities, not in use cases
- **Testing**: Write tests for all new domain entities and use cases
- **Code Quality**: Always run linting checks before committing (`ruff check` + `ruff format`)
- **Mandatory Testing**: Every feature/use case MUST have corresponding tests before implementation is considered complete

## Development Guidelines

- **Dependency Management**: 
  - Always use the venv activated and uv commands from https://docs.astral.sh/uv/ to interact with dependencies

## File Structure Context

- `test_entities.py` - Quick validation tests for domain models
- `pyproject.toml` - Project dependencies and tool configuration
- `src/core/` - Domain layer with entities, value objects, and interfaces
- `src/application/use_cases/` - Business workflows organized by domain
- `src/infrastructure/` - External integrations and concrete implementations
- `src/presentation/` - API endpoints and WebSocket handlers