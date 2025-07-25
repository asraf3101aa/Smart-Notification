# Smart Notification
A Django web application with PostgreSQL database and Celery for background task processing.

## Requirements

- Python 3.12
- PostgreSQL 12+
- Redis (for Celery broker)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/asraf3101aa/Smart-Notification
cd Smart-Notification
```

### 2. Create virtual environment

```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Environment variables configuration

Create a `.env` file in the project root and set environment variables:
| Variable | Description | Required |
|----------|-------------|---------|
| `APP_ENVIRONMENT` | Enable debug mode | False |
| `SECRET_KEY` | Django secret key | True |
| `DATABASE_URL` | PostgreSQL connection string | True |
| `CELERY_BROKER_URL` | Redis connection string | True |
| `WEEKLY_REPORT_DAY` | Day of week for weekly report | False |
| `WEEKLY_REPORT_HOUR` | Hour of the day for weekly report | False |
| `WEEKLY_REPORT_MINUTE` | Minutes of the day for weekly report | False |


### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create superuser (optional)

```bash
python manage.py createsuperuser
```

## Running the Application

### Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

### Celery Worker

In a separate terminal, start the Celery worker:

```bash
celery -A core worker --loglevel=info
```

### Celery Beat (Scheduler)

In another terminal, start the Celery beat scheduler:

```bash
celery -A core beat --loglevel=info
```

---

## API Documentation (cURL)

Below are cURL examples to interact with the API endpoints.

> Base URL: `http://127.0.0.1:8000`

---

### Account Endpoints (`/api/account/`)

#### Register a New User

```bash
curl -X POST http://127.0.0.1:8000/api/account/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword", "username":"yourusername"}'
```
#### Login

```bash
curl -X POST http://127.0.0.1:8000/api/account/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "yourusername", "password": "yourpassword", "device_id":"device-id-generate-from-frontend","device_name":"device-name-generate-from-frontend"}'
```

#### Refresh Token

```bash
curl -X POST http://127.0.0.1:8000/api/account/login/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'
```
#### Get User Info

```bash
curl -X GET http://127.0.0.1:8000/api/account/me/ \
  -H "Authorization: Bearer your_access_token"
```

#### Update User Info

```bash
curl -X PUT http://127.0.0.1:8000/api/account/me/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe"}'
```

#### Delete User Account

```bash
curl -X DELETE http://127.0.0.1:8000/api/account/me/ \
  -H "Authorization: Bearer your_access_token"
```
---
### Thread Endpoints (`/api/thread/`)


#### Create a New Thread

```bash
curl -X POST http://127.0.0.1:8000/api/thread/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Thread", "description": "Thread description"}'
```

#### Add Comment to a Thread

```bash
curl -X POST http://127.0.0.1:8000/api/thread/{thread_id}/comment/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a comment"}'
```
####  Subscribe to a Thread

```bash
curl -X POST http://127.0.0.1:8000/api/thread/{thread_id}/subscribe/ \
  -H "Authorization: Bearer your_access_token"
```
---
### Notification Endpoints (`/api/v1/notifications/`)


#### Set Notification Preferences

```bash
curl -X POST http://127.0.0.1:8000/api/v1/notifications/preferences/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"channel": "email", "notification_type":"new_comment","enabled": true}'
```
#### List Unread Notifications
```bash
curl -X GET http://127.0.0.1:8000/api/v1/notifications/unread/ \
  -H "Authorization: Bearer your_access_token"
```

#### Mark Notifications as Read

```bash
curl -X POST http://127.0.0.1:8000/api/v1/notifications/read/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"ids": [{list of thread ids to mark as read}]}'
```
#### List Notification History

```bash
curl -X GET http://127.0.0.1:8000/api/v1/notifications/history/ \
  -H "Authorization: Bearer your_access_token"
```
####  Trigger a Test Notification (Manual)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/notifications/trigger/ \
  -H "Authorization: Bearer your_access_token"
```