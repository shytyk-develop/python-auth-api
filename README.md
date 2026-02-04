# FastAPI Auth API

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.128.0-009688)
![License](https://img.shields.io/badge/license-MIT-blue)
![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-336791)
![Async](https://img.shields.io/badge/async-SQLAlchemy-orange)

A production-ready FastAPI authentication API with comprehensive documentation, security features, and database migrations.

## 📑 Quick Navigation

- [What's Included](#whats-included) - Core features and security
- [🚀 Quick Start](#-quick-start) - Get up and running in 5 minutes
- [📊 API Endpoints](#-api-endpoints) - All available endpoints
- [🔐 Security Features](#-security-features) - Authentication & admin system
- [📧 Email Configuration](#email-configuration) - SMTP setup
- [🗄️ Database Migrations](#️-database-migrations) - Alembic guide
- [📁 Project Structure](#-project-structure) - File organization
- [🔗 Resources](#-related-resources) - Official documentation links

## What's Included

### Core Features
- **User Authentication**: Secure registration and login with JWT tokens
- **Admin System**: Role-based access control for newsletter and user management
- **User Management**: Profile updates, password changes, account deletion
- **Newsletter System**: Admin-only bulk email sending to subscribers
- **Rate Limiting**: Endpoint-specific rate limits to prevent abuse
- **Database Migrations**: Alembic integration for schema versioning

### Security
- ✅ Bcrypt password hashing (v4.0.1)
- ✅ JWT authentication with HS256
- ✅ Admin credentials from environment variables
- ✅ Rate limiting on critical endpoints (3/min for auth)
- ✅ CORS headers configuration
- ✅ HttpOnly, Secure cookies for tokens
- ✅ Password verification for sensitive operations

### Technology Stack
- **Framework**: FastAPI 0.128.0 with uvloop for high performance
- **Database**: PostgreSQL with SQLAlchemy 2.0+ async ORM
- **Migrations**: Alembic for schema versioning
- **Authentication**: PyJWT + Bcrypt
- **Email**: aiosmtplib for async SMTP
- **Rate Limiting**: slowapi
- **Validation**: Pydantic v2 with email-validator

## 📁 Project Structure

```
fastapi-login-api/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependency injection (auth, admin)
│   │   └── routers/
│   │       ├── auth.py          # Login/register endpoints
│   │       ├── users.py         # User management endpoints
│   │       └── newsletter.py    # Admin-only newsletter
│   ├── core/
│   │   ├── config.py            # Settings from .env
│   │   ├── email.py             # SMTP email sending
│   │   ├── security.py          # Password & JWT utilities
│   │   ├── logging.py           # Structured logging
│   │   └── rate_limit.py        # Rate limiting config
│   ├── db/
│   │   ├── base.py              # ORM base class
│   │   └── session.py           # Database connection
│   ├── models/
│   │   └── user.py              # User model with is_admin
│   ├── schemas/
│   │   ├── auth.py              # Request/response schemas
│   │   ├── user.py
│   │   └── newsletter.py
│   └── main.py                  # FastAPI app initialization
├── migrations/
│   ├── versions/                # Auto-generated migrations
│   └── env.py                   # Alembic configuration
├── init_db.py                   # Initialize database tables
├── migrate_add_admin.py          # Add is_admin column migration
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── README.md                    # Comprehensive documentation
├── MIGRATIONS.md                # Migration guide
├── LICENSE                      # MIT license
└── .gitignore                   # Git exclusions
```

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone <repository-url>
cd fastapi-login-api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings:
# - DATABASE_URL: PostgreSQL connection string
# - JWT_SECRET_KEY: Random secure key
# - ADMIN_USERNAME/PASSWORD: Admin credentials
# - SMTP settings: For email sending (optional)
```

### 3. Database Setup
```bash
# Initialize tables
python init_db.py

# Or apply Alembic migrations
alembic upgrade head
```

### 4. Run the Server
```bash
uvicorn app.main:app --reload
```

Access API documentation at `http://localhost:8000/docs`

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - Register new user (3/min rate limit)
- `POST /auth/login` - Login and get JWT token (3/min rate limit)
- `POST /auth/logout` - Logout (3/min rate limit)

### User Management
- `PATCH /users/me/password` - Change password (protected, 5/min)
- `PATCH /users/me/username` - Change username (protected, 5/min)
- `PATCH /users/me/subscription` - Toggle newsletter subscription (5/min)
- `DELETE /users/me` - Delete account (protected, 5/min)

### Newsletter (Admin Only)
- `POST /newsletter/send` - Send email to all subscribers (10/min)

## 🔐 Security Features

### Admin System
- Admin credentials stored in `.env` (not in database)
- Admin login checks environment variables at login time
- Admin users cannot modify their own credentials via API
- Admin flag synced to database for efficient queries
- Support for multiple admin users sharing credentials

### Password Security
- Bcrypt hashing with automatic salt generation
- Min 8 characters, complexity validation
- Separate password verification for admin login
- Password changes require admin verification

### JWT Tokens
- Algorithm: HS256
- Expiration: 1440 minutes (24 hours)
- Storage: HttpOnly, Secure, SameSite cookies
- Validation on every protected endpoint

## Email Configuration

### For Gmail:
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Set in `.env`:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

### For Other Providers:
Update `SMTP_HOST` and `SMTP_PORT` accordingly

## 🗄️ Database Migrations

### View Status
```bash
alembic current      # Current revision
alembic history      # All migrations
```

### Create New Migration
```bash
# Modify your model in app/models/user.py
alembic revision --autogenerate -m "Add new field"
alembic upgrade head
```

### Rollback
```bash
alembic downgrade -1     # One step back
alembic downgrade head~3 # Three steps back
```

## Testing API

### Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"SecurePass123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"SecurePass123"}'
```

### Send Newsletter (Admin)
```bash
curl -X POST http://localhost:8000/newsletter/send \
  -H "Content-Type: application/json" \
  -H "Cookie: access_token=<TOKEN>" \
  -d '{"subject":"Hello","message":"Newsletter content"}'
```

## Key Files to Understand

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app setup, middleware, rate limiting |
| `app/core/config.py` | Environment configuration management |
| `app/core/security.py` | Password hashing and JWT utilities |
| `app/core/email.py` | Async SMTP email sending |
| `app/api/deps.py` | Authentication dependencies |
| `app/api/routers/auth.py` | Login logic with admin support |
| `app/models/user.py` | User database model with is_admin field |
| `migrations/env.py` | Alembic configuration with async handling |

## 📚 Documentation

- [README.md](README.md) - This file
- [LICENSE](LICENSE) - MIT license

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Related Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Guide](https://docs.sqlalchemy.org/en/20/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [JWT Authentication](https://jwt.io/)
- [OWASP Security](https://owasp.org/)

---

**Project Version**: 1.0.0  
**Last Updated**: February 4, 2025  
