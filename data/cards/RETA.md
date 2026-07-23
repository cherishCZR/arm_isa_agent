## RETA
_ARM A64 Instruction_

**Title**: RETAA, RETAB -- A64 | **Class**: `general` | **XML ID**: `RETA`

**Architecture**: `FEAT_PAuth` (ARMv8.3)

**Summary**: Return from subroutine, with pointer authentication

**Description**:
This instruction authenticates the address that is held in LR, using
SP as the modifier and the specified key, and branches to the
authenticated address, with a hint that this instruction is a
subroutine return.

Key A is used for RETAA. Key B is used for RETAB.

If the authentication passes, the PE continues execution at the
target of the branch.
For information on behavior if the authentication fails, see
Faulting on pointer authentication.

The authenticated address is not written back to LR.

If FEAT_PAuth_LR is implemented and PSTATE.PACM is 1, then
RETAA and RETAB include a second modifier that is in X16.

### Variant: `Integer (RETAA_64E_branch_reg)` (RETAA)
- **Condition**: `M == 0`
- **Assembly**: `RETAA`
- **Fixed bits**: `M`=`0`
- **Bit Pattern**: `??????????0?????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  24 23 22  20  15  11 10  9   4  |
|--------------------------------|
| 1101011 0   0   10  11111 0000 1   M   11111 11111 |
```

#### Decode (A64.control.branch_reg.RETAA_64E_branch_reg)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_UNDEF);

constant boolean use_key_a = (M == '0');
constant boolean auth_then_branch = TRUE;
```

#### Execute (A64.control.branch_reg.RETAA_64E_branch_reg)

```
GCSInstruction inst_type;
bits(64) target = X[30, 64];

constant bits(64) modifier = SP[64];
bits(64) modifier2;
boolean use_modifier2 = FALSE;
if IsFeatureImplemented(FEAT_PAuth_LR) && PSTATE.PACM == '1' then
    modifier2 = X[16, 64];
    use_modifier2 = TRUE;

if use_key_a then
    if use_modifier2 && IsFeatureImplemented(FEAT_PAuth_LR) then
        target = AuthIA2(target, modifier, modifier2, auth_then_branch);
    else
        target = AuthIA(target, modifier, auth_then_branch);
else
    if use_modifier2 && IsFeatureImplemented(FEAT_PAuth_LR) then
        target = AuthIB2(target, modifier, modifier2, auth_then_branch);
    else
        target = AuthIB(target, modifier, auth_then_branch);

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
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth)` |

### Variant: `Integer (RETAB_64E_branch_reg)` (RETAB)
- **Condition**: `M == 1`
- **Assembly**: `RETAB`
- **Fixed bits**: `M`=`1`
- **Bit Pattern**: `??????????1?????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  24 23 22  20  15  11 10  9   4  |
|--------------------------------|
| 1101011 0   0   10  11111 0000 1   M   11111 11111 |
```

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `reta.xml`
</details>