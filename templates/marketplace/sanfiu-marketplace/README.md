# Sanfiu Marketplace

![Sanfiu Marketplace UI preview](preview.svg)

A multi-seller storefront with a seller application flow, admin review, seller-only product management, and per-item order fulfillment status. The admin panel is the marketplace operator's control center.

## Stack

- Python 3.10
- Django 5.2 LTS
- SQLite for the quickest local start, or PostgreSQL with Docker Compose
- Django templates and plain CSS

## Run locally

From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` and copy the environment file with `Copy-Item .env.example .env`.

Open `http://127.0.0.1:8000/` for the marketplace and `http://127.0.0.1:8000/admin/` for seller, catalog, and order administration. The demo sellers are disabled accounts used only to attach sample products. To exercise the seller portal, apply for a shop, approve it in admin, then sign in with the account you created.

For local PostgreSQL with Docker Compose, set a local password in `.env` and run `docker compose up --build`. Create an admin user with `docker compose exec web python manage.py createsuperuser`.

## Seller flow

1. A seller applies and creates a password-protected account.
2. The account stays in review until an admin approves or rejects it.
3. Approved sellers can add or edit only their own listings.
4. New or edited listings stay unpublished until an admin activates them.
5. Sellers can see and update fulfillment for order items tied to their own products.

## Before deploying

This starter records orders and inventory but does not process payment, calculate shipping or tax, issue refunds, send email, or pay out sellers. Seller order views expose the recipient's name, phone, and delivery address only for that seller's ordered products. Configure privacy notices, data retention, payment, shipping, and payout services for your business and jurisdiction. Docker Compose is for local development, not production. For a real marketplace, use PostgreSQL, a private `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, correct allowed hosts, HTTPS static hosting, rate limits for seller signup and login, and Django's deployment checklist. Never use the sample secrets in production.

The software in this kit is MIT licensed. Sample photographs and remote services have separate terms.
