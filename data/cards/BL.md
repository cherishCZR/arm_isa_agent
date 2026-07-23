## BL
_ARM A64 Instruction_

**Title**: BL -- A64 | **Class**: `general` | **XML ID**: `BL`

**Summary**: Branch with link

**Description**:
This instruction branches to a PC-relative offset, setting
register X30 to PC+4. It provides a hint that this is a subroutine
call.

### Variant: `26-bit signed PC-relative branch offset`
- **Assembly**: `BL  <label>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  25  |
|--------------|
| 1   00  101 imm26 |
```

#### Decode (A64.control.branch_imm.BL_only_branch_imm)

```
constant bits(64) offset = SignExtend(imm26:'00', 64);
constant integer d = 30;
```

#### Execute (A64.control.branch_imm.BL_only_branch_imm)

```
if IsFeatureImplemented(FEAT_GCS) && GCSPCREnabled(PSTATE.EL) then
    AddGCSRecord(PC64 + 4);
X[d, 64] = PC64 + 4;

constant boolean branch_conditional = FALSE;
BranchTo(PC64 + offset, BranchType_DIRCALL, branch_conditional);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<label>` | `label` | `imm26` | Is the program label to be unconditionally branched to. Its offset from the address of this instruction, in the range +/-128MB, is encoded as "imm26"  |

---
<details><summary>Metadata</summary>

- branch-offset: `br26`
- isa: `A64`
- source: `bl.xml`
</details>