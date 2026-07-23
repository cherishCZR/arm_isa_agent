## B
_ARM A64 Instruction_

**Title**: B -- A64 | **Class**: `general` | **XML ID**: `B_uncond`

**Summary**: Branch

**Description**:
This instruction branches unconditionally to a label at a PC-relative offset,
with a hint that this is not a subroutine call or return.

### Variant: `26-bit signed PC-relative branch offset`
- **Assembly**: `B  <label>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  25  |
|--------------|
| 0   00  101 imm26 |
```

#### Decode (A64.control.branch_imm.B_only_branch_imm)

```
constant bits(64) offset = SignExtend(imm26:'00', 64);
```

#### Execute (A64.control.branch_imm.B_only_branch_imm)

```
constant boolean branch_conditional = FALSE;
BranchTo(PC64 + offset, BranchType_DIR, branch_conditional);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<label>` | `label` | `imm26` | Is the program label to be unconditionally branched to. Its offset from the address of this instruction, in the range +/-128MB, is encoded as "imm26"  |

---
<details><summary>Metadata</summary>

- branch-offset: `br26`
- isa: `A64`
- source: `b_uncond.xml`
</details>