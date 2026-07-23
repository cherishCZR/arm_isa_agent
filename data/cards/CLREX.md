## CLREX
_ARM A64 Instruction_

**Title**: CLREX -- A64 | **Class**: `system` | **XML ID**: `CLREX`

**Summary**: Clear exclusive

**Description**:
This instruction clears the local monitor of the executing PE.

### Variant: `System`
- **Assembly**: `CLREX  {#<imm>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110011 CRm 010 11111 |
```

#### Decode (A64.control.barriers.CLREX_BN_barriers)

```
// CRm field is ignored
```

#### Execute (A64.control.barriers.CLREX_BN_barriers)

```
ClearExclusiveLocal(ProcessorID());
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<imm>` | `immediate` | `CRm` | Is an optional 4-bit unsigned immediate, in the range 0 to 15, defaulting to 15 and encoded in the "CRm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `clrex.xml`
</details>