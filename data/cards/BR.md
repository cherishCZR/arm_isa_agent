## BR
_ARM A64 Instruction_

**Title**: BR -- A64 | **Class**: `general` | **XML ID**: `BR`

**Summary**: Branch to register

**Description**:
This instruction branches unconditionally to an address in a register,
with a hint that this is not a subroutine return.

### Variant: `Integer`
- **Assembly**: `BR  <Xn>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25 24 23 22  20  15  11 10  9   4  |
|--------------------------------------|
| 110 101 1   0   0   00  11111 0000 0   0   Rn  00000 |
```

#### Decode (A64.control.branch_reg.BR_64_branch_reg)

```
constant integer n = UInt(Rn);
```

#### Execute (A64.control.branch_reg.BR_64_branch_reg)

```
constant bits(64) target = X[n, 64];
// Value in BTypeNext will be used to set PSTATE.BTYPE
if InGuardedPage then
    if n == 16 || n == 17 then
        BTypeNext = '01';
    else
        BTypeNext = '11';
else
    BTypeNext = '01';

constant boolean branch_conditional = FALSE;
BranchTo(target, BranchType_INDIR, branch_conditional);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose register holding the address to be branched to, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `br.xml`
</details>