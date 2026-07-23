## BC
_ARM A64 Instruction_

**Title**: BC.cond -- A64 | **Class**: `general` | **XML ID**: `BC_cond`

**Architecture**: `FEAT_HBC` (ARMv8.8)

**Summary**: Branch consistent conditionally

**Description**:
This instruction branches conditionally to a label at a PC-relative
offset, with a hint that this branch will behave very consistently
and is very unlikely to change direction.

### Variant: `19-bit signed PC-relative branch offset`
- **Assembly**: `BC.<cond>  <label>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23   4  3  |
|--------------------|
| 010 101 00  imm19 1   cond |
```

#### Decode (A64.control.condbranch.BC_only_condbranch)

```
if !IsFeatureImplemented(FEAT_HBC) then EndOfDecode(Decode_UNDEF);
constant bits(64) offset = SignExtend(imm19:'00', 64);
constant bits(4) condition = cond;
```

#### Execute (A64.control.condbranch.BC_only_condbranch)

```
constant boolean branch_conditional = TRUE;
if ConditionHolds(condition) then
    BranchTo(PC64 + offset, BranchType_DIR, branch_conditional);
else
    BranchNotTaken(BranchType_DIR, branch_conditional);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_HBC)` |

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
- source: `bc_cond.xml`
</details>