# Matcha - Dating Website

A modern dating website built with **Clean Architecture** principles, following the 42 School subject requirements. This project implements a full-stack dating platform with real-time features, geolocation-based matching, and comprehensive user management.

## 🚀 Quick Start

```bash
# Setup development environment
./dev.sh setup

# Start all services
./dev.sh start

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 📋 Requirements

- **Docker & Docker Compose** - For containerized development
- **Node.js 18+** - For frontend development
- **Python 3.11+** - For backend development
- **UV** - Python package manager (installed in container)

## 🏗️ Architecture

### Clean Architecture + DDD

The project follows **Clean Architecture** with **Domain-Driven Design**:

```
src/
├── core/           # Domain Layer (Business Logic)
│   ├── entities/   # Business entities
│   ├── value_objects/ # Domain value objects
│   └── repositories/ # Abstract interfaces
├── application/    # Application Layer (Use Cases)
│   ├── use_cases/  # Business workflows
│   ├── dto/        # Data Transfer Objects
│   └── interfaces/ # Application interfaces
├── infrastructure/ # Infrastructure Layer (External)
│   ├── database/   # Database implementations
│   ├── external/   # External services
│   └── cache/      # Cache implementations
└── presentation/   # Presentation Layer (API)
    ├── api/        # REST endpoints
    ├── schemas/    # Request/Response models
    └── websocket/  # WebSocket handlers
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async web framework
- **UV** - Ultra-fast Python package manager
- **SQLAlchemy 2.0** - Async ORM
- **Pydantic v2** - Data validation and serialization
- **PostgreSQL 15** - Relational database
- **Redis 7** - Cache and sessions
- **Alembic** - Database migrations
- **WebSocket** - Real-time communication
- **JWT** - Authentication
- **Cloudinary** - Image storage

### Frontend
- **React 18** - UI framework
- **TypeScript** - Static typing
- **Vite** - Ultra-fast build tool
- **Tailwind CSS** - Utility-first CSS
- **Zustand** - Lightweight state management
- **React Query** - API cache management
- **Socket.io** - WebSocket client
- **React Hook Form** - Form management
- **Leaflet.js** - Interactive maps

### Development Tools
- **pytest** - Backend testing
- **Vitest** - Frontend testing
- **Black** - Python formatting
- **ESLint** - JS/TS linting
- **Pre-commit hooks** - Code quality
- **Docker** - Containerization

## 🎯 Features

### Core Features (Subject Requirements)
- ✅ **User Registration & Authentication** - Email verification, password reset
- ✅ **User Profiles** - Complete profile management with pictures
- ✅ **Matching System** - Like/Pass system with mutual matching
- ✅ **Geolocation** - Location-based matching and distance calculation
- ✅ **Real-time Chat** - WebSocket-based messaging
- ✅ **Notifications** - Real-time notifications for matches, messages
- ✅ **Profile Browsing** - Advanced search and filtering
- ✅ **Fame Rating** - Dynamic user rating system
- ✅ **Security** - XSS protection, SQL injection prevention

### Bonus Features
- 🎯 **Social Authentication** - Google/Facebook login
- 🗺️ **Interactive Maps** - Leaflet.js integration
- 📱 **Real-time Features** - Live notifications and chat
- 🎨 **Modern UI/UX** - Responsive design with Tailwind CSS
- 🔄 **Background Tasks** - Celery for async processing

## 🚀 Development

### Environment Setup
```bash
# Clone and setup
git clone <repository>
cd matcha
./dev.sh setup
```

### Development Workflow
```bash
# Start all services
./dev.sh start

# View logs
./dev.sh logs

# Run tests
./dev.sh test

# Code quality checks
./dev.sh lint
./dev.sh format

# Database operations
./dev.sh migrate
./dev.sh reset-db
```

### Manual Development
```bash
# Backend only (with DB/Redis)
./dev.sh backend
cd backend && uv run uvicorn src.main:app --reload

# Frontend only
cd frontend && npm run dev
```

## 🧪 Testing

### Backend Testing
```bash
# All backend tests
./dev.sh test-backend

# Specific test file
cd backend && uv run pytest tests/unit/core/test_entities.py

# Quick entity validation
cd backend && uv run python test_entities.py

# With coverage
cd backend && uv run pytest --cov=src
```

### Frontend Testing
```bash
# All frontend tests
./dev.sh test-frontend

# Specific test
cd frontend && npm test -- --run specific.test.ts

# Coverage
cd frontend && npm run test:coverage
```

## 📊 Database

### Migrations
```bash
# Run migrations
./dev.sh migrate

# Create new migration
cd backend && uv run alembic revision --autogenerate -m "description"

# Reset database
./dev.sh reset-db
```

### Database Schema
- **Users** - Authentication and basic info
- **Profiles** - User profiles with interests, pictures
- **Matches** - Like/match relationships
- **Messages** - Chat messages and conversations
- **Notifications** - System notifications
- **Locations** - Geolocation data

## 🔐 Security

- **Password Hashing** - bcrypt
- **JWT Authentication** - Secure token-based auth
- **XSS Protection** - Input sanitization
- **SQL Injection Prevention** - Parameterized queries
- **CORS Configuration** - Secure cross-origin requests
- **Rate Limiting** - API endpoint protection

## 🐳 Docker Services

```yaml
services:
  db:          # PostgreSQL 15
  redis:       # Redis 7
  backend:     # FastAPI application
  frontend:    # React + Vite
```

## 📝 Environment Variables

Copy example files and configure:
```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env
```

Key variables:
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `SECRET_KEY` - JWT secret
- `CLOUDINARY_*` - Image storage config

## 🤝 Contributing

1. Follow Clean Architecture principles
2. Use conventional commits
3. Run tests before committing
4. Use pre-commit hooks
5. Update documentation

## 📄 License

This project is part of the 42 School curriculum.

## 🎯 Subject Score Target

**Target: 125/125** (including bonus features)

### Mandatory (100/100)
- User registration and authentication
- Profile management
- Matching system
- Real-time chat
- Notifications
- Advanced search
- Security implementation

### Bonus (25/25)
- Omniauth integration
- Interactive maps
- Enhanced real-time features
- Modern UI/UX
- Additional security measures