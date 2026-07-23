## PACIA
_ARM A64 Instruction_

**Title**: PACIA, PACIA1716, PACIASP, PACIAZ, PACIZA -- A64 | **Class**: `N/A` | **XML ID**: `PACIA`

**Architecture**: `FEAT_PAuth` (ARMv8.3)

**Summary**: Pointer Authentication Code for instruction address, using key A

**Description**:
This instruction computes and inserts a Pointer Authentication Code
for an instruction address, using a modifier and key A.

The address is:

The modifier is:

If FEAT_PAuth_LR is implemented and PSTATE.PACM is 1, then
PACIA1716 and PACIASP include a second modifier that is:

A PACIASP instruction has an implicit BTI instruction. The
implicit BTI instruction of a PACIASP instruction is always
compatible with PSTATE.BTYPE == 0b01
and PSTATE.BTYPE == 0b10.
Controls in SCTLR_ELx configure whether the
implicit BTI instruction of a PACIASP instruction is compatible with
PSTATE.BTYPE == 0b11.
For more information, see PSTATE.BTYPE.

### Variant: `Integer (PACIA_64P_dp_1src)` (PACIA)
- **Condition**: `Z == 0`
- **Assembly**: `PACIA  <Xd>, <Xn|SP>`
- **Fixed bits**: `Z`=`0`
- **Bit Pattern**: `?????????????0??????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  13 12   9   4  |
|--------------------------------|
| 1   1   0   11010110 00001 00  Z   000 Rn  Rd  |
```

#### Decode (A64.dpreg.dp_1src.PACIA_64P_dp_1src)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_UNDEF);
boolean source_is_sp = FALSE;
constant boolean pacia1716 = FALSE;
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

if Z == '0' then // PACIA
    if n == 31 then source_is_sp = TRUE;
else // PACIZA
    if n != 31 then EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.dpreg.dp_1src.PACIA_64P_dp_1src)

```
if source_is_sp then
    if IsFeatureImplemented(FEAT_PAuth_LR) && PSTATE.PACM == '1' then
        X[d, 64] = AddPACIA2(X[d, 64], SP[64], PC64);
    else
        X[d, 64] = AddPACIA(X[d, 64], SP[64]);
else
    if IsFeatureImplemented(FEAT_PAuth_LR) && PSTATE.PACM == '1' && pacia1716 then
        X[d, 64] = AddPACIA2(X[d, 64], X[n, 64], X[15, 64]);
    else
        X[d, 64] = AddPACIA(X[d, 64], X[n, 64]);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `n == 31` |

### Variant: `Integer (PACIZA_64Z_dp_1src)` (PACIZA)
- **Condition**: `Z == 1 && Rn == 11111`
- **Assembly**: `PACIZA  <Xd>`
- **Fixed bits**: `Z`=`1`, `Rn`=`11111`
- **Bit Pattern**: `?????11111???1??????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  13 12   9   4  |
|--------------------------------|
| 1   1   0   11010110 00001 00  Z   000 Rn  Rd  |
```

### Variant: `System (PACIA1716_HI_hints)` (PACIA1716)
- **Condition**: `CRm == 0001 && op2 == 000`
- **Assembly**: `PACIA1716`
- **Fixed bits**: `CRm`=`0`, `op2`=`0`
- **Bit Pattern**: `?????0???0??????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  11   7   4  |
|--------------|
| 11010101000000110010 00x1 00x 11111 |
```

#### Decode (A64.control.hints.PACIA1716_HI_hints)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_NOP);
integer d;
integer n;
boolean source_is_sp = FALSE;
boolean pacia1716 = FALSE;

case CRm:op2 of
    when '0011 000' // PACIAZ
        d = 30;
        n = 31;
    when '0011 001' // PACIASP
        d = 30;
        source_is_sp = TRUE;
        if IsFeatureImplemented(FEAT_BTI) then
            // Check for branch target compatibility between PSTATE.BTYPE
            // and implicit branch target of PACIASP instruction.
            SetBTypeCompatible(BTypeCompatible_PACIXSP());
    when '0001 000' // PACIA1716
        d = 17;
        n = 16;
        pacia1716 = TRUE;
```

### Variant: `System (PACIASP_HI_hints)` (PACIASP)
- **Condition**: `CRm == 0011 && op2 == 001`
- **Assembly**: `PACIASP`
- **Fixed bits**: `CRm`=`1`, `op2`=`1`
- **Bit Pattern**: `?????1???1??????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  11   7   4  |
|--------------|
| 11010101000000110010 00x1 00x 11111 |
```

### Variant: `System (PACIAZ_HI_hints)` (PACIAZ)
- **Condition**: `CRm == 0011 && op2 == 000`
- **Assembly**: `PACIAZ`
- **Fixed bits**: `CRm`=`1`, `op2`=`0`
- **Bit Pattern**: `?????0???1??????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  11   7   4  |
|--------------|
| 11010101000000110010 00x1 00x 11111 |
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
- source: `pacia.xml`
</details>