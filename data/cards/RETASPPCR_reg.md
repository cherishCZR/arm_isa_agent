## RETASPPCR_reg
_ARM A64 Instruction_

**Title**: RETAASPPCR, RETABSPPCR -- A64 | **Class**: `general` | **XML ID**: `RETASPPCR_reg`

**Architecture**: `FEAT_PAuth_LR` (ARMv9.5)

**Summary**: Return from subroutine, with enhanced pointer authentication using a register

**Description**:
This instruction authenticates the address that is held in LR, using
SP as the first modifier,
the value in the specified register as the second modifier,
and the specified key, and branches to the authenticated address,
with a hint that this instruction is a subroutine return.

Key A is used for RETAASPPCR. Key B is used for RETABSPPCR.

If the authentication passes, the PE continues execution at the
target of the branch.
For information on behavior if the authentication fails, see
Faulting on pointer authentication.

The authenticated address is not written back to LR.

### Variant: `Integer (RETAASPPCR_64M_branch_reg)` (RETAASPPCR)
- **Condition**: `M == 0`
- **Assembly**: `RETAASPPCR  <Xm>`
- **Fixed bits**: `M`=`0`
- **Bit Pattern**: `??????????0?????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  24  20  15  10  9   4  |
|-----------------------|
| 1101011 0010 11111 00001 M   11111 ?   |
```

#### Decode (A64.control.branch_reg.RETAASPPCR_64M_branch_reg)

```
if !IsFeatureImplemented(FEAT_PAuth_LR) then EndOfDecode(Decode_UNDEF);
constant integer m = UInt(Rm);
constant boolean use_key_a = M == '0';
constant boolean auth_then_branch = TRUE;
```

#### Execute (A64.control.branch_reg.RETAASPPCR_64M_branch_reg)

```
GCSInstruction inst_type;
bits(64) target = X[30, 64];

constant bits(64) modifier = SP[64];
constant bits(64) modifier2 = X[m, 64];

if use_key_a then
    target = AuthIA2(target, modifier, modifier2, auth_then_branch);
else
    target = AuthIB2(target, modifier, modifier2, auth_then_branch);

if IsFeatureImplemented(FEAT_GCS) && GCSPCREnabled(PSTATE.EL) then
    inst_type = if use_key_a then GCSInstType_PRETAA else GCSInstType_PRETAB;
    target = LoadCheckGCSRecord(target, inst_type);
    SetCurrentGCSPointer(GetCurrentGCSPointer() + 8);

// Value in BTypeNext will be used to set PSTATE.BTYPE
BTypeNext = '00';

constant boolean branch_conditional = FALSE;
BranchTo(target, BranchType_RET, branch_conditional);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth_LR)` |

### Variant: `Integer (RETABSPPCR_64M_branch_reg)` (RETABSPPCR)
- **Condition**: `M == 1`
- **Assembly**: `RETABSPPCR  <Xm>`
- **Fixed bits**: `M`=`1`
- **Bit Pattern**: `??????????1?????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  24  20  15  10  9   4  |
|-----------------------|
| 1101011 0010 11111 00001 M   11111 ?   |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the general-purpose source register, encoded in the "Rm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `retasppcr_reg.xml`
</details>