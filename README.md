# My Personal Library

Personal library catalog built gradually with Django.

## Current milestone

Project foundation and visual layout only. No collection data or final catalog models have been added yet.

## Local setup

1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build`.
3. In another terminal, run `docker compose exec web python manage.py migrate`.
4. Open `http://localhost:8001`.

The Django development server runs on port 8000 inside the container and is exposed on port 8001 on the host to avoid conflicts with other local projects.

The first implementation intentionally contains only the Dashboard, Catalog, Editions, Authors and Languages layout shells.
