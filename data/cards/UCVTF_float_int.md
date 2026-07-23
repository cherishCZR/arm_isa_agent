## UCVTF
_ARM A64 Instruction_

**Title**: UCVTF (scalar, integer) -- A64 | **Class**: `float` | **XML ID**: `UCVTF_float_int`

**Summary**: Unsigned integer convert to floating-point (scalar)

**Description**:
This instruction converts the unsigned integer value
in the general-purpose source register to a
floating-point value using the rounding mode that is specified by the
FPCR, and
writes the result to the SIMD&FP destination register.

This instruction can generate a floating-point exception.
  Depending on the settings in FPCR,
  the exception results in either a flag being set in FPSR
  or a synchronous exception being generated.
  For more information, see
  Floating-point exceptions and exception traps.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Floating-point (UCVTF_H32_float2int)` (32-bit to half-precision)
- **Condition**: `sf == 0 && ftype == 11`
- **Assembly**: `UCVTF  <Hd>, <Wn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`11`
- **Bit Pattern**: `??????????????????????11???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   00  011 000000 Rn  Rd  |
```

#### Decode (A64.simd_dp.float2int.UCVTF_H32_float2int)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if ftype == '10' then EndOfDecode(Decode_UNDEF);
if ftype == '11' && !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer intsize = 32 << UInt(sf);
constant integer decode_fltsize = 8 << UInt(ftype EOR '10');
constant boolean unsigned    = TRUE;
```

#### Execute (A64.simd_dp.float2int.UCVTF_H32_float2int)

```
CheckFPEnabled64();

constant integer fltsize = if IsMerging(FPCR) then 128 else decode_fltsize;

constant bits(intsize) intval = X[n, intsize];
constant FPRounding rounding  = FPRoundingMode(FPCR);
constant integer fracbits = 0;
bits(fltsize) fltval = if IsMerging(FPCR) then V[d, fltsize] else Zeros(fltsize);
Elem[fltval, 0, decode_fltsize] = FixedToFP(intval, fracbits, unsigned,
                                            FPCR, rounding, decode_fltsize);

V[d, fltsize] = fltval;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `ftype != '10'` |
| 🔒 FEATURE_GATE | `ftype != '11' \|\| IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Floating-point (UCVTF_S32_float2int)` (32-bit to single-precision)
- **Condition**: `sf == 0 && ftype == 00`
- **Assembly**: `UCVTF  <Sd>, <Wn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`00`
- **Bit Pattern**: `??????????????????????00???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   00  011 000000 Rn  Rd  |
```

### Variant: `Floating-point (UCVTF_D32_float2int)` (32-bit to double-precision)
- **Condition**: `sf == 0 && ftype == 01`
- **Assembly**: `UCVTF  <Dd>, <Wn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`01`
- **Bit Pattern**: `??????????????????????10???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   00  011 000000 Rn  Rd  |
```

### Variant: `Floating-point (UCVTF_H64_float2int)` (64-bit to half-precision)
- **Condition**: `sf == 1 && ftype == 11`
- **Assembly**: `UCVTF  <Hd>, <Xn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`11`
- **Bit Pattern**: `??????????????????????11???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   00  011 000000 Rn  Rd  |
```

### Variant: `Floating-point (UCVTF_S64_float2int)` (64-bit to single-precision)
- **Condition**: `sf == 1 && ftype == 00`
- **Assembly**: `UCVTF  <Sd>, <Xn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`00`
- **Bit Pattern**: `??????????????????????00???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   00  011 000000 Rn  Rd  |
```

### Variant: `Floating-point (UCVTF_D64_float2int)` (64-bit to double-precision)
- **Condition**: `sf == 1 && ftype == 01`
- **Assembly**: `UCVTF  <Dd>, <Xn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`01`
- **Bit Pattern**: `??????????????????????10???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   00  011 000000 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hd>` | `register (16-bit)` | `Rd` | Is the 16-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<Sd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Dd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ucvtf_float_int.xml`
</details>