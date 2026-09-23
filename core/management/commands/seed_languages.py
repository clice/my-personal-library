import re
import unicodedata

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Language


LANGUAGES = [
    {
        "name": "Português (Brasil)",
        "code": "pt-BR",
        "aliases": {
            "Brazilian Portuguese",
            "Português Brasileiro",
            "Português do Brasil",
            "Português (Brasil)",
            "Português",
        },
        "code_aliases": {"pt", "pt-br", "pt_br"},
    },
    {
        "name": "Inglês",
        "code": "en",
        "aliases": {"English", "Inglês", "Ingles"},
        "code_aliases": {"en"},
    },
    {
        "name": "Francês",
        "code": "fr",
        "aliases": {"French", "Francês", "Frances"},
        "code_aliases": {"fr"},
    },
    {
        "name": "Espanhol",
        "code": "es",
        "aliases": {"Spanish", "Espanhol"},
        "code_aliases": {"es"},
    },
    {
        "name": "Italiano",
        "code": "it",
        "aliases": {"Italian", "Italiano"},
        "code_aliases": {"it"},
    },
    {
        "name": "Alemão",
        "code": "de",
        "aliases": {"German", "Alemão", "Alemao"},
        "code_aliases": {"de"},
    },
    {
        "name": "Japonês",
        "code": "ja",
        "aliases": {"Japanese", "Japonês", "Japones"},
        "code_aliases": {"ja", "jp"},
    },
    {
        "name": "Outro",
        "code": "other",
        "aliases": {"Other", "Outro", "Outros"},
        "code_aliases": {"other"},
    },
    {
        "name": "Português (Portugal)",
        "code": "pt-PT",
        "aliases": {
            "Portuguese",
            "Português de Portugal",
            "Português (Portugal)",
            "European Portuguese",
        },
        "code_aliases": {"pt-pt", "pt_pt"},
    },
    {
        "name": "Holandês",
        "code": "nl",
        "aliases": {"Dutch", "Holandês", "Holandes"},
        "code_aliases": {"nl"},
    },
]


def normalize_text(value):
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    value = value.casefold().strip()
    return re.sub(r"\s+", " ", value)


def normalize_code(value):
    return (value or "").strip().replace("_", "-").casefold()


class Command(BaseCommand):
    help = (
        "Synchronize the Language table with the controlled vocabulary from "
        "'My Library Catalogue — Rebuild' / 'Reference Data'."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would change without modifying the database.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        existing = list(Language.objects.order_by("id"))
        matched_ids = set()

        created = 0
        updated = 0
        unchanged = 0
        conflicts = 0

        self.stdout.write(
            self.style.MIGRATE_HEADING(
                "Language synchronization" + (" (dry run)" if dry_run else "")
            )
        )

        with transaction.atomic():
            for definition in LANGUAGES:
                alias_names = {
                    normalize_text(definition["name"]),
                    *(normalize_text(value) for value in definition["aliases"]),
                }
                alias_codes = {
                    normalize_code(definition["code"]),
                    *(normalize_code(value) for value in definition["code_aliases"]),
                }

                code_matches = [
                    item
                    for item in existing
                    if item.id not in matched_ids
                    and item.code
                    and normalize_code(item.code) in alias_codes
                ]
                name_matches = [
                    item
                    for item in existing
                    if item.id not in matched_ids
                    and normalize_text(item.name) in alias_names
                ]

                candidates = []
                seen = set()
                for item in code_matches + name_matches:
                    if item.id not in seen:
                        seen.add(item.id)
                        candidates.append(item)

                if len(candidates) > 1:
                    conflicts += 1
                    labels = ", ".join(
                        f"#{item.id} {item.name!r} ({item.code or 'sem código'})"
                        for item in candidates
                    )
                    self.stdout.write(
                        self.style.WARNING(
                            f"CONFLICT  {definition['name']}: {labels}. "
                            "Nenhum registro foi alterado."
                        )
                    )
                    continue

                if not candidates:
                    created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"CREATE    {definition['name']} [{definition['code']}]"
                        )
                    )
                    if not dry_run:
                        item = Language.objects.create(
                            name=definition["name"],
                            code=definition["code"],
                        )
                        existing.append(item)
                        matched_ids.add(item.id)
                    continue

                item = candidates[0]
                matched_ids.add(item.id)

                changes = []
                if item.name != definition["name"]:
                    changes.append(f"nome: {item.name!r} → {definition['name']!r}")
                if item.code != definition["code"]:
                    changes.append(f"código: {item.code or '—'} → {definition['code']}")

                if not changes:
                    unchanged += 1
                    self.stdout.write(
                        f"OK        {definition['name']} [{definition['code']}]"
                    )
                    continue

                updated += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"UPDATE    #{item.id} " + "; ".join(changes)
                    )
                )

                if not dry_run:
                    item.name = definition["name"]
                    item.code = definition["code"]
                    item.save(update_fields=["name", "code"])

            unmatched = [
                item for item in existing if item.id not in matched_ids
            ]

            if unmatched:
                self.stdout.write("")
                self.stdout.write(
                    self.style.WARNING(
                        "Registros existentes não reconhecidos foram preservados:"
                    )
                )
                for item in unmatched:
                    self.stdout.write(
                        f"  - #{item.id} {item.name} [{item.code or 'sem código'}]"
                    )

            if dry_run:
                transaction.set_rollback(True)

        self.stdout.write("")
        self.stdout.write(
            self.style.MIGRATE_LABEL(
                "Resumo: "
                f"{created} criar, {updated} corrigir, "
                f"{unchanged} já corretos, {conflicts} conflitos."
            )
        )

        if conflicts:
            self.stdout.write(
                self.style.WARNING(
                    "Há conflitos que exigem revisão antes de uma sincronização completa."
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
                self.style.SUCCESS("Idiomas sincronizados com sucesso.")
            )
