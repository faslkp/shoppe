# Shoppe

A Django e-commerce application that serves a storefront, order workflow, and a lightweight REST API for companion clients. It uses Django REST Framework with JWT authentication, custom user profiles, and an admin dashboard tailored for catalog and order management.

## Key Capabilities
- Browsable storefront with product detail pages, cart, and checkout flows.
- Custom user model with registration, login, and address management.
- Order management with status tracking, per-user history, and admin fulfillment views.
- Public API endpoints for user sign-up and product browsing, plus authenticated order listings via JWT.
- Centralized rotating log files for request activity, errors, and database debugging.

## Requirements
- Python 3.12+
- SQLite (default) or any Django-supported database
- Node is not required; all assets are served via Django static files

All Python dependencies are listed in `requirements.txt`.

## Getting Started
1. **Clone & create environment**
   ```bash
   git clone <repo-url>
   cd shoppe
   python -m venv venv
   venv\Scripts\activate  # or source venv/bin/activate on Unix
   ```
2. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Configure environment**
   - Set values into environment variables (`SECRET_KEY`, `DEBUG`, database credentials).
4. **Run migrations & seed data**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py loaddata <fixture>  # optional if you add fixtures
   ```
5. **Start the server**
   ```bash
   python manage.py runserver
   ```
   The storefront lives at `/`, Django admin at `/admin/`, and API routes under `/api/`.

## API 
- `POST /api/register/` – open registration endpoint that mirrors the web form validation.
- `GET /api/products/` – anonymous product listing with average rating annotations.
- `GET /api/orders/` – authenticated endpoint returning the requester’s orders; supports session or JWT auth.
