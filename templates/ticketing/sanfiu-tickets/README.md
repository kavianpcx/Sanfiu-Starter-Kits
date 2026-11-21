# Sanfiu Tickets

![Sanfiu Tickets UI preview](preview.svg)

A full-stack ticket marketplace starter for event discovery, seller listings, admin review, and quantity-limited reservations. All interface copy is in English.

## Stack and features

- Python 3.10+, Django 5.2, SQLite or PostgreSQL, Django templates and CSS
- Search and category filtering for upcoming events
- Seller signup, admin approval, ticket listing creation, and seller dashboard
- Listing moderation and an admin-managed event catalog
- Buyer reservation flow that checks and decrements available quantity
- Demo events, listings, and reservation records managed through Django admin

## Run locally

From this folder, run:

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    cp .env.example .env
    python manage.py migrate
    python manage.py seed_demo
    python manage.py createsuperuser
    python manage.py runserver

Open http://127.0.0.1:8000/ for events, /sell/apply/ for seller signup, and /admin/ to manage the catalog and approvals. A new seller profile must be approved in admin before it can publish a listing.

For local PostgreSQL, set a local password in .env and run docker compose up --build. Load sample events with docker compose exec web python manage.py seed_demo and create the admin user with docker compose exec web python manage.py createsuperuser.

## Before deployment

This starter records unpaid reservations. It does not charge buyers, issue or transfer scannable tickets, verify seller identity, send confirmations, or handle refunds and disputes. The seeded seller account has no usable password. Use a payment provider, define marketplace rules, add seller verification and ticket validation, use production PostgreSQL, and configure HTTPS, email, backups, and private secrets before launch. Sample image URLs are remote and are not included in the MIT software license.

The software in this kit is MIT licensed. Sample photographs and remote services have separate terms.
