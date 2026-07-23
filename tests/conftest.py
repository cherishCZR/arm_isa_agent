"""Tests configuration and shared fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# 确保 src 目录在 path 中
_src = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(_src))


@pytest.fixture(scope="session")
def xml_data_dir() -> Path:
    """ARM ISA XML 数据目录."""
    path = Path(__file__).resolve().parents[3] / "ISA_A64_xml_A_profile-2025-03" / "ISA_A64_xml_A_profile-2025-03"
    if path.exists():
        return path
    # fallback
    return Path("ISA_A64_xml_A_profile-2025-03/ISA_A64_xml_A_profile-2025-03")


@pytest.fixture(scope="session")
def sample_xml_files(xml_data_dir: Path) -> dict[str, Path]:
    """返回一组代表性 XML 文件路径."""
    return {
        "adr": xml_data_dir / "adr.xml",
        "b_cond": xml_data_dir / "b_cond.xml",
        "asr_sbfm": xml_data_dir / "asr_sbfm.xml",
        "ldr_lit_fpsimd": xml_data_dir / "ldr_lit_fpsimd.xml",
        "add_za_zzw": xml_data_dir / "add_za_zzw.xml",
        "shared_ps": xml_data_dir / "shared_pseudocode.xml",
    }
