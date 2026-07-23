## CBZ
_ARM A64 Instruction_

**Title**: CBZ -- A64 | **Class**: `general` | **XML ID**: `CBZ`

**Summary**: Compare and branch on zero

**Description**:
This instruction compares the value in a register with zero,
and conditionally branches to a label at a PC-relative offset if the
comparison is equal. It provides a hint that this is not a subroutine
call or return. This instruction does not affect condition flags.

### Variant: `19-bit signed PC-relative branch offset (CBZ_32_compbranch)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `CBZ  <Wt>, <label>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  24 23   4  |
|-----------------|
| sf  011010 0   imm19 Rt  |
```

#### Decode (A64.control.compbranch.CBZ_32_compbranch)

```
constant integer t = UInt(Rt);
constant integer datasize = 32 << UInt(sf);
constant bits(64) offset = SignExtend(imm19:'00', 64);
```

#### Execute (A64.control.compbranch.CBZ_32_compbranch)

```
constant boolean branch_conditional = TRUE;
constant bits(datasize) operand1 = X[t, datasize];
if IsZero(operand1) then
    BranchTo(PC64 + offset, BranchType_DIR, branch_conditional);
else
    BranchNotTaken(BranchType_DIR, branch_conditional);
```

### Variant: `19-bit signed PC-relative branch offset (CBZ_64_compbranch)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `CBZ  <Xt>, <label>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  24 23   4  |
|-----------------|
| sf  011010 0   imm19 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |
| `<label>` | `label` | `imm19` | Is the program label to be conditionally branched to. Its offset from the address of this instruction, in the range +/-1MB, is encoded as "imm19" time |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- branch-offset: `br19`
- compare-with: `cmp-zero`
- isa: `A64`
- source: `cbz.xml`
</details>