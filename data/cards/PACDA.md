## PACDA
_ARM A64 Instruction_

**Title**: PACDA, PACDZA -- A64 | **Class**: `general` | **XML ID**: `PACDA`

**Architecture**: `FEAT_PAuth` (ARMv8.3)

**Summary**: Pointer Authentication Code for data address, using key A

**Description**:
This instruction computes and inserts a Pointer Authentication Code
for a data address, using a modifier and key A.

The address is in the general-purpose register that is specified by
<Xd>.

The modifier is:

### Variant: `Integer (PACDA_64P_dp_1src)` (PACDA)
- **Condition**: `Z == 0`
- **Assembly**: `PACDA  <Xd>, <Xn|SP>`
- **Fixed bits**: `Z`=`0`
- **Bit Pattern**: `?????????????0??????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  13 12   9   4  |
|--------------------------------|
| 1   1   0   11010110 00001 00  Z   010 Rn  Rd  |
```

#### Decode (A64.dpreg.dp_1src.PACDA_64P_dp_1src)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_UNDEF);

boolean source_is_sp = FALSE;
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

if Z == '0' then // PACDA
    if n == 31 then source_is_sp = TRUE;
else // PACDZA
    if n != 31 then EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.dpreg.dp_1src.PACDA_64P_dp_1src)

```
if source_is_sp then
    X[d, 64] = AddPACDA(X[d, 64], SP[64]);
else
    X[d, 64] = AddPACDA(X[d, 64], X[n, 64]);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth)` |
| 🚫 ENCODING_UNDEF | `n == 31` |

### Variant: `Integer (PACDZA_64Z_dp_1src)` (PACDZA)
- **Condition**: `Z == 1 && Rn == 11111`
- **Assembly**: `PACDZA  <Xd>`
- **Fixed bits**: `Z`=`1`, `Rn`=`11111`
- **Bit Pattern**: `?????11111???1??????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  13 12   9   4  |
|--------------------------------|
| 1   1   0   11010110 00001 00  Z   010 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `pacda.xml`
</details>