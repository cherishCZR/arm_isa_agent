## BRA
_ARM A64 Instruction_

**Title**: BRAA, BRAAZ, BRAB, BRABZ -- A64 | **Class**: `general` | **XML ID**: `BRA`

**Architecture**: `FEAT_PAuth` (ARMv8.3)

**Summary**: Branch to register, with pointer authentication

**Description**:
This instruction authenticates the address in the general-purpose
register that is specified by <Xn>, using a modifier and
the specified key, and branches to the authenticated address.

The modifier is:

Key A is used for BRAA and BRAAZ. Key B is used for
BRAB and BRABZ.

If the authentication passes, the PE continues execution at the
target of the branch.
For information on behavior if the authentication fails, see
Faulting on pointer authentication.

The authenticated address is not written back to the general-purpose
register.

### Variant: `Integer (BRAA_64P_branch_reg)` (Key A, register modifier)
- **Condition**: `Z == 1 && M == 0`
- **Assembly**: `BRAA  <Xn>, <Xm|SP>`
- **Fixed bits**: `Z`=`1`, `M`=`0`
- **Bit Pattern**: `??????????0?????????????1???????`
**Encoding Diagram (32-bit)**:

```text
| 31  24 23 22  20  15  11 10  9   4  |
|--------------------------------|
| 1101011 Z   0   00  11111 0000 1   M   Rn  Rm  |
```

#### Decode (A64.control.branch_reg.BRAA_64P_branch_reg)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_UNDEF);
if Z == '0' && Rm != '11111' then EndOfDecode(Decode_UNDEF);

constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant boolean use_key_a = (M == '0');
constant boolean source_is_sp = ((Z == '1') && (m == 31));
constant boolean auth_then_branch = TRUE;
```

#### Execute (A64.control.branch_reg.BRAA_64P_branch_reg)

```
bits(64) target = X[n, 64];
constant bits(64) modifier = if source_is_sp then SP[64] else X[m, 64];

if use_key_a then
    target = AuthIA(target, modifier, auth_then_branch);
else
    target = AuthIB(target, modifier, auth_then_branch);
// Value in BTypeNext will be used to set PSTATE.BTYPE
if InGuardedPage then
    if n == 16 || n == 17 then
        BTypeNext = '01';
    else
        BTypeNext = '11';
else
    BTypeNext = '01';

constant boolean branch_conditional = FALSE;
BranchTo(target, BranchType_INDIR, branch_conditional);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth)` |
| 🚫 ENCODING_UNDEF | `Z != '0' \|\| Rm == '11111'` |

### Variant: `Integer (BRAAZ_64_branch_reg)` (Key A, zero modifier)
- **Condition**: `Z == 0 && M == 0 && Rm == 11111`
- **Assembly**: `BRAAZ  <Xn>`
- **Fixed bits**: `Z`=`0`, `M`=`0`, `Rm`=`11111`
- **Bit Pattern**: `11111?????0?????????????0???????`
**Encoding Diagram (32-bit)**:

```text
| 31  24 23 22  20  15  11 10  9   4  |
|--------------------------------|
| 1101011 Z   0   00  11111 0000 1   M   Rn  Rm  |
```

### Variant: `Integer (BRAB_64P_branch_reg)` (Key B, register modifier)
- **Condition**: `Z == 1 && M == 1`
- **Assembly**: `BRAB  <Xn>, <Xm|SP>`
- **Fixed bits**: `Z`=`1`, `M`=`1`
- **Bit Pattern**: `??????????1?????????????1???????`
**Encoding Diagram (32-bit)**:

```text
| 31  24 23 22  20  15  11 10  9   4  |
|--------------------------------|
| 1101011 Z   0   00  11111 0000 1   M   Rn  Rm  |
```

### Variant: `Integer (BRABZ_64_branch_reg)` (Key B, zero modifier)
- **Condition**: `Z == 0 && M == 1 && Rm == 11111`
- **Assembly**: `BRABZ  <Xn>`
- **Fixed bits**: `Z`=`0`, `M`=`1`, `Rm`=`11111`
- **Bit Pattern**: `11111?????1?????????????0???????`
**Encoding Diagram (32-bit)**:

```text
| 31  24 23 22  20  15  11 10  9   4  |
|--------------------------------|
| 1101011 Z   0   00  11111 0000 1   M   Rn  Rm  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose register holding the address to be branched to, encoded in the "Rn" field. |
| `<Xm\|SP>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the general-purpose source register or stack pointer holding the modifier, encoded in the "Rm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bra.xml`
</details>