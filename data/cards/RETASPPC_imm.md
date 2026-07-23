## RETASPPC_imm
_ARM A64 Instruction_

**Title**: RETAASPPC, RETABSPPC -- A64 | **Class**: `general` | **XML ID**: `RETASPPC_imm`

**Architecture**: `FEAT_PAuth_LR` (ARMv9.5)

**Summary**: Return from subroutine, with enhanced pointer authentication using an immediate offset

**Description**:
This instruction authenticates the address that is held in LR, using
SP as the first modifier,
the specified immediate subtracted from PC as the second modifier,
and the specified key, and branches to the authenticated address,
with a hint that this instruction is a subroutine return.

Key A is used for RETAASPPC. Key B is used for RETABSPPC.

If the authentication passes, the PE continues execution at the
target of the branch.
For information on behavior if the authentication fails, see
Faulting on pointer authentication.

The authenticated address is not written back to LR.

### Variant: `Integer (RETAASPPC_only_miscbranch)` (RETAASPPC)
- **Condition**: `opc == 000`
- **Assembly**: `RETAASPPC  <label>`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `?????????????????????0??????????`
**Encoding Diagram (32-bit)**:

```text
| 31  23  20   4  |
|--------------|
| 01010101 00x imm16 11111 |
```

#### Decode (A64.control.miscbranch.RETAASPPC_only_miscbranch)

```
if !IsFeatureImplemented(FEAT_PAuth_LR) then EndOfDecode(Decode_UNDEF);

constant boolean use_key_a = opc<0> == '0';
constant bits(64) offset = ZeroExtend(imm16:'00', 64);
constant boolean auth_then_branch = TRUE;
```

#### Execute (A64.control.miscbranch.RETAASPPC_only_miscbranch)

```
GCSInstruction inst_type;
bits(64) target = X[30, 64];

constant bits(64) modifier = SP[64];
constant bits(64) modifier2 = PC64 - offset;

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

### Variant: `Integer (RETABSPPC_only_miscbranch)` (RETABSPPC)
- **Condition**: `opc == 001`
- **Assembly**: `RETABSPPC  <label>`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `?????????????????????1??????????`
**Encoding Diagram (32-bit)**:

```text
| 31  23  20   4  |
|--------------|
| 01010101 00x imm16 11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<label>` | `label` | `imm16` | Is the program label whose address is to be calculated. Its negative offset from the address of this instruction, a multiple of 4 in the range -262140 |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `retasppc_imm.xml`
</details>