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


## Synchronize languages

The language seed is based on the controlled vocabulary in the Google Sheet
`My Library Catalogue — Rebuild`, tab `Reference Data`.

Preview changes without writing to the database:

```bash
docker compose exec web python manage.py seed_languages --dry-run
```

Apply the synchronization:

```bash
docker compose exec web python manage.py seed_languages
```

The command is idempotent: it recognizes common English/Portuguese labels and code
variants, corrects recognized records, creates missing languages, preserves unknown
records, and reports ambiguous duplicates as conflicts instead of deleting them.


## Synchronize authors

The author seed is based on the `Authors` tab in
`My Library Catalogue — Rebuild`.

The source snapshot currently contains 252 authors. The synchronization imports
the spreadsheet author ID, canonical name, and nationality when available.
Reading counts are intentionally not imported because they will be calculated
from the application's real book/reading relationships.

Preview changes:

```bash
docker compose exec web python manage.py seed_authors --dry-run
```

Apply changes:

```bash
docker compose exec web python manage.py seed_authors
```

The command matches by spreadsheet author ID first and normalized author name
second. It preserves existing sort names, additional manually entered
nationalities, authors not found in the spreadsheet, and leaves source records
with blank nationality unfilled rather than guessing.
