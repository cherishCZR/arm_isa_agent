"""Retrieval tools — search and query ARM instructions via RAG + SQLite."""

from __future__ import annotations

import json

import structlog
from sqlalchemy import func as sqlfunc

from arm_isa_agent.agent.tool_registry import get_rag, get_sqlite, register_tool
from arm_isa_agent.kb.sqlite.models import (
    ConstraintModel,
    EncodingModel,
    InstructionModel,
    OperandModel,
    PseudocodeModel,
)

logger = structlog.get_logger(__name__)


# ── retrieve_instruction ────────────────────────────────────────

@register_tool(
    "retrieve_instruction",
    "Semantically search for ARM instructions by description, mnemonic, or use case. "
    "Returns top-k matching instruction cards with relevance scores. "
    "Use this first when exploring an unfamiliar instruction or finding candidates.",
)
def retrieve_instruction(query: str, top_k: int = 5) -> str:
    """Hybrid search (BM25 + Vector) over the instruction card corpus.

    Args:
        query: Natural-language description (e.g., "add with shift", "SVE predicate loop").
        top_k: Number of results to return (max 10).

    Returns:
        JSON string with ranked results including mnemonic, xml_id, class, and scores.
    """
    try:
        rag = get_rag()
        response = rag.search(query, top_k=min(top_k, 10))

        results: list[dict] = []
        for r in response.results:
            results.append({
                "rank": len(results) + 1,
                "mnemonic": r.metadata.get("mnemonic", ""),
                "xml_id": r.doc_id,
                "title": r.metadata.get("title", ""),
                "instr_class": r.metadata.get("instr_class", ""),
                "rrf_score": round(r.score, 4),
                "bm25_score": round(r.bm25_score, 4),
                "vector_score": round(r.vector_score, 4),
            })

        return json.dumps({
            "query": query,
            "total_candidates": response.total_candidates,
            "elapsed_ms": response.elapsed_ms,
            "results": results,
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error("retrieve_instruction.error", error=str(e)[:200])
        return json.dumps({"error": f"Search failed: {str(e)[:300]}"}, ensure_ascii=False)


# ── query_instruction ───────────────────────────────────────────

@register_tool(
    "query_instruction",
    "Get full details of a specific ARM instruction by its XML ID or mnemonic. "
    "Returns description, operands, encodings summary, pseudocode sections, architecture features, and constraints. "
    "Use after retrieve_instruction to drill into a specific instruction.",
)
def query_instruction(xml_id_or_mnemonic: str) -> str:
    """Query full instruction details from the SQLite knowledge base.

    Args:
        xml_id_or_mnemonic: Instruction XML ID (e.g., "ADD_shifted_imm") or mnemonic (e.g., "ADD").

    Returns:
        JSON string with comprehensive instruction data.
    """
    try:
        sqlite = get_sqlite()
        with sqlite.session() as session:
            # Try exact xml_id match first, then mnemonic
            inst = session.query(InstructionModel).filter(
                InstructionModel.xml_id == xml_id_or_mnemonic
            ).first()

            if inst is None:
                # Try mnemonic search (case-insensitive)
                insts = session.query(InstructionModel).filter(
                    InstructionModel.mnemonic.ilike(xml_id_or_mnemonic)
                ).limit(5).all()
                if not insts:
                    # Try partial match on xml_id
                    insts = session.query(InstructionModel).filter(
                        InstructionModel.xml_id.ilike(f"%{xml_id_or_mnemonic}%")
                    ).limit(5).all()

                if not insts:
                    return json.dumps({
                        "found": False,
                        "query": xml_id_or_mnemonic,
                        "message": "No instruction found. Try retrieve_instruction to search semantically.",
                    }, ensure_ascii=False)

                # Return list of candidates
                candidates = [
                    {"mnemonic": i.mnemonic, "xml_id": i.xml_id, "title": i.title,
                     "instr_class": i.instr_class, "brief": i.brief[:200]}
                    for i in insts
                ]
                return json.dumps({
                    "found": False,
                    "query": xml_id_or_mnemonic,
                    "message": f"Multiple matches. Please specify exact xml_id.",
                    "candidates": candidates,
                }, ensure_ascii=False, indent=2)

            # Build full details
            enc_list: list[dict] = []
            for enc in inst.encodings:
                enc_list.append({
                    "name": enc.name,
                    "label": enc.label,
                    "assembly_template": enc.assembly_template,
                    "bitdiffs": enc.bitdiffs,
                    "bit_pattern": enc.bit_pattern,
                    "bit_pattern_mask": enc.bit_pattern_mask,
                    "equivalent_to": enc.equivalent_to if enc.equivalent_to else None,
                    "alias_condition": enc.alias_condition if enc.alias_condition else None,
                })

            op_list: list[dict] = []
            for op in inst.operands:
                op_list.append({
                    "symbol": op.symbol,
                    "description": op.description,
                    "operand_type": op.operand_type,
                    "encoded_in": op.encoded_in if op.encoded_in else None,
                    "register_class": op.register_class if op.register_class else None,
                    "register_width": op.register_width if op.register_width else None,
                })

            ps_list: list[dict] = []
            for ps in inst.pseudocode_list:
                ps_list.append({
                    "name": ps.name,
                    "section_type": ps.section_type,
                    "body_preview": ps.body_plain[:500] if ps.body_plain else ps.body[:500],
                })

            feat_list = [f.feature_name for f in inst.features] if inst.features else []

            const_list: list[dict] = []
            for c in inst.constraints:
                const_list.append({
                    "type": c.constraint_type,
                    "condition": c.condition,
                    "description": c.description,
                })

            return json.dumps({
                "found": True,
                "xml_id": inst.xml_id,
                "title": inst.title,
                "mnemonic": inst.mnemonic,
                "instr_class": inst.instr_class,
                "instruction_type": inst.instruction_type,
                "is_alias": inst.is_alias,
                "alias_of": inst.alias_of if inst.alias_of else None,
                "brief": inst.brief,
                "description": inst.description[:1000] if inst.description else "",
                "is_predicated": inst.is_predicated,
                "uses_dit": inst.uses_dit,
                "sm_policy": inst.sm_policy if inst.sm_policy else None,
                "source_file": inst.source_file,
                "encodings": enc_list,
                "operands": op_list,
                "pseudocode_sections": ps_list,
                "features": feat_list,
                "constraints": const_list,
                "operational_notes": inst.operational_notes[:500] if inst.operational_notes else "",
            }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error("query_instruction.error", error=str(e)[:200])
        return json.dumps({"error": f"Query failed: {str(e)[:300]}"}, ensure_ascii=False)


# ── query_encoding ──────────────────────────────────────────────

@register_tool(
    "query_encoding",
    "Get detailed encoding information for a specific instruction variant. "
    "Returns bit patterns, bitfield layouts, assembly template, and architecture variants. "
    "Use when the user asks about binary encoding, bit layout, or instruction format.",
)
def query_encoding(xml_id: str, encoding_name: str = "") -> str:
    """Query encoding details from SQLite.

    Args:
        xml_id: Instruction XML ID (e.g., "ADD_shifted_imm").
        encoding_name: Specific encoding name (e.g., "32-bit"). If empty, returns all encodings.

    Returns:
        JSON string with encoding details including bitfields and assembly template.
    """
    try:
        sqlite = get_sqlite()
        with sqlite.session() as session:
            inst = session.query(InstructionModel).filter(
                InstructionModel.xml_id == xml_id
            ).first()

            if inst is None:
                return json.dumps({"found": False, "message": f"Instruction '{xml_id}' not found."}, ensure_ascii=False)

            encodings = inst.encodings
            if encoding_name:
                encodings = [e for e in encodings if e.name == encoding_name or e.label == encoding_name]

            enc_details: list[dict] = []
            for enc in encodings:
                # Parse bitfields JSON
                bitfields = []
                try:
                    bf_raw = enc.bitfields_json
                    if bf_raw and bf_raw != "[]":
                        bitfields = json.loads(bf_raw)
                except (json.JSONDecodeError, TypeError):
                    pass

                # Parse arch_variants JSON
                arch_variants = []
                try:
                    av_raw = enc.arch_variants_json
                    if av_raw and av_raw != "[]":
                        arch_variants = json.loads(av_raw)
                except (json.JSONDecodeError, TypeError):
                    pass

                enc_details.append({
                    "name": enc.name,
                    "label": enc.label,
                    "assembly_template": enc.assembly_template,
                    "raw_template": enc.assembly_template_raw,
                    "bit_pattern": enc.bit_pattern,
                    "bit_pattern_mask": enc.bit_pattern_mask,
                    "bitdiffs": enc.bitdiffs,
                    "bitfields": bitfields,
                    "arch_variants": arch_variants,
                    "equivalent_to": enc.equivalent_to if enc.equivalent_to else None,
                    "alias_condition": enc.alias_condition if enc.alias_condition else None,
                })

            return json.dumps({
                "xml_id": inst.xml_id,
                "mnemonic": inst.mnemonic,
                "total_encodings": len(encodings),
                "encodings": enc_details,
            }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error("query_encoding.error", error=str(e)[:200])
        return json.dumps({"error": f"Encoding query failed: {str(e)[:300]}"}, ensure_ascii=False)


# ── query_constraint ────────────────────────────────────────────

@register_tool(
    "query_constraint",
    "Get all constraints (CONSTRAINED_UNPREDICTABLE, FEATURE_GATE, etc.) for an ARM instruction. "
    "Returns constraint types, conditions, and descriptions. "
    "Use when the user asks about edge cases, unpredictable behavior, or architecture requirements.",
)
def query_constraint(xml_id: str) -> str:
    """Query all constraints for a given instruction from SQLite.

    Args:
        xml_id: Instruction XML ID (e.g., "ADD_shifted_imm").

    Returns:
        JSON string with constraint details grouped by type.
    """
    try:
        sqlite = get_sqlite()
        with sqlite.session() as session:
            inst = session.query(InstructionModel).filter(
                InstructionModel.xml_id == xml_id
            ).first()

            if inst is None:
                return json.dumps({"found": False, "message": f"Instruction '{xml_id}' not found."}, ensure_ascii=False)

            const_list: list[dict] = []
            for c in inst.constraints:
                const_list.append({
                    "type": c.constraint_type,
                    "condition": c.condition,
                    "description": c.description,
                    "encoding_name": c.encoding_name if c.encoding_name else None,
                    "source_section": c.source_section if c.source_section else None,
                })

            # Group by type
            by_type: dict[str, list[dict]] = {}
            for c in const_list:
                ct = c["type"] or "UNKNOWN"
                by_type.setdefault(ct, []).append(c)

            return json.dumps({
                "xml_id": inst.xml_id,
                "mnemonic": inst.mnemonic,
                "total_constraints": len(const_list),
                "constraints_by_type": by_type,
            }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error("query_constraint.error", error=str(e)[:200])
        return json.dumps({"error": f"Constraint query failed: {str(e)[:300]}"}, ensure_ascii=False)
