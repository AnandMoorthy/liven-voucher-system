# Liven Voucher App

This Django app allows you to manage Liven vouchers and their associated restaurant details.

## Setup Instructions

### Prerequisites

- Python (>=3.10)
- pip
- virtualenv

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/AnandMoorthy/liven-voucher-system.git
    cd liven-voucher-system
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser to access the Django admin panel:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Open your browser and navigate to [http://localhost:8000/admin/](http://localhost:8000/admin/) to log in with the superuser credentials.

### Django Admin

You can manage vouchers and restaurants through the Django admin panel:

- [http://localhost:8000/admin/](http://localhost:8000/admin/)