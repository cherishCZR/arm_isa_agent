"""Exhaustive, XML-metadata-driven taxonomy for AArch64 instruction variants."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any

from sqlalchemy import func

from arm_isa_agent.kb.sqlite.models import (
    EncodingModel,
    InstructionClassificationModel,
    InstructionFacetModel,
    InstructionModel,
)

TAXONOMY_VERSION = "arm-a64-2025-03"

CATEGORY_DEFINITIONS = [
    ("base_integer", "A64 Base Integer"),
    ("branch_exception", "A64 Branch, Exception and Control Flow"),
    ("load_store", "A64 Load/Store and Address Generation"),
    ("atomic_memory", "A64 Atomic, Exclusive and Memory Ordering"),
    ("system", "A64 System, Hint and Cache Maintenance"),
    ("security", "A64 Security, PAC, MTE and Tagging"),
    ("cryptography", "A64 Cryptography"),
    ("floating_point", "A64 Floating Point"),
    ("advsimd", "A64 Advanced SIMD"),
    ("sve", "SVE"),
    ("sve2", "SVE2"),
    ("sme", "SME"),
    ("mops", "MOPS"),
    ("ls64", "LS64"),
    ("other_extensions", "Other Architectural Extensions"),
]
CATEGORY_NAMES = dict(CATEGORY_DEFINITIONS)

SUBCATEGORY_NAMES = {
    "conditional_compare_select": "Conditional Compare and Select",
    "data_processing_immediate": "Data Processing - Immediate",
    "data_processing_register": "Data Processing - Register",
    "multiply_divide": "Multiply and Divide",
    "move_address_generation": "Move and Address Generation",
    "branch_call_return": "Branch, Call and Return",
    "exception_control": "Exception and Control",
    "load_store": "Load and Store",
    "address_generation": "Address Generation",
    "simd_fp_load_store": "SIMD and FP Load/Store",
    "atomic_or_exclusive": "Atomic and Exclusive",
    "system_register_or_hint": "System Register, Hint and Cache",
    "pointer_auth_or_tagging": "Pointer Authentication and Tagging",
    "cryptographic_transform": "Cryptographic Transform",
    "arithmetic": "Arithmetic",
    "conversion_or_compare": "Conversion and Compare",
    "arithmetic_logic": "Arithmetic and Logic",
    "permute_data_movement": "Permute and Data Movement",
    "reduction": "Reduction",
    "predicated_operation": "Predicated Operation",
    "matrix_streaming": "Matrix and Streaming Operations",
    "streaming_control": "Streaming Control",
    "memory_copy_set": "Memory Copy and Set",
    "streaming_load_store": "Streaming Load/Store",
    "architectural_extension": "Other Architectural Extension",
}


def display_name(identifier: str) -> str:
    """Return a stable human-readable name for taxonomy identifiers."""
    return SUBCATEGORY_NAMES.get(identifier, identifier.replace("_", " ").title())


class InstructionClassificationService:
    """Build and query a complete primary taxonomy plus independent facets."""

    def __init__(self, sqlite_client: Any) -> None:
        self._sqlite = sqlite_client

    def rebuild(self) -> dict[str, Any]:
        """Classify every currently imported XML variant and return coverage audit."""
        with self._sqlite.session() as session:
            instructions = session.query(InstructionModel).all()
            existing = {entry.instruction_id: entry for entry in session.query(InstructionClassificationModel).all()}
            session.query(InstructionFacetModel).delete(synchronize_session=False)
            for instruction in instructions:
                category, subcategory = self._classify(instruction)
                record = existing.get(instruction.id)
                if record is None:
                    record = InstructionClassificationModel(instruction_id=instruction.id)
                    session.add(record)
                record.primary_category = category
                record.subcategory = subcategory
                record.classifier_source = "xml_rule"
                record.taxonomy_version = TAXONOMY_VERSION
                for facet_type, facet_value in self._facets(instruction, category):
                    session.add(InstructionFacetModel(
                        instruction_id=instruction.id, facet_type=facet_type, facet_value=facet_value,
                    ))
            stale_ids = set(existing) - {instruction.id for instruction in instructions}
            if stale_ids:
                session.query(InstructionClassificationModel).filter(
                    InstructionClassificationModel.instruction_id.in_(stale_ids)
                ).delete(synchronize_session=False)
        return self.audit()

    def ensure_current(self) -> dict[str, Any]:
        with self._sqlite.session() as session:
            variant_count = session.query(InstructionModel).count()
            classified_count = session.query(InstructionClassificationModel).count()
            current_version_count = session.query(InstructionClassificationModel).filter(
                InstructionClassificationModel.taxonomy_version == TAXONOMY_VERSION
            ).count()
        return self.rebuild() if variant_count != classified_count or variant_count != current_version_count else self.audit()

    def audit(self, xml_dir: Path | None = None) -> dict[str, Any]:
        with self._sqlite.session() as session:
            variants = session.query(InstructionModel).count()
            encodings = session.query(EncodingModel).count()
            classifications = session.query(InstructionClassificationModel).all()
            by_category = Counter(entry.primary_category for entry in classifications)
            duplicate_assignments = sum(
                1 for _, count in session.query(
                    InstructionClassificationModel.instruction_id,
                    func.count(InstructionClassificationModel.id),
                ).group_by(InstructionClassificationModel.instruction_id).all() if count != 1
            )
            xml_file_count = None
            if xml_dir and xml_dir.exists():
                xml_file_count = len([path for path in xml_dir.glob("*.xml") if path.name != "shared_pseudocode.xml"])
            return {
                "taxonomy_version": TAXONOMY_VERSION,
                "xml_instruction_files": xml_file_count,
                "xml_variants": variants,
                "classified_variants": len(classifications),
                "unclassified_variants": max(0, variants - len(classifications)),
                "duplicate_primary_assignments": duplicate_assignments,
                "encodings": encodings,
                "category_variant_counts": dict(sorted(by_category.items())),
                "coverage_complete": variants == len(classifications) and duplicate_assignments == 0,
            }

    def taxonomy(self) -> dict[str, Any]:
        audit = self.ensure_current()
        with self._sqlite.session() as session:
            rows = session.query(InstructionClassificationModel).all()
            grouped: dict[str, list[InstructionClassificationModel]] = defaultdict(list)
            for row in rows:
                grouped[row.primary_category].append(row)
            categories = []
            for category_id, name in CATEGORY_DEFINITIONS:
                records = grouped.get(category_id, [])
                instruction_ids = [record.instruction_id for record in records]
                mnemonic_count = 0
                encoding_count = 0
                subcategories: dict[str, int] = {}
                if instruction_ids:
                    mnemonic_count = len({row[0] for row in session.query(InstructionModel.mnemonic).filter(InstructionModel.id.in_(instruction_ids)).all() if row[0]})
                    encoding_count = session.query(EncodingModel).filter(EncodingModel.instruction_id.in_(instruction_ids)).count()
                    subcategories = dict(Counter(record.subcategory for record in records))
                categories.append({
                    "id": category_id,
                    "name": name,
                    "variant_count": len(records),
                    "mnemonic_count": mnemonic_count,
                    "encoding_count": encoding_count,
                    "subcategories": [
                        {"id": key, "name": display_name(key), "variant_count": value}
                        for key, value in sorted(subcategories.items())
                    ],
                })
        return {"taxonomy_version": TAXONOMY_VERSION, "coverage": audit, "categories": categories}

    def category(self, category_id: str) -> dict[str, Any] | None:
        taxonomy = self.taxonomy()
        category = next((item for item in taxonomy["categories"] if item["id"] == category_id), None)
        if category is None or category["variant_count"] == 0:
            return None
        return {"taxonomy_version": taxonomy["taxonomy_version"], "category": category}

    def variants(
        self,
        category: str | None = None,
        subcategory: str | None = None,
        search: str = "",
        page: int = 1,
        page_size: int = 50,
    ) -> dict[str, Any]:
        page = max(1, page)
        page_size = min(max(1, page_size), 200)
        with self._sqlite.session() as session:
            query = session.query(InstructionModel, InstructionClassificationModel).join(
                InstructionClassificationModel, InstructionClassificationModel.instruction_id == InstructionModel.id,
            )
            if category:
                query = query.filter(InstructionClassificationModel.primary_category == category)
            if subcategory:
                query = query.filter(InstructionClassificationModel.subcategory == subcategory)
            if search.strip():
                term = f"%{search.strip()}%"
                query = query.filter((InstructionModel.mnemonic.ilike(term)) | (InstructionModel.xml_id.ilike(term)) | (InstructionModel.title.ilike(term)))
            total = query.count()
            rows = query.order_by(InstructionModel.mnemonic, InstructionModel.xml_id).offset((page - 1) * page_size).limit(page_size).all()
            items = []
            for instruction, classification in rows:
                items.append({
                    "xml_id": instruction.xml_id,
                    "mnemonic": instruction.mnemonic or "(no mnemonic)",
                    "title": instruction.title,
                    "primary_category": classification.primary_category,
                    "subcategory": classification.subcategory,
                    "encoding_count": len(instruction.encodings),
                    "features": [feature.feature_name for feature in instruction.features],
                    "operand_classes": sorted({operand.register_class for operand in instruction.operands if operand.register_class}),
                    "is_alias": instruction.is_alias,
                })
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    def instruction(self, xml_id: str) -> dict[str, Any] | None:
        """Return a complete, presentation-ready record for one XML variant."""
        with self._sqlite.session() as session:
            instruction = session.query(InstructionModel).filter(InstructionModel.xml_id == xml_id).one_or_none()
            if instruction is None or instruction.classification is None:
                return None
            classification = instruction.classification
            encodings = [
                {
                    "name": encoding.name,
                    "label": encoding.label,
                    "assembly_template": encoding.assembly_template,
                    "assembly_template_raw": encoding.assembly_template_raw,
                    "bit_pattern": encoding.bit_pattern,
                    "bitdiffs": encoding.bitdiffs,
                    "operand_symbols": self._json_list(encoding.operand_symbols_json),
                    "arch_variants": self._json_list(encoding.arch_variants_json),
                }
                for encoding in instruction.encodings
            ]
            return {
                "xml_id": instruction.xml_id,
                "mnemonic": instruction.mnemonic or "(no mnemonic)",
                "title": instruction.title,
                "brief": instruction.brief,
                "description": instruction.description,
                "instruction_type": instruction.instruction_type,
                "is_alias": instruction.is_alias,
                "alias_of": instruction.alias_of,
                "instr_class": instruction.instr_class,
                "source_file": instruction.source_file,
                "is_predicated": instruction.is_predicated,
                "category": {
                    "id": classification.primary_category,
                    "name": CATEGORY_NAMES.get(classification.primary_category, display_name(classification.primary_category)),
                    "subcategory": {
                        "id": classification.subcategory,
                        "name": display_name(classification.subcategory),
                    },
                },
                "features": sorted(feature.feature_name for feature in instruction.features),
                "operands": [
                    {
                        "symbol": operand.symbol,
                        "description": operand.description,
                        "type": operand.operand_type,
                        "register_class": operand.register_class,
                        "register_width": operand.register_width,
                        "encoding_name": operand.encoding_name,
                    }
                    for operand in instruction.operands
                ],
                "constraints": [
                    {
                        "type": constraint.constraint_type,
                        "condition": constraint.condition,
                        "description": constraint.description,
                        "encoding_name": constraint.encoding_name,
                    }
                    for constraint in instruction.constraints
                ],
                "encodings": encodings,
                "pseudocode": [
                    {"name": item.name, "section_type": item.section_type, "body": item.body_plain or item.body}
                    for item in instruction.pseudocode_list
                ],
            }

    def related_variants(self, xml_id: str, limit: int = 12) -> list[dict[str, Any]]:
        with self._sqlite.session() as session:
            instruction = session.query(InstructionModel).filter(InstructionModel.xml_id == xml_id).one_or_none()
            if instruction is None or not instruction.mnemonic:
                return []
            rows = session.query(InstructionModel, InstructionClassificationModel).join(
                InstructionClassificationModel, InstructionClassificationModel.instruction_id == InstructionModel.id,
            ).filter(
                InstructionModel.mnemonic == instruction.mnemonic,
                InstructionModel.xml_id != instruction.xml_id,
            ).order_by(InstructionModel.xml_id).limit(max(1, min(limit, 50))).all()
            return [
                {
                    "xml_id": variant.xml_id,
                    "mnemonic": variant.mnemonic or "(no mnemonic)",
                    "title": variant.title,
                    "primary_category": classification.primary_category,
                    "subcategory": classification.subcategory,
                    "encoding_count": len(variant.encodings),
                }
                for variant, classification in rows
            ]

    @staticmethod
    def _json_list(value: str) -> list[Any]:
        try:
            result = json.loads(value or "[]")
        except json.JSONDecodeError:
            return []
        return result if isinstance(result, list) else []

    @staticmethod
    def _classify(instruction: InstructionModel) -> tuple[str, str]:
        features = " ".join(feature.feature_name.upper() for feature in instruction.features)
        mnemonic = (instruction.mnemonic or "").upper()
        xml_id = instruction.xml_id.lower()
        text = " ".join([instruction.title, instruction.brief, instruction.description[:500], xml_id]).lower()
        instr_class = (instruction.instr_class or "").lower()

        if "FEAT_MOPS" in features:
            return "mops", "memory_copy_set"
        if "FEAT_LS64" in features:
            return "ls64", "streaming_load_store"
        # XML instruction class is authoritative for SVE/SVE2/SME.  A feature
        # expression such as ``FEAT_SVE || FEAT_SME`` must not reclassify an
        # SVE XML variant as SME merely because it names an alternative gate.
        if instr_class in {"mortlach", "mortlach2"}:
            return "sme", "matrix_streaming" if "za" in xml_id or "mopa" in xml_id else "streaming_control"
        if instr_class == "sve2":
            return "sve2", InstructionClassificationService._vector_subcategory(text, xml_id)
        if instr_class == "sve":
            return "sve", InstructionClassificationService._vector_subcategory(text, xml_id)
        if "FEAT_SME" in features:
            return "sme", "matrix_streaming" if "za" in xml_id or "mopa" in xml_id else "streaming_control"
        if "FEAT_SVE2" in features:
            return "sve2", InstructionClassificationService._vector_subcategory(text, xml_id)
        if "FEAT_SVE" in features:
            return "sve", InstructionClassificationService._vector_subcategory(text, xml_id)
        if any(token in features for token in ("FEAT_AES", "FEAT_SHA", "FEAT_SM3", "FEAT_SM4", "FEAT_PMULL")):
            return "cryptography", "cryptographic_transform"
        if any(token in features for token in ("FEAT_PAUTH", "FEAT_MTE", "FEAT_GCS", "FEAT_THE", "FEAT_CPA")):
            return "security", "pointer_auth_or_tagging"
        if instr_class == "system":
            return "system", "system_register_or_hint"
        if instr_class == "float":
            return "floating_point", "arithmetic" if mnemonic.startswith("F") else "conversion_or_compare"
        if instr_class == "advsimd":
            return "advsimd", InstructionClassificationService._vector_subcategory(text, xml_id)
        if instr_class == "fpsimd":
            return "load_store", "simd_fp_load_store"
        if any(token in features for token in ("FEAT_LSE", "FEAT_LRCPC", "FEAT_LOR")) or any(part in xml_id for part in ("atomic", "cas", "swp", "ldxr", "stxr")):
            return "atomic_memory", "atomic_or_exclusive"
        if mnemonic in {"B", "BL", "BR", "BLR", "RET", "ERET", "DRPS", "BRK", "HLT", "SVC", "HVC", "SMC"} or "branch" in text or "exception" in text:
            return "branch_exception", "branch_call_return" if mnemonic in {"B", "BL", "BR", "BLR", "RET"} else "exception_control"
        if InstructionClassificationService._is_memory_instruction(instruction, mnemonic, xml_id):
            return "load_store", "load_store" if mnemonic.startswith(("LD", "ST")) else "address_generation"
        if any(token in features for token in ("FEAT_DIT", "FEAT_RME", "FEAT_TME", "FEAT_SPECRES")):
            return "other_extensions", "architectural_extension"
        return "base_integer", InstructionClassificationService._integer_subcategory(xml_id, mnemonic)

    @staticmethod
    def _is_memory_instruction(instruction: InstructionModel, mnemonic: str, xml_id: str) -> bool:
        return mnemonic.startswith(("LD", "ST", "PRFM")) or "load" in xml_id or "store" in xml_id or any(
            operand.operand_type == "memory" for operand in instruction.operands
        )

    @staticmethod
    def _integer_subcategory(xml_id: str, mnemonic: str) -> str:
        if any(token in xml_id for token in ("addsub_imm", "logical_imm", "movwide", "bitfield")):
            return "data_processing_immediate"
        if any(token in xml_id for token in ("mul", "div", "madd", "msub")):
            return "multiply_divide"
        if mnemonic.startswith(("CSEL", "CSINC", "CSINV", "CSNEG", "CCMP", "CCMN")):
            return "conditional_compare_select"
        if mnemonic in {"ADR", "ADRP", "MOV", "MOVK", "MOVN", "MOVZ"}:
            return "move_address_generation"
        return "data_processing_register"

    @staticmethod
    def _vector_subcategory(text: str, xml_id: str) -> str:
        if any(token in text for token in ("load", "store", "gather", "scatter")):
            return "load_store"
        if any(token in text for token in ("reduce", "across", "pairwise")) or "addp" in xml_id:
            return "reduction"
        if any(token in text for token in ("permute", "zip", "unzip", "table", "compact")):
            return "permute_data_movement"
        if "predicate" in text or "_p_" in xml_id:
            return "predicated_operation"
        return "arithmetic_logic"

    @staticmethod
    def _facets(instruction: InstructionModel, category: str) -> list[tuple[str, str]]:
        facets = [("primary_category", category), ("xml_instr_class", instruction.instr_class or "unknown")]
        facets.extend(("feature", feature.feature_name) for feature in instruction.features)
        facets.extend(("operand_class", operand.register_class) for operand in instruction.operands if operand.register_class)
        if instruction.is_alias:
            facets.append(("kind", "alias"))
        if instruction.is_predicated:
            facets.append(("execution", "predicated"))
        if any(operand.operand_type == "memory" for operand in instruction.operands):
            facets.append(("semantic", "memory"))
        return list(dict.fromkeys(facets))
