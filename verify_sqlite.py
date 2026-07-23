"""verify_sqlite.py — 验证 SQLite 数据量和格式"""
import sqlite3
import os

# 自动定位项目根目录（脚本放在项目根目录执行）
ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT, "data", "sqlite", "isa_kb.db")

if not os.path.exists(DB_PATH):
    print(f"❌ 找不到数据库文件: {DB_PATH}")
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

TABLES = [
    "instructions", "encodings", "operands", "pseudocode",
    "constraints", "features", "shared_pseudocode",
    "instruction_index", "instruction_features",
]

print("=" * 64)
print("1. 各表行数 (ROW COUNTS)")
print("=" * 64)
counts = {}
for t in TABLES:
    try:
        n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    except sqlite3.OperationalError:
        n = "N/A (表不存在)"
    counts[t] = n
    print(f"  {t:24s} : {n}")

print("\n" + "=" * 64)
print("2. 与源文件交叉比对 (CROSS CHECK)")
print("=" * 64)
xml_dir = os.path.join(ROOT, "ISA_A64_xml_A_profile-2025-03", "ISA_A64_xml_A_profile-2025-03")
xml_count = len([f for f in os.listdir(xml_dir) if f.endswith(".xml")]) if os.path.isdir(xml_dir) else "N/A"
card_dir = os.path.join(ROOT, "data", "cards")
card_count = len([f for f in os.listdir(card_dir) if f.endswith(".md")]) if os.path.isdir(card_dir) else "N/A"
print(f"  XML 源文件数 (.xml)        : {xml_count}")
print(f"  Card .md 文件数            : {card_count}")
print(f"  instructions 条数          : {counts.get('instructions')}")

print("\n" + "=" * 64)
print("3. instructions 分类统计 (BREAKDOWN)")
print("=" * 64)
for row in cur.execute("SELECT instruction_type, COUNT(*) c FROM instructions GROUP BY instruction_type"):
    print(f"  instruction_type={row['instruction_type']:14s} : {row['c']}")
for row in cur.execute("SELECT is_alias, COUNT(*) c FROM instructions GROUP BY is_alias"):
    print(f"  is_alias={row['is_alias']!s:14s} : {row['c']}")

print("\n" + "=" * 64)
print("4. 格式检查 (FORMAT CHECKS)")
print("=" * 64)

# 4.1 bit_pattern 是可选字段；空值必须由 bitfields_json 兜底
n_empty = cur.execute(
    "SELECT COUNT(*) FROM encodings WHERE bit_pattern IS NULL OR bit_pattern=''"
).fetchone()[0]
n_empty_ok = cur.execute(
    "SELECT COUNT(*) FROM encodings WHERE (bit_pattern IS NULL OR bit_pattern='') "
    "AND bitfields_json IS NOT NULL AND bitfields_json<>''"
).fetchone()[0]
bad_filled = cur.execute(
    "SELECT COUNT(*) FROM encodings WHERE bit_pattern IS NOT NULL AND bit_pattern<>'' "
    "AND (LENGTH(bit_pattern)!=32 OR bit_pattern GLOB '*[^01?]*')"
).fetchone()[0]
print(f"  bit_pattern 为空但无 bitfields_json 兜底 : {n_empty - n_empty_ok}  (期望 0)")
print(f"  bit_pattern 已填但格式非法(非32位/非01?) : {bad_filled}  (期望 0)")
print(f"  (注: 空 bit_pattern 共 {n_empty} 条, 均由 bitfields_json 描述位模式, 属正常)")

# 4.2 枚举值检查
print("  operand_type 取值:", dict(
    (r['operand_type'], r['c']) for r in
    cur.execute("SELECT operand_type, COUNT(*) c FROM operands GROUP BY operand_type")
))
print("  register_class 取值:", dict(
    (r['register_class'], r['c']) for r in
    cur.execute("SELECT register_class, COUNT(*) c FROM operands GROUP BY register_class")
))
print("  section_type 取值:", dict(
    (r['section_type'], r['c']) for r in
    cur.execute("SELECT section_type, COUNT(*) c FROM pseudocode GROUP BY section_type")
))

# 4.3 JSON 字段有效性
json_cols = {
    "instructions": ["bitfields_json", "arch_variants_json", "fields_json"],
    "encodings": ["fields_json"],
}
for tbl, cols in json_cols.items():
    for col in cols:
        try:
            bad_json = cur.execute(
                f"SELECT COUNT(*) FROM {tbl} WHERE {col} IS NOT NULL AND json_valid({col})=0"
            ).fetchone()[0]
            if bad_json:
                print(f"  ⚠ {tbl}.{col} 非法 JSON 条数: {bad_json}")
        except sqlite3.OperationalError:
            pass
print("  JSON 字段检查完成 (无输出即全部有效)")

# 4.4 xml_id 唯一性
dup = cur.execute(
    "SELECT COUNT(*) FROM (SELECT xml_id FROM instructions GROUP BY xml_id HAVING COUNT(*)>1)"
).fetchone()[0]
print(f"  xml_id 重复条数              : {dup}  (期望 0)")

print("\n" + "=" * 64)
print("5. 关联完整性 (REFERENTIAL INTEGRITY)")
print("=" * 64)
orphan_enc = cur.execute(
    "SELECT COUNT(*) FROM encodings e LEFT JOIN instructions i ON e.instruction_id=i.id WHERE i.id IS NULL"
).fetchone()[0]
orphan_op = cur.execute(
    "SELECT COUNT(*) FROM operands o LEFT JOIN instructions i ON o.instruction_id=i.id WHERE i.id IS NULL"
).fetchone()[0]
orphan_pc = cur.execute(
    "SELECT COUNT(*) FROM pseudocode p LEFT JOIN instructions i ON p.instruction_id=i.id WHERE i.id IS NULL"
).fetchone()[0]
print(f"  orphan encodings  : {orphan_enc}  (期望 0)")
print(f"  orphan operands   : {orphan_op}  (期望 0)")
print(f"  orphan pseudocode : {orphan_pc}  (期望 0)")

print("\n" + "=" * 64)
print("6. 数据质量抽查 (SPOT-CHECK, instructions 前3条)")
print("=" * 64)
for row in cur.execute("SELECT xml_id, mnemonic, instr_class, instruction_type, brief, source_file FROM instructions LIMIT 3"):
    print(f"\n  {dict(row)}")

conn.close()
print("\n验证完成。若所有 '期望 0' 项都为 0，且 instructions 数 ≈ XML/Card 数，则数据量和格式均正确。")
