from pathlib import Path

from arm_isa_agent.kb.classification import InstructionClassificationService
from arm_isa_agent.kb.sqlite.client import SQLiteClient


def _sqlite() -> SQLiteClient:
    db = SQLiteClient("data/sqlite/isa_kb.db")
    db.initialize()
    return db


def test_xml_variant_taxonomy_is_exhaustive() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    service = InstructionClassificationService(_sqlite())
    audit = service.rebuild()

    assert audit["xml_variants"] > 0
    assert audit["classified_variants"] == audit["xml_variants"]
    assert audit["unclassified_variants"] == 0
    assert audit["duplicate_primary_assignments"] == 0
    assert sum(audit["category_variant_counts"].values()) == audit["xml_variants"]


def test_taxonomy_keeps_sve_and_sme_xml_classes_separate() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    categories = {
        category["id"]: category
        for category in InstructionClassificationService(_sqlite()).taxonomy()["categories"]
    }

    assert categories["sve"]["variant_count"] > 0
    assert categories["sve2"]["variant_count"] > 0
    assert categories["sme"]["variant_count"] > 0


def test_taxonomy_directories_and_instruction_profiles_are_resolvable() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    service = InstructionClassificationService(_sqlite())
    taxonomy = service.taxonomy()
    category = next(item for item in taxonomy["categories"] if item["variant_count"] > 0)
    directory = service.category(category["id"])

    assert directory is not None
    assert directory["category"]["subcategories"]

    subcategory = directory["category"]["subcategories"][0]
    variants = service.variants(category=category["id"], subcategory=subcategory["id"], page_size=1)
    assert variants["total"] > 0
    profile = service.instruction(variants["items"][0]["xml_id"])
    assert profile is not None
    assert profile["category"]["id"] == category["id"]
    assert profile["category"]["subcategory"]["id"] == subcategory["id"]
