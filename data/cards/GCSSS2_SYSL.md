## SYSL `[ALIAS]`
_ARM A64 Instruction_ (Alias of sysl.xml)

**Title**: GCSSS2 -- A64 | **Class**: `system` | **XML ID**: `GCSSS2_SYSL`

**Architecture**: `FEAT_GCS` (ARMv9.4)

**Summary**: Guarded Control Stack switch stack 2

**Description**:
This instruction validates that the most recent entry of
the Guarded Control Stack being switched to contains an In-progress cap entry,
stores a Valid cap entry to the Guarded Control Stack that is being switched
from, and sets Xt to the Guarded Control Stack pointer that is being
switched from.

### Variant: `System`
- **Assembly**: `GCSSS2  <Xt>`
- **Alias of**: `SYSL  <Xt>, #3, C7, C7, #3`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 1   01  011 0111 0111 011 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `GCSSS2`
- isa: `A64`
- source: `gcsss2_sysl.xml`
</details>