import json
import re
import unicodedata
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import Author, Nationality


NATIONALITY_MAP = {
    "Ancient Greece": ("HIST-GRC", "Grécia Antiga", ""),
    "Argentina": ("AR", "Argentina", ""),
    "Austria": ("AT", "Áustria", ""),
    "Brazil": ("BR", "Brasil", ""),
    "Canada": ("CA", "Canadá", ""),
    "Colombia": ("CO", "Colômbia", ""),
    "Czech Republic": ("CZ", "República Tcheca", ""),
    "England": ("GB-ENG", "Inglaterra", "Reino Unido"),
    "France": ("FR", "França", ""),
    "Germany": ("DE", "Alemanha", ""),
    "Ireland": ("IE", "Irlanda", ""),
    "Israel": ("IL", "Israel", ""),
    "Italy": ("IT", "Itália", ""),
    "Mexico": ("MX", "México", ""),
    "Northern Ireland": ("GB-NIR", "Irlanda do Norte", "Reino Unido"),
    "Norway": ("NO", "Noruega", ""),
    "Poland": ("PL", "Polônia", ""),
    "Portugal": ("PT", "Portugal", ""),
    "Roman Empire": ("HIST-ROM", "Império Romano", ""),
    "Russia": ("RU", "Rússia", ""),
    "Scotland": ("GB-SCT", "Escócia", "Reino Unido"),
    "Spain": ("ES", "Espanha", ""),
    "Turkey": ("TR", "Turquia", ""),
    "United States": ("US", "Estados Unidos", ""),
    "Unknown": ("UNK", "Desconhecida", ""),
    "Wales": ("GB-WLS", "País de Gales", "Reino Unido"),
}


def normalize_text(value):
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    value = value.casefold().strip()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


class Command(BaseCommand):
    help = (
        "Synchronize authors from 'My Library Catalogue — Rebuild' / 'Authors'. "
        "Existing authors are matched by spreadsheet source ID first and normalized name second."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would change without modifying the database.",
        )

    def _load_seed(self):
        path = Path(__file__).resolve().parents[2] / "data" / "authors_seed.json"

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CommandError(f"Could not read author seed data: {exc}") from exc

        source_ids = [item["source_id"] for item in data]
        if len(source_ids) != len(set(source_ids)):
            raise CommandError("Duplicate source IDs found in authors_seed.json.")

        return data

    def _ensure_nationality(self, source_value):
        if not source_value:
            return None

        definition = NATIONALITY_MAP.get(source_value)
        if not definition:
            raise CommandError(
                f"Nationality {source_value!r} has no mapping in seed_authors.py."
            )

        code, name, sovereign_state = definition
        nationality, _ = Nationality.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "sovereign_state": sovereign_state,
            },
        )
        return nationality

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        seed = self._load_seed()

        authors = list(
            Author.objects.prefetch_related("nationalities").order_by("id")
        )
        matched_ids = set()

        created = 0
        updated = 0
        unchanged = 0
        conflicts = 0
        nationality_changes = 0

        self.stdout.write(
            self.style.MIGRATE_HEADING(
                f"Author synchronization — {len(seed)} source records"
                + (" (dry run)" if dry_run else "")
            )
        )

        with transaction.atomic():
            for item in seed:
                source_id = item["source_id"].strip()
                source_name = item["name"].strip()
                source_nationality = item.get("nationality", "").strip()

                source_matches = [
                    author
                    for author in authors
                    if author.source_id == source_id
                ]

                if len(source_matches) > 1:
                    conflicts += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"CONFLICT  {source_id} {source_name}: "
                            "mais de um registro com o mesmo ID de origem."
                        )
                    )
                    continue

                author = source_matches[0] if source_matches else None

                if author is None:
                    normalized_name = normalize_text(source_name)
                    name_matches = [
                        candidate
                        for candidate in authors
                        if candidate.id not in matched_ids
                        and normalize_text(candidate.name) == normalized_name
                    ]

                    if len(name_matches) > 1:
                        conflicts += 1
                        labels = ", ".join(
                            f"#{candidate.id} {candidate.name!r}"
                            for candidate in name_matches
                        )
                        self.stdout.write(
                            self.style.WARNING(
                                f"CONFLICT  {source_id} {source_name}: "
                                f"mais de um autor corresponde ao nome ({labels})."
                            )
                        )
                        continue

                    author = name_matches[0] if name_matches else None

                changes = []

                if author is None:
                    author = Author(
                        source_id=source_id,
                        name=source_name,
                    )
                    if not dry_run:
                        author.save()
                    else:
                        author.save()

                    authors.append(author)
                    matched_ids.add(author.id)
                    created += 1
                    changes.append("criar autor")
                else:
                    matched_ids.add(author.id)

                    if author.source_id != source_id:
                        changes.append(
                            f"ID: {author.source_id or '—'} → {source_id}"
                        )
                        author.source_id = source_id

                    if author.name != source_name:
                        changes.append(
                            f"nome: {author.name!r} → {source_name!r}"
                        )
                        author.name = source_name

                    if changes:
                        author.save(update_fields=["source_id", "name"])

                nationality = self._ensure_nationality(source_nationality)

                if nationality is not None:
                    current_ids = set(
                        author.nationalities.values_list("id", flat=True)
                    )

                    if nationality.id not in current_ids:
                        if (
                            source_nationality == "Unknown"
                            and current_ids
                        ):
                            changes.append(
                                "nacionalidade da planilha é desconhecida; "
                                "nacionalidade existente preservada"
                            )
                        else:
                            author.nationalities.add(nationality)
                            nationality_changes += 1
                            changes.append(
                                f"adicionar nacionalidade: {nationality.name}"
                            )

                if "criar autor" in changes:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"CREATE    {source_id} · {source_name}"
                            + (
                                f" · {source_nationality}"
                                if source_nationality
                                else ""
                            )
                        )
                    )
                elif changes:
                    updated += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"UPDATE    {source_id} · {source_name} · "
                            + "; ".join(changes)
                        )
                    )
                else:
                    unchanged += 1

            unmatched = [
                author
                for author in authors
                if author.id not in matched_ids
            ]

            if unmatched:
                self.stdout.write("")
                self.stdout.write(
                    self.style.WARNING(
                        "Autores locais não reconhecidos na planilha foram preservados:"
                    )
                )
                for author in unmatched:
                    self.stdout.write(
                        f"  - #{author.id} {author.name}"
                        + (
                            f" [{author.source_id}]"
                            if author.source_id
                            else ""
                        )
                    )

            if dry_run:
                transaction.set_rollback(True)

        self.stdout.write("")
        self.stdout.write(
            self.style.MIGRATE_LABEL(
                "Resumo: "
                f"{created} criar, {updated} atualizar, "
                f"{unchanged} já corretos, "
                f"{nationality_changes} vínculos de nacionalidade, "
                f"{conflicts} conflitos."
            )
        )

        if conflicts:
            self.stdout.write(
                self.style.WARNING(
                    "Conflitos foram preservados sem alteração automática."
                )
            )
        elif dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    "Dry run concluído. Nenhuma alteração foi salva."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Autores sincronizados com sucesso.")
            )
