## B
_ARM A64 Instruction_

**Title**: B.cond -- A64 | **Class**: `general` | **XML ID**: `B_cond`

**Summary**: Branch conditionally

**Description**:
This instruction branches conditionally to a label at a PC-relative
offset, with a hint that this is not a subroutine call or return.

### Variant: `19-bit signed PC-relative branch offset`
- **Assembly**: `B.<cond>  <label>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23   4  3  |
|--------------------|
| 010 101 00  imm19 0   cond |
```

#### Decode (A64.control.condbranch.B_only_condbranch)

```
constant bits(64) offset = SignExtend(imm19:'00', 64);
constant bits(4) condition = cond;
```

#### Execute (A64.control.condbranch.B_only_condbranch)

```
constant boolean branch_conditional = TRUE;
if ConditionHolds(condition) then
    BranchTo(PC64 + offset, BranchType_DIR, branch_conditional);
else
    BranchNotTaken(BranchType_DIR, branch_conditional);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<cond>` | `condition` | `cond` | Is one of the standard conditions, encoded in the standard way, and |
| `<label>` | `label` | `imm19` | Is the program label to be conditionally branched to. Its offset from the address of this instruction, in the range +/-1MB, is encoded as "imm19" time |

**<cond> Value Table**:

| bitfield | symbol |
|---|---|
| 0000 | EQ |
| 0001 | NE |
| 0010 | CS |
| 0011 | CC |
| 0100 | MI |
| 0101 | PL |
| 0110 | VS |
| 0111 | VC |
| 1000 | HI |
| 1001 | LS |
| 1010 | GE |
| 1011 | LT |
| 1100 | GT |
| 1101 | LE |
| 1110 | AL |
| 1111 | NV |

---
<details><summary>Metadata</summary>

- branch-offset: `br19`
- compare-with: `cmp-cond`
- isa: `A64`
- source: `b_cond.xml`
</details>