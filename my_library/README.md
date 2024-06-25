# My Library

This library provides a Flask application integrated with OpenAI API for handling question-answer sessions with optional image uploads.

## Features
- Upload images and questions through a web interface.
- Integrates with OpenAI API for generating answers and related questions.
- Stores questions and answers in a MySQL database.

## Installation
1. Clone the repository.
2. Navigate to the project directory.
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the database configuration in `my_library/db.py`.
5. Run the application:
    ```bash
    python -m my_library.app
    ```

## Usage
Access the application in your browser at `http://127.0.0.1:5000`.
