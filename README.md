# Photographer Assignment System

A Django API to manage events and photographers, featuring an automated smart assignment system.

## Features

- Manage Events and Photographers (CRUD).
- **Smart Assignment**: Automatically match available photographers to events based on date and availability.
- View Photographer Schedules.

## Setup Instructions

### Local Setup (Without Docker)

1. **Configure Environment Variables**:
   Copy the example environment file and configure it:
   ```bash
   cp .env.example .env
   ```
   Modify `.env` if necessary (e.g., database credentials).

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  
   # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Create Superuser (for Admin Access)**:
   ```bash
   python manage.py createsuperuser
   ```
6. **Run Server**:
   ```bash
   python manage.py runserver
   ```

### Docker Setup (Recommended)

1. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   ```
     Edit the `.env` file as per your environment.

2. **Build and Run Containers**:
   ```bash
   docker-compose up --build -d
   ```
   The API will be available at `http://localhost:8000`.

3. **Run Migrations (if not verified automatically)**:
   ```bash
   docker-compose exec eg_backend python manage.py migrate
   ```

4. **Create Superuser**:
   ```bash
   docker-compose exec eg_backend python manage.py createsuperuser
   ```

5. **Run Tests**:
   ```bash
   docker-compose exec eg_backend python manage.py test events
   ```

6. **Stop Containers**:
   ```bash
   docker-compose down
   ```

## Admin Interface

- Access the Django Admin interface at: `http://localhost:8000/admin/`
- Login using the credentials created via the `createsuperuser` command.
- You can manage Events, Photographers, and Assignments directly from the admin dashboard.

## API Documentation

The base URL for all API endpoints is `http://localhost:8000/api/`.

### Events

- **List all events**
    - `GET /events/`
- **Create a new event**
    - `POST /events/`
    - Body:
      ```json
      {
        "event_name": "Wedding Shoot",
        "event_date": "2025-12-30",
        "photographers_required": 2
      }
      ```
- **Get event details**
    - `GET /events/<id>/`
- **Update event details**
    - `PUT /events/<id>/`
- **Delete an event**
    - `DELETE /events/<id>/`
- **Auto-assign photographers (Core Feature)**
    - `POST /events/<id>/assign-photographers/`
    - Logic: Validates requirements, checks photographer availability (active status + no date conflicts), and creates assignments.
    - Response (Success):
      ```json
      {
        "message": "Photographers assigned successfully",
        "assigned_photographers": [ ... ]
      }
      ```
    - Response (Error):
      ```json
      {
        "error": "Not enough available photographers",
        "required": 2,
        "available": 1
      }
      ```
- **View assigned photographers for an event**
    - `GET /events/<id>/assignments/`

### Photographers

- **List all photographers**
    - `GET /photographers/`
- **Create a new photographer**
    - `POST /photographers/`
    - Body:
      ```json
      {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "9876543210",
        "is_active": true
      }
      ```
- **Get photographer details**
    - `GET /photographers/<id>/`
- **Update photographer details**
    - `PUT /photographers/<id>/`
- **View photographer schedule**
    - `GET /photographers/<id>/schedule/`
    - Returns a list of events assigned to this photographer.

## Smart Assignment Logic

The assignment logic is handled in the `assign_photographers` view:

1. **Validation**: Checks if `photographers_required > 0`, event is not in past, and event doesn't already have assignments.
2. **Availability Check**:
   - Fetches all photographers with `is_active=True`.
   - Identifies photographers who already have an assignment on the same `event_date`.
   - Filters the active list to exclude those busy photographers.
3. **Assignment**:
   - Checks if the number of available photographers is sufficient.
   - If yes, creates `Assignment` records for the required number of photographers.
   - Uses database transactions to ensure data integrity.
4. **Error Handling**: Returns specific error messages if requirements aren't met (e.g., "Not enough available photographers").

## Running Tests

To run the automated tests for the assignment logic:

```bash
# Local
python manage.py test events

# Docker
docker-compose exec eg_backend python manage.py test events
```
