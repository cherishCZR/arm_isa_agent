## BLR
_ARM A64 Instruction_

**Title**: BLR -- A64 | **Class**: `general` | **XML ID**: `BLR`

**Summary**: Branch with link to register

**Description**:
This instruction calls a subroutine at an address in a register,
setting register X30 to PC+4.

### Variant: `Integer`
- **Assembly**: `BLR  <Xn>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25 24 23 22  20  15  11 10  9   4  |
|--------------------------------------|
| 110 101 1   0   0   01  11111 0000 0   0   Rn  00000 |
```

#### Decode (A64.control.branch_reg.BLR_64_branch_reg)

```
constant integer n = UInt(Rn);
```

#### Execute (A64.control.branch_reg.BLR_64_branch_reg)

```
constant bits(64) target = X[n, 64];
if IsFeatureImplemented(FEAT_GCS) && GCSPCREnabled(PSTATE.EL) then
    AddGCSRecord(PC64 + 4);

// Value in BTypeNext will be used to set PSTATE.BTYPE
BTypeNext = '10';

X[30, 64] = PC64 + 4;

constant boolean branch_conditional = FALSE;
BranchTo(target, BranchType_INDCALL, branch_conditional);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose register holding the address to be branched to, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `blr.xml`
</details>