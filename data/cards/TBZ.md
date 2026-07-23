## TBZ
_ARM A64 Instruction_

**Title**: TBZ -- A64 | **Class**: `general` | **XML ID**: `TBZ`

**Summary**: Test bit and branch if zero

**Description**:
This instruction compares the value of a test bit with zero,
and conditionally branches to a label at a PC-relative offset if the
comparison is equal. It provides a hint that this is not a subroutine call
or return. This instruction does not affect condition flags.

### Variant: `14-bit signed PC-relative branch offset`
- **Assembly**: `TBZ  <R><t>, #<imm>, <label>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  25 24 23  18   4  |
|--------------------------|
| b5  01  101 1   0   b40 imm14 Rt  |
```

#### Decode (A64.control.testbranch.TBZ_only_testbranch)

```
constant integer t = UInt(Rt);

constant integer datasize = 32 << UInt(b5);
constant integer bit_pos = UInt(b5:b40);
constant bits(64) offset = SignExtend(imm14:'00', 64);
```

#### Execute (A64.control.testbranch.TBZ_only_testbranch)

```
constant bits(datasize) operand = X[t, datasize];
constant boolean branch_conditional = TRUE;
if operand<bit_pos> == '0' then
    BranchTo(PC64 + offset, BranchType_DIR, branch_conditional);
else
    BranchNotTaken(BranchType_DIR, branch_conditional);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<R>` | `unknown` | `b5` | Is a width specifier, |
| `<t>` | `unknown` | `Rt` | Is the number [0-30] of the general-purpose register to be tested or the name ZR (31), encoded in the "Rt" field. |
| `<imm>` | `immediate` | `b40:b5` | Is the bit number to be tested, in the range 0 to 63, encoded in "b5:b40". |
| `<label>` | `label` | `imm14` | Is the program label to be conditionally branched to. Its offset from the address of this instruction, in the range +/-32KB, is encoded as "imm14" tim |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | W |
| 1 | X |

---
<details><summary>Metadata</summary>

- branch-offset: `br14`
- isa: `A64`
- source: `tbz.xml`
</details>