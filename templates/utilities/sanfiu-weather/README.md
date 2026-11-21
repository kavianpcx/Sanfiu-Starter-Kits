# Sanfiu Weather

![Sanfiu Weather UI preview](preview.svg)

A weather dashboard starter with city pages, current-condition fields, five-day forecast records, and Django admin management. The included values are clearly labeled sample data, not live forecasts.

## Included

- Searchable city dashboard and city detail pages
- Weather station and daily forecast models with admin workflows
- Sample cities and forecast records
- SQLite or PostgreSQL with Docker Compose
- Responsive interface in English

## Run locally

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    cp .env.example .env
    python manage.py migrate
    python manage.py seed_demo
    python manage.py createsuperuser
    python manage.py runserver

Open http://127.0.0.1:8000/ and manage city data at /admin/. For PostgreSQL in Docker, set a local password in .env and run docker compose up --build, then run docker compose exec web python manage.py seed_demo and docker compose exec web python manage.py createsuperuser.

## Live data

The included forecast records are sample content. Connect a weather-data provider in the view or add a scheduled import command before showing current conditions to visitors. The starter does not make live weather requests or include API credentials. Sample photography is remote and separate from the MIT software license.

The software in this kit is MIT licensed. Sample photographs and remote services have separate terms.
