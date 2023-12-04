# vms

Vendor Management System

# Django API Project README

This Django project provides an API for managing Purchase Orders (PO).

## Setup Instructions

### Prerequisites

- Python (>=3.8)
- Django (>=4.2)
- Django REST Framework (>=3.11)

### Installation

1. Clone the repository:

    ```cmd
    git clone https://github.com/iamsubu8/vms.git
    ```

2. Navigate to the project directory:

    ```cmd
    cd vms_project
    ```

3. Install dependencies:

    ```cmd
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```cmd
    python manage.py migrate
    ```

5. Create a superuser for admin access:

    ```cmd
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```cmd
    python manage.py runserver
    ```

The API should now be accessible at `http://127.0.0.1:8000/`.

## API Endpoints
Obtain JWT Token:
    Endpoint: /token/obtain/
    Description: Used to obtain a JSON Web Token (JWT) for authentication.

Refresh JWT Token:
    Endpoint: /token/refresh/
    Description: Used to refresh an existing JWT to extend the validity.

User Login:
    Endpoint: /login
    Description: Custom user login endpoint.
    Method: POST

Create Vendor:
    Endpoint: /api/vendors
    Description: Used to create a new vendor.
    Method: POST

GET Vendors:
    Endpoint: /api/vendors
    Description: Retrieve a list of vendor.
    Method: GET

Get, Update, or Delete Vendor:
    Endpoint: /api/vendors/<int:vendor_id>
    Description: Perform operations (GET, PUT, DELETE) on a specific vendor.
    Methods: GET, PUT, DELETE

Create PO:
    Endpoint: /api/purchase_orders
    Description: Used create PO.
    Method: POST

Get PO:
    Endpoint: /api/purchase_orders
    Description: Retrieve a list of purchase orders.
    Method: GET
    Perform Operations on a Specific Purchase Order:

Endpoint: /api/purchase_orders/<int:po_id>
    Description: Perform operations (GET, PUT, DELETE) on a specific purchase order.
    Methods: GET, PUT, DELETE
x
Endpoint: /api/statusupdate/<int:po_id>
    Description: Update the status of a specific purchase order.
    Method: POST

Endpoint: /api/purchase_orders/<int:po_id>/acknowledge
    Description: Acknowledge the receipt or processing of a specific purchase order.
    Method: POST

Endpoint: /api/vendors/<int:vendor_id>/performance
    Description: Evaluate the performance of a specific vendor.
    Method: GET