# Facial Recognition Check-in Robot

## Overview

This project implements a facial recognition check-in robot designed to streamline attendance tracking. The system
consists of four main components:

1. **Robot End:** Captures images and can be controlled remotely via the management backend.
2. **Management Frontend:** Displays the robot's latest image uploads, facial recognition results, user attendance
   records, and statistics.
3. **User Frontend:** Allows users to register, log in, update personal information, and enroll their facial data.
4. **Server:** Handles image uploads, processes facial detection, and manages user data through RESTful APIs.

## Technologies Used

- **FastAPI:** A modern web framework for building APIs with Python.
- **SQLite:** A lightweight database for storing user and attendance records.
- **SQLAlchemy:** ORM for database operations.
- **Pydantic:** Data validation and settings management using Python type annotations.

## Project Structure

```
project/
├── main.py
├── models.py
├── schemas.py
├── database.py
├── facial_recognition.py
```

## Database Design

### Users Table

| Column Name | Data Type | Constraints                 |
|-------------|-----------|-----------------------------|
| id          | INT       | PRIMARY KEY, AUTO_INCREMENT |
| username    | VARCHAR   | UNIQUE, NOT NULL            |
| password    | VARCHAR   | NOT NULL                    |
| face_image  | BLOB      | NOT NULL                    |
| nickname    | VARCHAR   |                             |
| exp         | INT       |                             |
| email       | VARCHAR   |                             |

### Records Table

| Column Name | Data Type | Constraints                 |
|-------------|-----------|-----------------------------|
| id          | INT       | PRIMARY KEY, AUTO_INCREMENT |
| username    | VARCHAR   |                             |
| timestamp   | DATETIME  | DEFAULT CURRENT_TIMESTAMP   |

## API Documentation

### Base URL

```
http://127.0.0.1:8000
```

### Endpoints

#### 1. Upload Image

- **POST** `/image/`
- **Description:** Upload an image captured by the robot for facial detection.
- **Request Body:**
    - Content-Type: `multipart/form-data`
    - File: A single image file (JPEG/PNG).
- **Response:**
    - Status: `200 OK`
    - Body: `{ "message": "Image uploaded successfully." }`

#### 2. Get Detection Result

- **GET** `/detection_result/`
- **Description:** Retrieve the most recent facial detection results and the annotated image.
- **Response:**
    - Status: `200 OK`
    - Body:
      ```json
      {
        "annotated_image": "base64_encoded_image",
        "username": "string?"
      }
      ```

#### 3. User Information

- **GET** `/user/{username}/`
- **Description:** Retrieve user information by username.
- **Response:**
    - Status: `200 OK`
    - Body:
      ```json
      {
        "face_image": "base64_encoded_image",
        "username": "string",
        "password": "string",
        "nickname": "string?",
        "exp": "number?",
        "email": "string?"
      }
      ```

- **POST** `/user/`
- **Description:** Create a new user.
- **Request Body:**
    ```json
    {
      "face_image": "base64_encoded_image",
      "username": "string",
      "password": "string",
      "nickname": "string?",
      "exp": "number?",
      "email": "string?"
    }
    ```
- **Response:**
    - Status: `201 Created`
    - Body: `{ "message": "User created successfully." }`

- **PUT** `/user/{username}/`
- **Description:** Update user information.
- **Request Body:**
    ```json
    {
      "face_image": "base64_encoded_image",
      "password": "string",
      "nickname": "string?",
      "exp": "number?",
      "email": "string?"
    }
    ```
- **Response:**
    - Status: `200 OK`
    - Body: `{ "message": "User updated successfully." }`

- **DELETE** `/user/{username}/`
- **Description:** Delete a user by username.
- **Response:**
    - Status: `204 No Content`

#### 4. List All Users

- **GET** `/user/`
- **Description:** Retrieve a list of all users.
- **Response:**
    - Status: `200 OK`
    - Body:
      ```json
      [
        {
          "username": "string", 
          "nickname": "string?",
          "exp": "number?",
          "email": "string?"
        }
      ]
      ```

#### 5. Control Robot

- **POST** `/control/`
- **Description:** Send control signals to the robot.
- **Request Body:**
    ```json
    {
      "command": "string"
    }
    ```
- **Response:**
    - Status: `200 OK`
    - Body: `{ "message": "Command sent to robot." }`

- **GET** `/control/`
- **Description:** Retrieve the latest robot control command.
- **Response:**
    - Status: `200 OK`
    - Body: `{ "command": "string" }`

#### 6. Check-in Records

- **GET** `/records/`
- **Description:** Retrieve check-in records.
- **Response:**
    - Status: `200 OK`
    - Body:
      ```json
      [
        {
          "username": "string",
          "timestamp": "string"
        }
      ]
      ```

## Usage Instructions

1. **Installation:**
    - Clone the repository:
      ```bash
      git clone <repository-url>
      cd project
      ```
    - Install the required packages:
      ```bash
      pip install fastapi uvicorn sqlalchemy
      ```

2. **Run the Server:**
    - Start the application using Uvicorn:
      ```bash
      uvicorn main:app --reload
      ```
    - Access the API documentation at `http://127.0.0.1:8000/docs`.

3. **Interacting with the API:**
    - Use tools like Postman or CURL to test the endpoints. The API is designed to handle various operations related to
      user management, image uploads, and robot control.