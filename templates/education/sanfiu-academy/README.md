# Sanfiu Academy

A customizable online learning starter with a course catalog, student accounts, enrollment, lesson pages, progress tracking, sample content, and an admin panel.

[Download this kit as a ZIP](../../../downloads/sanfiu-academy.zip).

## Stack

- Python 3.10+
- Django 5.2 LTS
- SQLite for the quickest local start, or PostgreSQL with Docker Compose
- Django templates and plain CSS

## Included

- Searchable course catalog with categories and featured courses
- Student signup, sign-in, enrollment, and personal learning dashboard
- Ordered lesson pages with optional external video links
- Lesson completion and per-course progress tracking
- Django admin for course content, enrollments, and progress
- Demo courses and lessons that can be safely re-seeded

## Run locally

From this folder:

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    cp .env.example .env
    python manage.py migrate
    python manage.py seed_demo
    python manage.py createsuperuser
    python manage.py runserver

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` and copy the environment file with `Copy-Item .env.example .env`.

Open `http://127.0.0.1:8000/` to browse courses, `http://127.0.0.1:8000/accounts/signup/` to create a learner account, and `http://127.0.0.1:8000/admin/` to manage content.

To use PostgreSQL in Docker, set a local password in `.env`, then run `docker compose up --build`. In another terminal, create an admin account with `docker compose exec web python manage.py createsuperuser`. Add sample courses with `docker compose exec web python manage.py seed_demo`.

## Customize

- Change course copy, instructors, levels, categories, and lessons in the admin panel.
- Update the visual system in `static/css/site.css` and shared layout in `templates/base.html`.
- Replace the sample cover image URLs with images you have permission to use.
- Add course-specific fields or connect your preferred video hosting service in `academy/models.py`.

## Before deploying

This starter handles free enrollment and lesson progress. It does not include paid course checkout, video hosting or access control, certificates, email notifications, or instructor payouts. The optional video link opens externally and is not protected. Docker Compose is for local development. Before deployment, use PostgreSQL, configure a private `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=0` and `DJANGO_ALLOWED_HOSTS`, serve static files over HTTPS, configure backups and email, and review Django's deployment checklist. Never use the sample values in production.
