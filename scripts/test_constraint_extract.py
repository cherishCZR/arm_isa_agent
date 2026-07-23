"""测试 constraint_extractor 功能 —— 不依赖完整 ETL Pipeline。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from arm_isa_agent.etl.xml_parser import XMLInstructionParser
from arm_isa_agent.etl.constraint_extractor import EncodingConstraintExtractor
from arm_isa_agent.core.config import Settings, get_settings

# 测试文件列表（基于已知文件）
TEST_FILES = [
    "abs.xml",         # FEATURE_GATE: FEAT_CSSC → UNDEF
    "esb.xml",         # FEATURE_GATE: FEAT_RAS → NOP
    "dgh.xml",         # FEATURE_GATE: FEAT_DGH → NOP
    "bti.xml",         # FEATURE_GATE: FEAT_BTI → NOP
    "clrbhb.xml",      # FEATURE_GATE: FEAT_CLRBHB → NOP
    "hint.xml",        # DECODE_FALLBACK: otherwise → NOP + 多个 FEATURE_GATE
    "ldr_imm_gen.xml", # CONSTRAINED_UNPREDICTABLE: WBOVERLAPLD
]

def main():
    settings = get_settings()
    xml_dir = settings.raw_xml_dir

    for fname in TEST_FILES:
        filepath = xml_dir / fname
        if not filepath.exists():
            print(f"[SKIP] {fname} — not found")
            continue

        result = XMLInstructionParser.parse_file(filepath)
        if not result.ok:
            print(f"[FAIL] {fname}: {result.error}")
            continue

        inst = result.instruction
        if not inst:
            print(f"[SKIP] {fname} — no instruction")
            continue

        print(f"\n{'='*60}")
        print(f"[FILE] {fname} ({inst.mnemonic or inst.xml_id})")
        print(f"   Pseudocode sections: {[(ps.section_type, ps.name.split('.')[-1]) for ps in inst.pseudocode_list]}")
        print(f"   Constraints extracted: {len(inst.constraints)}")

        for c in inst.constraints:
            print(f"   |-- [{c.constraint_type}]")
            print(f"   |   Condition : {c.condition}")
            print(f"   |   Description: {c.description}")
        print(f"   `-- Total: {len(inst.constraints)} constraints")

    print(f"\n{'='*60}")
    print("Test complete")


if __name__ == "__main__":
    main()
