# Advanced Library Management System

A modern library management system built with Django, featuring real-time notifications, location-based services, and advanced book management capabilities.

## Features

- User authentication with JWT
- Library and book management
- Real-time notifications using WebSockets
- Location-based library search
- Email notifications for book borrowing
- Asynchronous task processing with Celery
- RESTful API architecture

## Tech Stack

- Django 5.0
- Django REST Framework
- PostgreSQL with PostGIS
- Django Channels
- Celery with Redis
- JWT Authentication
- Docker

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Git

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd library-management
```

2. Create a `.env` file in the root directory with the following variables:
```
DEBUG=1
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=library_management.settings
DATABASE_URL=postgres://postgres:postgres@db:5432/library_db
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

The application will be available at:
- Main application: http://localhost:8000
- API documentation: http://localhost:8000/api/docs/
- Mailhog (email testing): http://localhost:8025

## Development

- The project uses Docker for development
- Celery worker and beat run in separate containers for task processing
- PostGIS is used for location-based queries
- WebSocket support is configured for real-time notifications
- Redis is used as message broker for Celery and Channels

## Task Processing

The system uses Celery for handling asynchronous tasks:
- Email notifications
- Scheduled tasks (daily reminders)
- Background processing
- Task monitoring and management

## API Documentation

API documentation will be available at `/api/docs/` once the server is running.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License. 
