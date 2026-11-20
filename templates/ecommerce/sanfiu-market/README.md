# Sanfiu Market

A customizable full-stack starter for a small online store. It includes a responsive storefront, product catalog, session-based shopping bag, order placement, inventory tracking, sample catalog data, and Django's password-protected admin panel.

## Stack

- Python 3.10+
- Django 5.2 LTS
- SQLite for local development
- Django templates and plain CSS

## Included

- Product search and category filters
- Product detail pages and responsive storefront
- Shopping bag stored in the visitor's session
- Server-validated checkout that records an order and reduces stock
- Admin pages for products, categories, and order status
- Six sample products with editable names, prices, copy, and image URLs
- Local migrations and a repeatable demo-data command

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

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`. Copy `.env.example` to `.env` in PowerShell with `Copy-Item .env.example .env`.

Open `http://127.0.0.1:8000/` for the store and `http://127.0.0.1:8000/admin/` for product and order management. The admin username and password are the ones you create with `createsuperuser`.

## Customize

- Change the store name and page copy in `templates/`.
- Adjust colors, spacing, and typography in `static/css/site.css`.
- Manage product names, descriptions, prices, stock, and image URLs in the admin panel.
- Update the starter catalog in `catalog/management/commands/seed_demo.py` and run `python manage.py seed_demo` again.

The demo catalog uses remote Unsplash image URLs. Replace them with images you have permission to use, or extend the project with an uploaded-image storage service.

## Before deploying

This starter records orders but does not charge customers, send email, calculate shipping or taxes, or provide customer accounts. Add and test those services for your use case. For a real store, use PostgreSQL, set a private `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=0`, configure `DJANGO_ALLOWED_HOSTS`, serve static files over HTTPS, and review Django's deployment checklist. Never reuse the demo secret in production.

