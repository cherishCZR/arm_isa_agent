## ISB
_ARM A64 Instruction_

**Title**: ISB -- A64 | **Class**: `system` | **XML ID**: `ISB`

**Summary**: Instruction synchronization barrier

**Description**:
This instruction flushes the pipeline in the PE
and is a context synchronization event. For more information, see
Instruction Synchronization Barrier (ISB).

### Variant: `System`
- **Assembly**: `ISB  {<option>|#<imm>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7  6   4  |
|-----------------------|
| 110 101 01000000110011 CRm 1   10  11111 |
```

#### Decode (A64.control.barriers.ISB_BI_barriers)

```
// No additional decoding required
```

#### Execute (A64.control.barriers.ISB_BI_barriers)

```
InstructionSynchronizationBarrier();

if IsFeatureImplemented(FEAT_BRBE) && BRBEBranchOnISB() then
    BRBEISB();
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<option>` | `unknown` | `CRm` | Specifies an optional limitation on the barrier operation. Values are: All other encodings of "CRm" are reserved. The corresponding instructions execu |
| `<imm>` | `immediate` | `CRm` | Is an optional 4-bit unsigned immediate, in the range 0 to 15, defaulting to 15 and encoded in the "CRm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `isb.xml`
</details>