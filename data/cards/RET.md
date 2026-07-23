## RET
_ARM A64 Instruction_

**Title**: RET -- A64 | **Class**: `general` | **XML ID**: `RET`

**Summary**: Return from subroutine

**Description**:
This instruction branches unconditionally to an address in a register,
with a hint that this is a subroutine return.

### Variant: `Integer`
- **Assembly**: `RET  {<Xn>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25 24 23 22  20  15  11 10  9   4  |
|--------------------------------------|
| 110 101 1   0   0   10  11111 0000 0   0   Rn  00000 |
```

#### Decode (A64.control.branch_reg.RET_64R_branch_reg)

```
constant integer n = UInt(Rn);
```

#### Execute (A64.control.branch_reg.RET_64R_branch_reg)

```
bits(64) target = X[n, 64];
if IsFeatureImplemented(FEAT_GCS) && GCSPCREnabled(PSTATE.EL) then
    target = LoadCheckGCSRecord(target, GCSInstType_PRET);
    SetCurrentGCSPointer(GetCurrentGCSPointer() + 8);

// Value in BTypeNext will be used to set PSTATE.BTYPE
BTypeNext = '00';

constant boolean branch_conditional = FALSE;
BranchTo(target, BranchType_RET, branch_conditional);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose register holding the address to be branched to, encoded in the "Rn" field. Defaults to X30 if absent. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ret.xml`
</details>