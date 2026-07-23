## FCVTZU
_ARM A64 Instruction_

**Title**: FCVTZU (scalar, fixed-point) -- A64 | **Class**: `float` | **XML ID**: `FCVTZU_float_fix`

**Summary**: Floating-point convert to unsigned fixed-point, rounding toward zero (scalar)

**Description**:
This instruction converts the floating-point value
in the SIMD&FP source register to a 32-bit or 64-bit fixed-point unsigned integer
using the Round towards Zero rounding mode, and
writes the result to the general-purpose destination register.

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

### Variant: `Floating-point (FCVTZU_32H_float2fix)` (Half-precision to 32-bit)
- **Condition**: `sf == 0 && ftype == 11`
- **Assembly**: `FCVTZU  <Wd>, <Hn>, #<fbits>`
- **Fixed bits**: `sf`=`0`, `ftype`=`11`
- **Bit Pattern**: `??????????????????????11???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 0   11  001 scale Rn  Rd  |
```

#### Decode (A64.simd_dp.float2fix.FCVTZU_32H_float2fix)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if ftype == '10' then EndOfDecode(Decode_UNDEF);
if ftype == '11' && !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);
if sf == '0' && scale<5> == '0' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer intsize = 32 << UInt(sf);
constant integer decode_fltsize = 8 << UInt(ftype EOR '10');

constant integer fracbits = 64 - UInt(scale);

constant FPRounding rounding = FPRounding_ZERO;
constant boolean unsigned = TRUE;
```

#### Execute (A64.simd_dp.float2fix.FCVTZU_32H_float2fix)

```
CheckFPEnabled64();

constant bits(decode_fltsize) fltval = V[n, decode_fltsize];
X[d, intsize] = FPToFixed(fltval, fracbits, unsigned, FPCR, rounding, intsize);
```

#### Constraints
_2× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `ftype != '10'` |
| 🔒 FEATURE_GATE | `ftype != '11' \|\| IsFeatureImplemented(FEAT_FP16)` |
| 🚫 ENCODING_UNDEF | `sf != '0' \|\| scale<5> != '0'` |

### Variant: `Floating-point (FCVTZU_64H_float2fix)` (Half-precision to 64-bit)
- **Condition**: `sf == 1 && ftype == 11`
- **Assembly**: `FCVTZU  <Xd>, <Hn>, #<fbits>`
- **Fixed bits**: `sf`=`1`, `ftype`=`11`
- **Bit Pattern**: `??????????????????????11???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 0   11  001 scale Rn  Rd  |
```

### Variant: `Floating-point (FCVTZU_32S_float2fix)` (Single-precision to 32-bit)
- **Condition**: `sf == 0 && ftype == 00`
- **Assembly**: `FCVTZU  <Wd>, <Sn>, #<fbits>`
- **Fixed bits**: `sf`=`0`, `ftype`=`00`
- **Bit Pattern**: `??????????????????????00???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 0   11  001 scale Rn  Rd  |
```

### Variant: `Floating-point (FCVTZU_64S_float2fix)` (Single-precision to 64-bit)
- **Condition**: `sf == 1 && ftype == 00`
- **Assembly**: `FCVTZU  <Xd>, <Sn>, #<fbits>`
- **Fixed bits**: `sf`=`1`, `ftype`=`00`
- **Bit Pattern**: `??????????????????????00???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 0   11  001 scale Rn  Rd  |
```

### Variant: `Floating-point (FCVTZU_32D_float2fix)` (Double-precision to 32-bit)
- **Condition**: `sf == 0 && ftype == 01`
- **Assembly**: `FCVTZU  <Wd>, <Dn>, #<fbits>`
- **Fixed bits**: `sf`=`0`, `ftype`=`01`
- **Bit Pattern**: `??????????????????????10???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 0   11  001 scale Rn  Rd  |
```

### Variant: `Floating-point (FCVTZU_64D_float2fix)` (Double-precision to 64-bit)
- **Condition**: `sf == 1 && ftype == 01`
- **Assembly**: `FCVTZU  <Xd>, <Dn>, #<fbits>`
- **Fixed bits**: `sf`=`1`, `ftype`=`01`
- **Bit Pattern**: `??????????????????????10???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 0   11  001 scale Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<fbits>` | `unknown` | `scale` | For the "Double-precision to 32-bit", "Half-precision to 32-bit", and "Single-precision to 32-bit" variants: is the number of bits after the binary po |
| `<fbits>` | `unknown` | `scale` | For the "Double-precision to 64-bit", "Half-precision to 64-bit", and "Single-precision to 64-bit" variants: is the number of bits after the binary po |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the SIMD&FP source register, encoded in the "Rn" field. |

### Operational Notes

If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the general-purpose register written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvtzu_float_fix.xml`
</details>