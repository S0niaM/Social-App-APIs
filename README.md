# Social Media Backend API

This project is a social media backend api implemented using the Django REST framework. It includes features such as user authentication (login and signup), friend requests, and other social media functionalities.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Features](#features)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- - [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [Troubleshooting](#troubleshooting)
  

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.11.4
- MySQL 5.7+ or MySQL 8.0+
- MySQL client library (MySQL Workbench, Sequel Pro, or similar)
- Git (for cloning the repository)
- Virtualenv (for creating a virtual environment)

## Features

- User Authentication:
  - Signup
  - Login
- Friend Request Management:
  - Send Friend Request
  - Accept/Decline Friend Request
  - View Pending Friend Requests
- View existing friends
- Search other users


## Usage
Access the API at http://localhost:8000/api/
Use a tool like Postman or curl to interact with the API endpoints.
You can also access the Django admin panel at http://localhost:8000/admin/ using the superuser credentials.

## API endpoints
- User Signup
    http://127.0.0.1:8000/api/signup/
  
- User Login
    http://127.0.0.1:8000/api/login/
  
- Generation of Token
    http://127.0.0.1:8000/api/token/
  
- API to search other users by email and name
    http://127.0.0.1:8000/api/search/?q=a
    http://127.0.0.1:8000/api/search/?q=amit@gmail.com
  
- API to send/accept/reject friend request
    http://127.0.0.1:8000/api/friend-request/
  
- API to list friends(list of users who have accepted friend request)
    http://127.0.0.1:8000/api/friends/
  
- List pending friend requests
    http://127.0.0.1:8000/api/pending-requests/


## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install MySQL server and client:**

    - Follow the installation instructions for your operating system from the [MySQL Downloads](https://dev.mysql.com/downloads/) page.

## Configuration

1. **Create a `.env` file for environment variables:**

    ```bash
    touch .env
    ```

    Add the following to your `.env` file:

    ```env
    SECRET_KEY=your-secret-key
    DEBUG=True  # Set to False in production
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=3306
    ```

2. **Update `settings.py` to use environment variables:**

    Add the following code to the top of your `settings.py` file:

    ```python
    from pathlib import Path
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }
    ```

## Database Setup

1. **Create a MySQL database:**

    - Use your MySQL client to create a new database:

    ```sql
    CREATE DATABASE your_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```

2. **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```


3. **Test the connection:**

    Run the following command to ensure that everything is set up correctly:

    ```bash
    python manage.py check
    ```

## Running the Project

1. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

    You should be able to access your application at `http://127.0.0.1:8000/`.

2. **Access the Django Admin:**

    Navigate to `http://127.0.0.1:8000/admin` and log in using the superuser credentials.

## Troubleshooting

- **Common Issues:**
    - Ensure that your MySQL server is running.
    - Check that your database settings in `.env` match your MySQL configuration.
    - Verify that you have installed the MySQL client library (`mysqlclient`).





