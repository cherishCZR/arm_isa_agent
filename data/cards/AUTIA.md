## AUTIA
_ARM A64 Instruction_

**Title**: AUTIA, AUTIA1716, AUTIASP, AUTIAZ, AUTIZA -- A64 | **Class**: `N/A` | **XML ID**: `AUTIA`

**Architecture**: `FEAT_PAuth` (ARMv8.3)

**Summary**: Authenticate instruction address, using key A

**Description**:
This instruction authenticates an instruction address, using a modifier and key A.

If the authentication passes, the upper bits of the address are
restored to enable subsequent use of the address.
For information on behavior if the authentication fails, see
Faulting on pointer authentication.

The address is:

The modifier is:

If FEAT_PAuth_LR is implemented and PSTATE.PACM is 1, then
AUTIA1716 and AUTIASP include a second modifier that is:

### Variant: `Integer (AUTIA_64P_dp_1src)` (AUTIA)
- **Condition**: `Z == 0`
- **Assembly**: `AUTIA  <Xd>, <Xn|SP>`
- **Fixed bits**: `Z`=`0`
- **Bit Pattern**: `?????????????0??????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  13 12   9   4  |
|--------------------------------|
| 1   1   0   11010110 00001 00  Z   100 Rn  Rd  |
```

#### Decode (A64.dpreg.dp_1src.AUTIA_64P_dp_1src)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_UNDEF);
if Z == '1' && Rn != '11111' then EndOfDecode(Decode_UNDEF);
constant boolean autia1716 = FALSE;
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant boolean auth_combined = FALSE;

constant boolean source_is_sp = Z == '0' && n == 31;
```

#### Execute (A64.dpreg.dp_1src.AUTIA_64P_dp_1src)

```
if source_is_sp then
    if IsFeatureImplemented(FEAT_PAuth_LR) && PSTATE.PACM == '1' then
        X[d, 64] = AuthIA2(X[d, 64], SP[64], X[16, 64], auth_combined);
    else
        X[d, 64] = AuthIA(X[d, 64], SP[64], auth_combined);
else
    if IsFeatureImplemented(FEAT_PAuth_LR) && PSTATE.PACM == '1' && autia1716 then
        X[d, 64] = AuthIA2(X[d, 64], X[n, 64], X[15, 64], auth_combined);
    else
        X[d, 64] = AuthIA(X[d, 64], X[n, 64], auth_combined);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `Z != '1' \|\| Rn == '11111'` |

### Variant: `Integer (AUTIZA_64Z_dp_1src)` (AUTIZA)
- **Condition**: `Z == 1 && Rn == 11111`
- **Assembly**: `AUTIZA  <Xd>`
- **Fixed bits**: `Z`=`1`, `Rn`=`11111`
- **Bit Pattern**: `?????11111???1??????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  13 12   9   4  |
|--------------------------------|
| 1   1   0   11010110 00001 00  Z   100 Rn  Rd  |
```

### Variant: `System (AUTIA1716_HI_hints)` (AUTIA1716)
- **Condition**: `CRm == 0001 && op2 == 100`
- **Assembly**: `AUTIA1716`
- **Fixed bits**: `CRm`=`0`, `op2`=`0`
- **Bit Pattern**: `?????0???0??????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  11   7   4  |
|--------------|
| 11010101000000110010 00x1 10x 11111 |
```

#### Decode (A64.control.hints.AUTIA1716_HI_hints)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_NOP);
integer d;
integer n;
boolean source_is_sp = FALSE;
boolean autia1716 = FALSE;
constant boolean auth_combined = FALSE;

case CRm:op2 of
    when '0011 100' // AUTIAZ
        d = 30;
        n = 31;
    when '0011 101' // AUTIASP
        d = 30;
        source_is_sp = TRUE;
    when '0001 100' // AUTIA1716
        d = 17;
        n = 16;
        autia1716 = TRUE;
```

### Variant: `System (AUTIASP_HI_hints)` (AUTIASP)
- **Condition**: `CRm == 0011 && op2 == 101`
- **Assembly**: `AUTIASP`
- **Fixed bits**: `CRm`=`1`, `op2`=`1`
- **Bit Pattern**: `?????1???1??????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  11   7   4  |
|--------------|
| 11010101000000110010 00x1 10x 11111 |
```

### Variant: `System (AUTIAZ_HI_hints)` (AUTIAZ)
- **Condition**: `CRm == 0011 && op2 == 100`
- **Assembly**: `AUTIAZ`
- **Fixed bits**: `CRm`=`1`, `op2`=`0`
- **Bit Pattern**: `?????0???1??????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  11   7   4  |
|--------------|
| 11010101000000110010 00x1 10x 11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register or stack pointer, encoded in the "Rn" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `autia.xml`
</details>