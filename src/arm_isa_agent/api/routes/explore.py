"""Explore API backed by the exhaustive XML-variant taxonomy."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from arm_isa_agent.api.deps import get_sqlite
from arm_isa_agent.core.config import get_settings
from arm_isa_agent.kb.classification import InstructionClassificationService

router = APIRouter(prefix="/api/explore", tags=["explore"])


@router.get("/taxonomy")
async def get_taxonomy():
    return InstructionClassificationService(get_sqlite()).taxonomy()


@router.get("/coverage")
async def get_coverage():
    service = InstructionClassificationService(get_sqlite())
    service.ensure_current()
    return service.audit(get_settings().raw_xml_dir)


@router.get("/variants")
async def get_variants(
    category: str | None = None,
    subcategory: str | None = None,
    search: str = "",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    service = InstructionClassificationService(get_sqlite())
    service.ensure_current()
    return service.variants(
        category=category,
        subcategory=subcategory,
        search=search,
        page=page,
        page_size=page_size,
    )


@router.get("/categories/{category_id}")
async def get_category(category_id: str):
    service = InstructionClassificationService(get_sqlite())
    service.ensure_current()
    result = service.category(category_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Unknown or empty taxonomy category: {category_id}")
    return result


@router.get("/categories/{category_id}/{subcategory_id}")
async def get_subcategory(
    category_id: str,
    subcategory_id: str,
    search: str = "",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    service = InstructionClassificationService(get_sqlite())
    service.ensure_current()
    category = service.category(category_id)
    if category is None or not any(item["id"] == subcategory_id for item in category["category"]["subcategories"]):
        raise HTTPException(status_code=404, detail=f"Unknown taxonomy subcategory: {category_id}/{subcategory_id}")
    return {
        "category": category["category"],
        "subcategory": next(item for item in category["category"]["subcategories"] if item["id"] == subcategory_id),
        **service.variants(category=category_id, subcategory=subcategory_id, search=search, page=page, page_size=page_size),
    }


@router.get("/instructions/{xml_id}")
async def get_instruction(xml_id: str):
    service = InstructionClassificationService(get_sqlite())
    service.ensure_current()
    result = service.instruction(xml_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Unknown XML instruction variant: {xml_id}")
    return result


@router.get("/instructions/{xml_id}/related")
async def get_related_variants(xml_id: str, limit: int = Query(default=12, ge=1, le=50)):
    service = InstructionClassificationService(get_sqlite())
    service.ensure_current()
    if service.instruction(xml_id) is None:
        raise HTTPException(status_code=404, detail=f"Unknown XML instruction variant: {xml_id}")
    return {"items": service.related_variants(xml_id, limit=limit)}
