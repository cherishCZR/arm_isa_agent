## CSDB
_ARM A64 Instruction_

**Title**: CSDB -- A64 | **Class**: `system` | **XML ID**: `CSDB`

**Summary**: Consumption of speculative data barrier

**Description**:
This instruction is a memory barrier
that controls speculative execution arising from data value prediction.
For more information and details of the semantics, see
Consumption of Speculative Data Barrier (CSDB).

### Variant: `System`
- **Assembly**: `CSDB`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0010 100 11111 |
```

#### Decode (A64.control.hints.CSDB_HI_hints)

```
// Empty.
```

#### Execute (A64.control.hints.CSDB_HI_hints)

```
ConsumptionOfSpeculativeDataBarrier();
```

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `csdb.xml`
</details>