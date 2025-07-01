# Employee Feedback Management System - Backend

A robust, production-ready FastAPI backend for managing employee feedback workflows with role-based access control, real-time notifications, and comprehensive analytics.

## 🚀 Overview

This backend service provides a complete API for employee feedback management, featuring secure authentication, role-based permissions, and a comprehensive feedback lifecycle from request to acknowledgment. Built with modern Python technologies and designed for scalability and maintainability.

### Key Features

- **🔐 Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **👥 Role-Based Access Control**: Separate permissions for managers and employees
- **📝 Feedback Management**: Complete CRUD operations for feedback with sentiment analysis
- **🔔 Request System**: Employee-initiated feedback requests with status tracking
- **📊 Analytics**: Real-time dashboard data and performance insights
- **🗄️ Database Management**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **📚 API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **🔍 Health Monitoring**: Built-in health checks and error handling
- **🌐 CORS Support**: Configurable cross-origin resource sharing
- **🚀 Production Ready**: Environment-based configuration and deployment support

## 🛠️ Technology Stack

### Core Framework
- **FastAPI 0.104+**: Modern, fast web framework for building APIs
- **Python 3.8+**: Latest Python features and performance improvements
- **Uvicorn**: Lightning-fast ASGI server

### Database & ORM
- **PostgreSQL 12+**: Robust relational database
- **SQLAlchemy 2.0+**: Modern Python SQL toolkit and ORM
- **Alembic**: Database migration tool
- **Psycopg2**: PostgreSQL adapter for Python

### Authentication & Security
- **Python-JOSE**: JWT token handling
- **Passlib**: Password hashing with bcrypt
- **Cryptography**: Secure cryptographic operations

### Development & Testing
- **Pytest**: Testing framework with async support
- **Pydantic**: Data validation and settings management
- **Python-dotenv**: Environment variable management

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd feedback-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration

```bash
# Create PostgreSQL database
createdb feedback_db

# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
DATABASE_URL=postgresql://username:password@localhost:5432/feedback_db
SECRET_KEY=your-super-secret-key-here
```

### 3. Database Initialization

```bash
# Initialize database tables
python setup_db.py

# Or run migrations (if using Alembic)
alembic upgrade head
```

### 4. Start Development Server

```bash
# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use the startup script
python start.py
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
feedback-backend/
├── app/
│   ├── __init__.py
│   ├── auth.py              # Authentication utilities
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection setup
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic data models
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── users.py         # User management endpoints
│       └── feedback.py      # Feedback and request endpoints
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── main.py                  # FastAPI application entry point
├── start.py                 # Production startup script
├── setup_db.py             # Database initialization
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .env.production         # Production environment template
├── Dockerfile              # Docker configuration
├── railway.json            # Railway deployment config
├── render.yaml             # Render deployment config
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/feedback_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
ENVIRONMENT=development
DEBUG=true

# CORS Settings (for production)
FRONTEND_URL=https://your-frontend-domain.com
```

### Production Configuration

For production deployment, use these additional settings:

```env
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=super-secure-random-key
FRONTEND_URL=https://your-production-frontend.com
```

## 🗄️ Database Models

### User Model
```python
class User(Base):
    id: int (Primary Key)
    email: str (Unique)
    full_name: str
    hashed_password: str
    role: UserRole (MANAGER | EMPLOYEE)
    manager_id: int (Foreign Key, nullable)
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

### Feedback Model
```python
class Feedback(Base):
    id: int (Primary Key)
    manager_id: int (Foreign Key)
    employee_id: int (Foreign Key)
    strengths: str
    areas_to_improve: str
    overall_sentiment: SentimentType (POSITIVE | NEUTRAL | NEGATIVE)
    acknowledged: bool
    acknowledged_at: datetime (nullable)
    created_at: datetime
    updated_at: datetime
```

### FeedbackRequest Model
```python
class FeedbackRequest(Base):
    id: int (Primary Key)
    employee_id: int (Foreign Key)
    manager_id: int (Foreign Key)
    message: str (nullable)
    status: str (pending | completed | cancelled)
    created_at: datetime
    completed_at: datetime (nullable)
```

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/login` - User authentication
- `POST /api/auth/register` - User registration

### User Management
- `GET /api/users/me` - Get current user profile
- `GET /api/users/team` - Get team members (managers only)
- `GET /api/users/managers` - Get all managers

### Feedback Operations
- `GET /api/feedback/` - List feedback (role-based filtering)
- `POST /api/feedback/` - Create feedback (managers only)
- `PUT /api/feedback/{id}` - Update feedback (managers only)
- `POST /api/feedback/{id}/acknowledge` - Acknowledge feedback (employees only)
- `GET /api/feedback/dashboard` - Get dashboard analytics

### Feedback Requests
- `POST /api/feedback/request` - Create feedback request (employees only)
- `GET /api/feedback/requests` - List feedback requests (role-based)
- `POST /api/feedback/requests/{id}/complete` - Mark request complete (managers only)
- `DELETE /api/feedback/requests/{id}` - Cancel request

### System
- `GET /` - API information
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

## 🔒 Security Features

### Authentication
- JWT tokens with configurable expiration
- Secure password hashing using bcrypt
- Token-based session management

### Authorization
- Role-based access control (RBAC)
- Endpoint-level permission checks
- Resource ownership validation

### Data Protection
- Input validation using Pydantic
- SQL injection prevention via SQLAlchemy
- CORS configuration for cross-origin requests
- Environment-based secret management

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Test configuration and fixtures
├── test_auth.py            # Authentication tests
├── test_users.py           # User management tests
├── test_feedback.py        # Feedback operation tests
└── test_requests.py        # Feedback request tests
```

## 🚀 Deployment

### Railway (Recommended)

1. **Connect Repository**: Link your GitHub repository to Railway
2. **Add PostgreSQL**: Add a PostgreSQL database service
3. **Set Environment Variables**: Configure production environment variables
4. **Deploy**: Railway automatically builds and deploys

### Render

1. **Create Web Service**: Connect your GitHub repository
2. **Configure Build**: Set build and start commands
3. **Add Database**: Create PostgreSQL database
4. **Set Environment Variables**: Configure production settings

### Docker

```bash
# Build image
docker build -t feedback-backend .

# Run container
docker run -p 8000:8000 --env-file .env feedback-backend
```

### Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="your-database-url"
export SECRET_KEY="your-secret-key"

# Start production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📊 Monitoring & Logging

### Health Checks
- `/health` endpoint for service monitoring
- Database connection validation
- Application status reporting

### Logging
- Structured logging with appropriate levels
- Request/response logging for debugging
- Error tracking and reporting

### Performance
- Database query optimization
- Connection pooling
- Async request handling

## 🔧 Development

### Code Style
- Follow PEP 8 Python style guide
- Use type hints for better code documentation
- Implement comprehensive error handling

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Adding New Features

1. **Create Models**: Add database models in `app/models.py`
2. **Define Schemas**: Create Pydantic schemas in `app/schemas.py`
3. **Implement Routes**: Add API endpoints in appropriate router
4. **Add Tests**: Write comprehensive tests for new functionality
5. **Update Documentation**: Update API documentation and README

## 🐛 Troubleshooting

### Common Issues

**Database Connection Errors**:
```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Verify database exists
psql -l

# Test connection
psql postgresql://username:password@localhost:5432/feedback_db
```

**Import Errors**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Authentication Issues**:
- Verify `SECRET_KEY` is set and consistent
- Check token expiration settings
- Validate user credentials in database

### Debug Mode

```bash
# Enable debug logging
export DEBUG=true

# Run with detailed output
uvicorn main:app --reload --log-level debug
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI team for the excellent framework
- SQLAlchemy team for the powerful ORM
- PostgreSQL community for the robust database
- Python community for the amazing ecosystem
