# Easy Recipe

API for managing recipes, ingredients, and cooking steps.

---

## Setup

### 1. Prerequisites

- Docker and Docker Compose
- Python 3.11+
- [Poetry](https://python-poetry.org/)

### 2. Environment Variables

Copy the `.env.example` file to `.env` and adjust the variables as needed:

```bash
cp .env.example .env
```

- `SECRET_KEY`: Django secret key.
- `DATABASE_URL`: PostgreSQL database connection URL.

### 3. Running with Docker

Run:

```bash
docker compose up --build
```

The application will be available at: http://localhost:8000/

### 4. Manual Installation (without Docker)

1. Install dependencies:

   ```bash
   poetry install
   ```

2. Activate the Poetry virtual environment:

   ```bash
   poetry env activate
   ```

3. Run migrations:

   ```bash
   python manage.py migrate
   ```

4. (Optional) Create a test user:

   ```bash
   python scripts/create_user_and_token.py
   ```

5. Start the server:

   ```bash
   python manage.py runserver
   ```

Access at: http://localhost:8000/

---

## API Documentation

The interactive documentation (Swagger UI) is available at:

- http://localhost:8000/api/schema/swagger-ui/

The OpenAPI schema can be accessed at:

- http://localhost:8000/api/schema/

---

## Authentication

The API uses Token authentication. To obtain a token, make a POST request to:

```
POST /api/token/
```

With the fields `username` and `password`.

By default, a test user is created:

- username: `testuser`
- password: `testpassword`

When you make a request to the `/api/token` route, the token to be used in PUT, PATCH, and DELETE requests will be returned. In the Authorize button, enter the token with the prefix 'Token'. Example: `Token e7ed6e4c79f877c1e5247221398f2e41ff65330b`

---

## Tests

To run the tests:

```bash
poetry run python manage.py test
```

---

If you need more details or usage examples, consult the Swagger documentation or the source code.
