# Sanfiu Tickets

![Illustrative Sanfiu Tickets interface preview](preview.svg)

A cinema and attraction ticket-marketplace starter with movie discovery, dated screenings, venue details, seller offers, quantity-limited reservations, seller approval, and Django admin. The demo seed includes fictional film sessions and water-park day passes.

## Stack and features

- Python 3.10+, Django 5.2, SQLite or PostgreSQL, Django templates and CSS
- Search and category filters for movies, water parks, attractions, and other tickets
- Screening and venue detail pages with seller offers and available quantities
- Seller signup, admin approval, listing review, and seller dashboard
- A reservation flow that checks and decrements available inventory
- Repeatable sample sessions and ticket offers via `seed_demo`

## Run locally

From this folder, run:

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

Open `http://127.0.0.1:8000/` to browse sample tickets, `/sell/apply/` to create a seller account, and `/admin/` to manage shows and approvals. New sellers need admin approval before their offers can be published.

For local PostgreSQL, change the password in `.env`, then run `docker compose up --build`. Use `docker compose exec web python manage.py seed_demo` and `docker compose exec web python manage.py createsuperuser` to load demo records and make an admin.

## Before deployment

The reservation flow updates sample inventory but is not a paid booking system. It does not charge buyers, issue or transfer scannable tickets, assign specific cinema seats, verify seller identity, send email, or handle refunds and disputes. Add a payment provider, real seat or capacity inventory, seller verification, and ticket validation before production. All show and water-park records are fictional samples. Remote photos have terms separate from the MIT software license.
