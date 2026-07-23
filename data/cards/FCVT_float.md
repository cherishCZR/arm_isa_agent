## FCVT
_ARM A64 Instruction_

**Title**: FCVT -- A64 | **Class**: `float` | **XML ID**: `FCVT_float`

**Architecture**: `FEAT_FP` (ARMv8.0)

**Summary**: Floating-point convert precision (scalar)

**Description**:
This instruction converts the floating-point value
in the SIMD&FP source register to the precision for the destination register data type
using the rounding mode that is determined by the FPCR
and writes the result to the SIMD&FP destination register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Floating-point (FCVT_SH_floatdp1)` (Half-precision to single-precision)
- **Condition**: `ftype == 11 && opc == 00`
- **Assembly**: `FCVT  <Sd>, <Hn>`
- **Fixed bits**: `ftype`=`11`, `opc`=`00`
- **Bit Pattern**: `???????????????00?????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  14   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 10001 opc 10000 Rn  Rd  |
```

#### Decode (A64.simd_dp.floatdp1.FCVT_SH_floatdp1)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if ftype == opc || ftype == '10' || opc == '10' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer srcsize = 8 << UInt(ftype EOR '10');
constant integer dstsize = 8 << UInt(opc EOR '10');
```

#### Execute (A64.simd_dp.floatdp1.FCVT_SH_floatdp1)

```
CheckFPEnabled64();

constant bits(srcsize) operand = V[n, srcsize];
bits(128) result = if IsMerging(FPCR) then V[d, 128] else Zeros(128);

Elem[result, 0, dstsize] = FPConvert(operand, FPCR, dstsize);

V[d, 128] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `ftype != opc && ftype != '10' && opc != '10'` |

### Variant: `Floating-point (FCVT_DH_floatdp1)` (Half-precision to double-precision)
- **Condition**: `ftype == 11 && opc == 01`
- **Assembly**: `FCVT  <Dd>, <Hn>`
- **Fixed bits**: `ftype`=`11`, `opc`=`01`
- **Bit Pattern**: `???????????????10?????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  14   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 10001 opc 10000 Rn  Rd  |
```

### Variant: `Floating-point (FCVT_HS_floatdp1)` (Single-precision to half-precision)
- **Condition**: `ftype == 00 && opc == 11`
- **Assembly**: `FCVT  <Hd>, <Sn>`
- **Fixed bits**: `ftype`=`00`, `opc`=`11`
- **Bit Pattern**: `???????????????11?????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  14   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 10001 opc 10000 Rn  Rd  |
```

### Variant: `Floating-point (FCVT_DS_floatdp1)` (Single-precision to double-precision)
- **Condition**: `ftype == 00 && opc == 01`
- **Assembly**: `FCVT  <Dd>, <Sn>`
- **Fixed bits**: `ftype`=`00`, `opc`=`01`
- **Bit Pattern**: `???????????????10?????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  14   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 10001 opc 10000 Rn  Rd  |
```

### Variant: `Floating-point (FCVT_HD_floatdp1)` (Double-precision to half-precision)
- **Condition**: `ftype == 01 && opc == 11`
- **Assembly**: `FCVT  <Hd>, <Dn>`
- **Fixed bits**: `ftype`=`01`, `opc`=`11`
- **Bit Pattern**: `???????????????11?????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  14   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 10001 opc 10000 Rn  Rd  |
```

### Variant: `Floating-point (FCVT_SD_floatdp1)` (Double-precision to single-precision)
- **Condition**: `ftype == 01 && opc == 00`
- **Assembly**: `FCVT  <Sd>, <Dn>`
- **Fixed bits**: `ftype`=`01`, `opc`=`00`
- **Bit Pattern**: `???????????????00?????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  14   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 10001 opc 10000 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Sd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Dd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Hd>` | `register (16-bit)` | `Rd` | Is the 16-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the SIMD&FP source register, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvt_float.xml`
</details>