# Vehicle Inventory & Booking REST API

## Overview

A REST API built using Django and Django REST Framework to manage vehicle inventory and customer bookings. The application supports vehicle CRUD operations, booking creation, date validation, automatic rental price calculation, vehicle availability checks, and vehicle filtering.

## Technologies Used

- Python
- Django
- Django REST Framework
- django-filter
- SQLite
- Postman

## Features

- Create, retrieve, update, and delete vehicles.
- Create and retrieve customer bookings.
- Validate booking dates and customer phone numbers.
- Automatically calculate rental costs based on rental duration and daily price.
- Prevent overlapping bookings for the same vehicle.
- Filter vehicles by brand, fuel type, and availability.
- Check vehicle availability for a requested date range.

## Project Structure

```text
vehicle_management_system/
├── env/                       # Local virtual environment
├── vehicle_system/
│   ├── inventory/
│   ├── vehicle_system/
│   ├── db.sqlite3
│   └── manage.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```



## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd vehicle_management_system
```

Replace the repository URL and folder name with the actual values if they differ.

### 2. Create a Virtual Environment

```bash
python -m venv env
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\env\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source env/bin/activate
```

### 4. Install Dependencies

Run this command from the main `vehicle_management_system/` directory:

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file using `.env.example` as a reference. Configure the Django secret key, debug setting, and allowed hosts as appropriate for the environment.

Do not commit the actual `.env` file or production secrets to GitHub.

### 6. Navigate to the Django Project Directory

```bash
cd vehicle_system
```

This directory contains `manage.py`.

### 7. Apply Database Migrations

```bash
python manage.py migrate
```

If model changes have not yet been migrated, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Start the Development Server

```bash
python manage.py runserver
```

The local API will be available at:

`http://127.0.0.1:8000/`

## API Endpoints

### Vehicles

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/vehicles/` | List vehicles |
| POST | `/api/vehicles/` | Create a vehicle |
| GET | `/api/vehicles/<id>/` | Retrieve vehicle details |
| PUT | `/api/vehicles/<id>/` | Update a vehicle |
| PATCH | `/api/vehicles/<id>/` | Partially update a vehicle |
| DELETE | `/api/vehicles/<id>/` | Delete a vehicle |

### Bookings

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/bookings/` | List bookings |
| POST | `/api/bookings/` | Create a booking |
| GET | `/api/bookings/<id>/` | Retrieve booking details |

## Vehicle Filtering

Filter vehicles using query parameters:

- By brand: `/api/vehicles/?brand=Toyota`
- By fuel type: `/api/vehicles/?fuel_type=Electric`
- By availability: `/api/vehicles/?is_available=true`

To search for vehicles available for a specific date range:

`/api/vehicles/?start_date=2026-11-10&end_date=2026-11-12`

Both `start_date` and `end_date` must be provided in `YYYY-MM-DD` format.

## Sample Booking Request

**Method:** `POST`

**Endpoint:** `/api/bookings/`

**Request Body:**

```json
{
  "vehicle": 1,
  "customer_name": "Ameen",
  "customer_phone": "9876543210",
  "start_date": "2026-11-05",
  "end_date": "2026-11-08"
}
```

The backend calculates the total rental amount using the rental duration and the selected vehicle's daily rental price.

## Booking Validations

- The start date cannot be in the past.
- The end date must be after the start date.
- The customer phone number must contain exactly 10 digits.
- Overlapping bookings for the same vehicle are rejected.
- The total rental amount is calculated by the backend.
- Vehicle availability is checked against the requested rental dates.

## Testing

Use Postman to test vehicle CRUD operations, booking creation, date-range filtering, and validation scenarios.



## Project Links

- **GitHub Repository:** https://github.com/Fathima-noor/Vehicle-Management-System
  
Live API: https://vehicle-management-system-3sk9.onrender.com/api/

Vehicles API: https://vehicle-management-system-3sk9.onrender.com/api/vehicles/

Bookings API: https://vehicle-management-system-3sk9.onrender.com/api/bookings/


