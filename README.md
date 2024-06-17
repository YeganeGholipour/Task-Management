# Task Management API Server

### This project is a Task Management API server built with Django and Docker, utilizing PostgreSQL as the database. It allows users to manage projects, tasks within those projects, add comments to tasks, receive daily reports of tasks, and reminders for tasks due within the next 24 hours.
## Features

    1. Projects Management: CRUD operations for projects.
    2. Tasks Management: CRUD operations for tasks within projects.
    3. Comments: Add comments to individual tasks.
    4. Daily Reports: Receive reports of tasks completed or due.
    5. Email Notifications: Receive reminders for tasks due within the next 24 hours.

## Technologies Used

    * Django: Python web framework
    * PostgreSQL: Database management system
    * Docker: Containerization platform for easy deployment
    * Django REST Framework: Toolkit for building Web APIs
    * Celery: used for managing tasks
    * RabbitMQ: as the message broker for celery tasks
    * Redis: to enable in memory cache

## Installation

To run this project locally, make sure you have Docker installed on your system.

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```
2. Create a .env file in the root directory with the following environment variables:
   ```bash
   SECRET_KEY=your_secret_key
   DEBUG=True
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   DB_HOST=db
   DB_PORT=5432
   ```
3. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```
4. Apply migrations and create a superuser:
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```
5. To run celery, make sure to run these two commands in two different terminals:
   ```bash
   celery -A your_project worker --loglevel=info
   ```
## EndPoints
these are the list of endpoints available:
1. GET /projects/ - List all projects.
2. POST /projects/ - Create a new project.
3. GET /projects/<id>/ - Retrieve a single project by ID.
4. PUT /projects/<id>/ - Update a project by ID.
5. DELETE /projects/<id>/ - Delete a project by ID.
6. GET /tasks/ - List all tasks.
7. POST /tasks/ - Create a new task.
8. GET /tasks/<id>/ - Retrieve a single task by ID.
9. PUT /tasks/<id>/ - Update a task by ID.
10. DELETE /tasks/<id>/ - Delete a task by ID.
11. POST /tasks/<id>/comments/ - Add a comment to a task.
12. GET /tasks/<id>/comments/ - List all comments for a task.



