# ShopSphere E-Commerce Application

ShopSphere is a highly polished, production-ready e-commerce web application built using Python 3, Django 5, PostgreSQL, and Bootstrap 5. It integrates Stripe, Razorpay, and Cash on Delivery payment mechanisms, dynamic carts (session-based for guests and database-linked for users), review systems, email notifications, a custom admin dashboard, and REST API support.

---

## Technical Stack
- **Core Engine**: Python 3.14.0, Django 5.2.15
- **Database**: PostgreSQL 18.4
- **Styling & UI**: Bootstrap 5, Bootstrap Icons, Vanilla CSS
- **REST APIs**: Django REST Framework (DRF)
- **Integrations**: Stripe SDK, Razorpay SDK, Pillow (media uploads)
- **Invoices**: ReportLab (commercial PDF generator)
- **Testing**: Pytest & pytest-django

---

## Features

### 1. Authentication System
- Email-based user sign-up, verification flow, password resets, and changes.
- Custom CustomUser model replacing Django's default username-only authentication.

### 2. Products Catalog
- Multi-tier Category mapping (sub-categories).
- Product variations (Size, Color, etc.) supporting custom pricing overrides.
- Search indexes, price range filter panels, sorting filters (latest, lowest price, highest price, highest rated).

### 3. Shopping Cart & Wishlist
- Persists items in local sessions for guest browsers.
- Automatically merges session items with database cart upon user login.
- Wishlist system for bookmarking and moving products to cart in one-click.

### 4. Checkout & Order Flow
- Address management (multiple shipping/billing locations).
- Coupon codes discount application (percentage or flat currency discount).
- Flat shipping charges and 5% taxes calculation.
- Cancel or Return orders from profile tracking details.

### 5. Payment Gateways
- Cash on Delivery (COD) processing.
- Stripe API session checkouts (includes simulation mode for developers).
- Razorpay UPI & netbanking gateway integration (with mock success callback).

### 6. Custom Admin Dashboard
- Analytical graphs of monthly revenue and sold shares.
- Out of stock and low stock alert trackers.
- Complete customer registry, orders directory, and product lists.

### 7. REST APIs
- ViewSets exposing: `/api/categories/`, `/api/products/`, `/api/reviews/`, `/api/cart/`, `/api/wishlist/`, `/api/orders/`.
- Auth endpoints: `/accounts/api/register/`, `/accounts/api/login/`.

---

## Installation & Setup

### 1. PostgreSQL Database Configuration
Start your PostgreSQL server and create a database named `shopsphere`:
```sql
CREATE DATABASE shopsphere;
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in the values:
```bash
Copy-Item .env.example .env
```
Ensure your database password matches your Postgres configuration (default is set to `12345`).

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Admin User Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py shell -c "from accounts.models import CustomUser; CustomUser.objects.create_superuser('admin', 'admin@shopsphere.com', 'adminpassword')"
```

### 5. Start Development Server
```bash
python manage.py runserver
```
Visit the website at `http://127.0.0.1:8000/`. You can log in using user email `admin@shopsphere.com` and password `adminpassword` to access the admin portal at `/dashboard/`.

---

## Running Test Suite
Execute the pytest suite using:
```bash
python -m pytest
```
All tests verify model constraints, pricing calculations, default address handling, and slugify systems.
