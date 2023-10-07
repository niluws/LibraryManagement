# Library Management System

This is an online library management system built using Django Rest Framework (DRF). It allows users to borrow and return books, view available books, and generate income reports. The system also includes features for managing customers, categories, and books.

## Features

- **Book Borrowing:** Users can borrow books, and the system tracks the number of books borrowed, return dates, and available stock.

- **Book Returning:** Users can return borrowed books, and the stock is updated accordingly.

- **Book Listing:** Managers can view the list of available books and filter them based on title, genre, type, and stock.

- **Book Posting:** Managers can add new books to the library.

- **Income Reporting:** Managers can generate income reports for different book categories, including income from book borrowings and book purchases.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/niluws/LibraryManagement.git
   cd LibraryManagement
   ```

2. Create a virtual environment and install the dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use "venv\Scripts\activate"
   ```

3. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

4. Create a superuser account for managing the system:

   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the admin panel at `http://localhost:8000/admin/` and log in with your superuser credentials to manage the system.

## Usage

1. Use the provided API endpoints to interact with the system.

2. Create book categories and add books to the library using the `/api/post-book/` endpoint.

3. Borrow books using the `/api/borrow-book/` endpoint.

4. Return books using the `/api/books/return/<int:id>/` endpoint.

5. View available books using the `/api/book/` endpoint.

6. Generate income reports using the `/api/income-report/` endpoint.

7. View books with advanced filtering options using the `/api/customer-book/` endpoint.

## Permissions

- Customers can borrow and return books.
- Managers can manage books, categories, and view income reports.

## Dependencies

- Django
- Django Rest Framework
- Django Filters
