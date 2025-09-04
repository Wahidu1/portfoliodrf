# 🚀 Portfolio Backend API

> **A modern Django REST Framework backend with Redis integration for my personal portfolio**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-red.svg)](https://www.django-rest-framework.org/)
[![Redis](https://img.shields.io/badge/Redis-7.0+-red.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This is the **backend API** for my personal portfolio website. Built with modern technologies and best practices, it provides a robust foundation for portfolio management, contact handling, and content delivery.

## ✨ Features

- 🎯 **RESTful API** with Django REST Framework
- ⚡ **Redis Caching** for improved performance
- 📧 **Email Integration** for contact forms
- 🔐 **Authentication & Authorization**
- 📊 **Admin Dashboard** for content management
- 🐳 **Docker Support** for easy deployment
- 🔍 **API Documentation** with Swagger/OpenAPI
- ✅ **Comprehensive Testing Suite**

---

## 🛠️ Tech Stack

| Technology | Purpose | Version |
|-----------|---------|---------|
| [Django](https://www.djangoproject.com/) | Web Framework | 4.2+ |
| [Django REST Framework](https://www.django-rest-framework.org/) | API Development | 3.14+ |
| [Redis](https://redis.io/) | Caching & Background Tasks | 7.0+ |
| [Celery](https://celery.dev/) | Async Task Queue | 5.3+ |
| [PostgreSQL](https://www.postgresql.org/) | Database (Production) | 13+ |
| [SQLite](https://www.sqlite.org/) | Database (Development) | 3.39+ |
| [Docker](https://www.docker.com/) | Containerization | Latest |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Redis Server
- Git

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Wahidu1/portfolio-backend.git
cd portfolio-backend
```

### 2️⃣ Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Environment Configuration

Create a `.env` file in the project root:

```ini
# Django Settings
DEBUG=True
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Database
DATABASE_URL=sqlite:///db.sqlite3
# For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost:5432/portfolio_db

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis Configuration
REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# Security (Production)
SECURE_SSL_REDIRECT=False
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

### 5️⃣ Start Redis Server

**Option A: Using Docker**
```bash
docker run -d --name redis-server -p 6379:6379 redis:alpine
```

**Option B: Local Installation**
```bash
# On macOS
brew install redis
brew services start redis

# On Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server

# On Windows (using WSL or download from Redis website)
```

### 6️⃣ Database Setup

```bash
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 7️⃣ Start Development Server

```bash
# Start Django development server
python manage.py runserver

# In another terminal, start Celery worker (for async tasks)
celery -A portfolio_backend worker --loglevel=info

# Optional: Start Celery Beat (for scheduled tasks)
celery -A portfolio_backend beat --loglevel=info
```

🎉 **Your API is now running at:** `http://127.0.0.1:8000/`

---

## 📁 Project Structure

```
portfolio-backend/
├── 📁 apps/                    # Django applications
│   ├── 📁 projects/           # Projects management
│   ├── 📁 skills/             # Skills & technologies
│   ├── 📁 experience/         # Work experience
│   ├── 📁 contact/            # Contact form handling
│   └── 📁 core/               # Core utilities
├── 📁 portfolio_backend/       # Main Django project
│   ├── 📄 settings.py         # Django settings
│   ├── 📄 urls.py             # URL configuration
│   ├── 📄 wsgi.py             # WSGI configuration
│   └── 📄 celery.py           # Celery configuration
├── 📁 static/                 # Static files
├── 📁 media/                  # Media files
├── 📁 templates/              # Email templates
├── 📁 tests/                  # Test files
├── 📁 fixtures/               # Sample data
├── 📄 requirements.txt        # Python dependencies
├── 📄 docker-compose.yml      # Docker configuration
├── 📄 Dockerfile             # Docker image
├── 📄 .env.example           # Environment variables template
└── 📄 README.md              # This file
```

---

## 🔗 API Endpoints

### 📊 Core Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/` | API root & documentation | ❌ |
| `GET` | `/api/docs/` | Swagger UI documentation | ❌ |
| `GET` | `/admin/` | Django admin panel | ✅ |

### 🎯 Portfolio Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/projects/` | List all projects | ❌ |
| `GET` | `/api/projects/{id}/` | Get project details | ❌ |
| `POST` | `/api/projects/` | Create new project | ✅ |
| `PUT` | `/api/projects/{id}/` | Update project | ✅ |
| `DELETE` | `/api/projects/{id}/` | Delete project | ✅ |

### 🛠️ Skills Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/skills/` | List all skills | ❌ |
| `GET` | `/api/skills/categories/` | List skill categories | ❌ |
| `POST` | `/api/skills/` | Add new skill | ✅ |

### 💼 Experience Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/experience/` | List work experience | ❌ |
| `POST` | `/api/experience/` | Add experience | ✅ |

### 📧 Contact Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/contact/` | Send contact message | ❌ |
| `GET` | `/api/contact/messages/` | List messages (admin) | ✅ |

---

## 🐳 Docker Deployment

### Development with Docker Compose

```yaml
version: "3.9"

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - redis
      - db
    env_file:
      - .env

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: portfolio_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  celery:
    build: .
    command: celery -A portfolio_backend worker --loglevel=info
    volumes:
      - .:/app
    depends_on:
      - redis
      - db
    env_file:
      - .env

volumes:
  postgres_data:
  redis_data:
```

### Start Services

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report

# Run specific test
python manage.py test apps.projects.tests.test_models

# Run tests in parallel
python manage.py test --parallel
```

---

## 🔧 Configuration

### Redis Configuration

```python
# settings.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Celery Configuration
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```

### CORS Configuration

```python
# For frontend integration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://yourportfolio.com",
]
```

---

## 📝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Wahid**
- 🌐 Portfolio: [yourportfolio.com](https://yourportfolio.com)
- 💼 LinkedIn: [linkedin.com/in/wahid](https://linkedin.com/in/wahid)
- 🐙 GitHub: [@Wahidu1](https://github.com/Wahidu1)
- 📧 Email: your.email@example.com

---

## 🙏 Acknowledgments

- Django & DRF communities for excellent documentation
- Redis team for blazing-fast caching
- All open-source contributors who made this possible

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

Made with ❤️ by **Wahid**

</div>
