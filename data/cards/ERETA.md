## ERETA
_ARM A64 Instruction_

**Title**: ERETAA, ERETAB -- A64 | **Class**: `general` | **XML ID**: `ERETA`

**Architecture**: `FEAT_PAuth` (ARMv8.3)

**Summary**: Exception return, with pointer authentication

**Description**:
This instruction authenticates the address in ELR, using SP as the
modifier and the specified key, restores
PSTATE from the SPSR for the current
Exception level, and branches to the authenticated address.

Key A is used for ERETAA.
Key B is used for ERETAB.

If the authentication passes, the PE continues execution at the
target of the branch.
For information on behavior if the authentication fails, see
Faulting on pointer authentication.

The authenticated address is not written back to ELR.

The SPSR is checked for the current Exception level for an illegal return event.
See Illegal exception returns from AArch64 state.

ERETAA and ERETAB are UNDEFINED at EL0.

### Variant: `Integer (ERETAA_64E_branch_reg)` (ERETAA)
- **Condition**: `M == 0`
- **Assembly**: `ERETAA`
- **Fixed bits**: `M`=`0`
- **Bit Pattern**: `??????????0?????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  24  20  15  11 10  9   4  |
|--------------------------|
| 1101011 0100 11111 0000 1   M   11111 11111 |
```

#### Decode (A64.control.branch_reg.ERETAA_64E_branch_reg)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_UNDEF);

constant boolean pac = TRUE;
constant boolean use_key_a = (M == '0');
constant boolean auth_then_branch = TRUE;
```

#### Execute (A64.control.branch_reg.ERETAA_64E_branch_reg)

```
if PSTATE.EL == EL0 then UNDEFINED;
AArch64.CheckForERetTrap(pac, use_key_a);
bits(64) target = ELR_ELx[];
constant bits(64) modifier = SP[64];

if use_key_a then
    target = AuthIA(target, modifier, auth_then_branch);
else
    target = AuthIB(target, modifier, auth_then_branch);

AArch64.ExceptionReturn(target, SPSR_ELx[]);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth)` |

### Variant: `Integer (ERETAB_64E_branch_reg)` (ERETAB)
- **Condition**: `M == 1`
- **Assembly**: `ERETAB`
- **Fixed bits**: `M`=`1`
- **Bit Pattern**: `??????????1?????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  24  20  15  11 10  9   4  |
|--------------------------|
| 1101011 0100 11111 0000 1   M   11111 11111 |
```

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ereta.xml`
</details>