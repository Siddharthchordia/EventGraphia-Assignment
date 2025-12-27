# Photographer Assignment System

A Django API to manage events and photographers, featuring an automated smart assignment system.

## Features

- Manage Events and Photographers (CRUD).
- **Smart Assignment**: Automatically match available photographers to events based on date and availability.
- View Photographer Schedules.

## Setup Instructions

1. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  
   # On Windows: venv\Scripts\activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
4. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## API Documentation

### Events

- `GET /api/events/`: List all events.
- `POST /api/events/`: Create a new event.
   - Body: `{"event_name": "Wedding", "event_date": "2024-12-30", "photographers_required": 2}`
- `GET /api/events/<id>/`: Get event details.
- `PUT /api/events/<id>/`: Update event details.
- `DELETE /api/events/<id>/`: Delete an event.
- `POST /api/events/<id>/assign-photographers/`: **Auto-assign photographers.**
    - This endpoint implements the smart assignment logic.
    - It validates availability and conflicts before assigning.
- `GET /api/events/<id>/assignments/`: View assigned photographers for an event.

### Photographers

- `GET /api/photographers/`: List all photographers.
- `POST /api/photographers/`: Add a photographer.
   - Body: `{"name": "John Doe", "email": "john@example.com", "phone": "1234567890", "is_active": true}`
- `GET /api/photographers/<id>/`: Get details.
- `PUT /api/photographers/<id>/`: Update details.
- `GET /api/photographers/<id>/schedule/`: View all events assigned to a photographer.

## Smart Assignment Logic

The assignment logic is handled in the `assign_photographers` view:

1. **Validation**: Checks if `photographers_required > 0`, event is not in result, and event doesn't already have assignments.
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
python manage.py test events
```
