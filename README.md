# Student Book Rental System

A Django-based web application that allows students to rent books with controlled business logic and automated fee calculation.

## Business Rules

- First 30 days are free
- After 30 days, monthly fee = (book page count ÷ 100)
- Example: 300 pages → 3 per additional month
- Rental extensions automatically update due date and total fee

The system integrates with the OpenLibrary API to automatically fetch book metadata.

---

## Features

### Rental Management
- Create new rental
- First month free
- Extend rental by one month
- Automatic fee calculation
- Mark rental as returned
- Controlled admin interface

### Book Management
- Add book manually
- Enter only title → auto-fetch metadata from OpenLibrary
- Prevent duplicate book entries using `get_or_create`
- Dynamic monthly fee calculation

### API Endpoints (Django REST Framework)

| Method | Endpoint | Description |
|--------|----------|------------|
| POST | `/api/rent/` | Create rental |
| GET | `/api/rentals/` | List all rentals |
| POST | `/api/rentals/<id>/extend/` | Extend rental |

---

## Architecture Overview

### Models

### Book
- `title`
- `author`
- `page_count`
- `monthly_fee()` → returns page_count / 100

### Rental
- `user` (ForeignKey)
- `book` (ForeignKey)
- `start_date`
- `due_date`
- `total_fee`
- `returned`

Business logic is encapsulated inside model methods:
- `calculate_fee()`
- `extend_rental()`

---

## OpenLibrary API Integration

Books are fetched using:

https://openlibrary.org/search.json?title=BOOK_TITLE

The system extracts:
- `number_of_pages`
- `author_name`
- `title`

This ensures accurate rental cost calculation.

---

## Fee Calculation Logic

- Free period = 30 days
- Extra months = ceil((days_used - 30) / 30)
- Monthly fee = page_count / 100

Example:

- Book = 450 pages
- Monthly fee = 4.5
- 2 extra months → 9.0 total fee

## Installation Guide
### Clone Repository
- git clone <repository-url>
- cd student-book-rental-system
### Create Virtual Environment
- python -m venv venv
- venv\Scripts\activate
### Install Dependencies
- pip install -r requirements.txt
### Apply Migrations
- python manage.py makemigrations
- python manage.py migrate
### Create Superuser
- python manage.py createsuperuser
### Run Server
- python manage.py runserver


### Access:

Admin → http://127.0.0.1:8000/admin/

API → http://127.0.0.1:8000/api/


### Design Decisions

- Business logic encapsulated inside models
- Service layer for external API calls
- get_or_create used to prevent duplicate books

### Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- OpenLibrary API