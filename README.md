# Flask API with JWT Authentication

This repository contains a simple Flask API with JWT authentication for user registration, login, and CRUD operations on products.

## Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a `.env` file with necessary environment variables.
4. Initialize the database: `flask db init`, `flask db migrate`, `flask db upgrade`.
5. Run the Flask application: `flask run`.

## Models

The `models.py` file defines the database models for users and products.

- **User Model**: Represents users registered in the system with username and password.
- **Product Model**: Represents products with title, description, price, and a foreign key relationship to the user who created it.

## Routes

The `routes.py` file contains route definitions for the API endpoints.

- **User Registration**: POST request to `/register` with JSON payload containing `username` and `password`.
- **User Login**: POST request to `/login` with user credentials to receive an access token.
- **Product Operations**: CRUD operations on products available at `/products` and `/products/<product-id>`.

## Tests

The `tests.py` file contains unit tests for the API endpoints.

- **User Registration Test**: Tests user registration functionality.
- **User Login Test**: Tests user login functionality.
- **Product Creation Test**: Tests product creation with authentication.
- **Product Retrieval Test**: Tests retrieval of all products.
- **Product Update Test**: Tests updating product information.
- **Product Deletion Test**: Tests deletion of products.

Run tests with: `python -m unittest`.

## License

This project is licensed under the MIT License.
