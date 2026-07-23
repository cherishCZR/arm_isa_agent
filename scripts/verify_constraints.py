"""验证 constraints 提取结果."""
import sqlite3

conn = sqlite3.connect("data/sqlite/isa_kb.db")
cur = conn.cursor()

print("=== Constraint type distribution ===")
for row in cur.execute("SELECT constraint_type, COUNT(*) c FROM constraints GROUP BY constraint_type ORDER BY c DESC"):
    print(f"  {row[0]:30s} : {row[1]:5d}")

print()
print("=== Sample FEATURE_GATE constraints ===")
for row in cur.execute("""
    SELECT c.constraint_type, c.condition, c.description, i.mnemonic, i.xml_id
    FROM constraints c JOIN instructions i ON c.instruction_id=i.id
    WHERE c.constraint_type='FEATURE_GATE'
    ORDER BY i.mnemonic LIMIT 8
"""):
    mnemonic = row[3] or row[4]
    cond = row[1] or "N/A"
    desc = (row[2] or "")[:120]
    print(f"  [{row[0]}] {mnemonic:15s} | condition: {cond:35s} | {desc}")

print()
print("=== Sample CONSTRAINED_UNPREDICTABLE ===")
for row in cur.execute("""
    SELECT c.constraint_type, c.condition, c.description, i.mnemonic, i.xml_id
    FROM constraints c JOIN instructions i ON c.instruction_id=i.id
    WHERE c.constraint_type='CONSTRAINED_UNPREDICTABLE'
    LIMIT 6
"""):
    mnemonic = row[3] or row[4]
    cond = row[1] or "N/A"
    desc = (row[2] or "")[:150]
    print(f"  [{row[0]}] {mnemonic:15s} | condition: {cond:60s} | {desc}")

print()
print("=== Sample DECODE_FALLBACK ===")
for row in cur.execute("""
    SELECT c.constraint_type, c.condition, c.description, i.mnemonic, i.xml_id
    FROM constraints c JOIN instructions i ON c.instruction_id=i.id
    WHERE c.constraint_type='DECODE_FALLBACK'
    LIMIT 5
"""):
    mnemonic = row[3] or row[4]
    cond = row[1] or "N/A"
    desc = (row[2] or "")[:100]
    print(f"  [{row[0]}] {mnemonic:15s} | condition: {cond:35s} | {desc}")

conn.close()
print("\nDone.")
