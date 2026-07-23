## FCVTZU
_ARM A64 Instruction_

**Title**: FCVTZU (scalar, integer) -- A64 | **Class**: `float` | **XML ID**: `FCVTZU_float_int`

**Summary**: Floating-point convert to unsigned integer, rounding toward zero (scalar)

**Description**:
This instruction converts the floating-point value
in the SIMD&FP source register to a 32-bit or 64-bit unsigned integer
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

### Variant: `Floating-point (FCVTZU_32H_float2int)` (Half-precision to 32-bit)
- **Condition**: `sf == 0 && ftype == 11`
- **Assembly**: `FCVTZU  <Wd>, <Hn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`11`
- **Bit Pattern**: `??????????????????????11???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  001 000000 Rn  Rd  |
```

#### Decode (A64.simd_dp.float2int.FCVTZU_32H_float2int)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if ftype == '10' then EndOfDecode(Decode_UNDEF);
if ftype == '11' && !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer intsize = 32 << UInt(sf);
constant integer fltsize = 8 << UInt(ftype EOR '10');

constant FPRounding rounding = FPRounding_ZERO;
constant boolean unsigned    = TRUE;
```

#### Execute (A64.simd_dp.float2int.FCVTZU_32H_float2int)

```
CheckFPEnabled64();

constant bits(fltsize) fltval = V[n, fltsize];
constant integer fracbits = 0;

X[d, intsize] = FPToFixed(fltval, fracbits, unsigned, FPCR, rounding, intsize);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `ftype != '10'` |
| 🔒 FEATURE_GATE | `ftype != '11' \|\| IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Floating-point (FCVTZU_64H_float2int)` (Half-precision to 64-bit)
- **Condition**: `sf == 1 && ftype == 11`
- **Assembly**: `FCVTZU  <Xd>, <Hn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`11`
- **Bit Pattern**: `??????????????????????11???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  001 000000 Rn  Rd  |
```

### Variant: `Floating-point (FCVTZU_32S_float2int)` (Single-precision to 32-bit)
- **Condition**: `sf == 0 && ftype == 00`
- **Assembly**: `FCVTZU  <Wd>, <Sn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`00`
- **Bit Pattern**: `??????????????????????00???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  001 000000 Rn  Rd  |
```

### Variant: `Floating-point (FCVTZU_64S_float2int)` (Single-precision to 64-bit)
- **Condition**: `sf == 1 && ftype == 00`
- **Assembly**: `FCVTZU  <Xd>, <Sn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`00`
- **Bit Pattern**: `??????????????????????00???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  001 000000 Rn  Rd  |
```

### Variant: `Floating-point (FCVTZU_32D_float2int)` (Double-precision to 32-bit)
- **Condition**: `sf == 0 && ftype == 01`
- **Assembly**: `FCVTZU  <Wd>, <Dn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`01`
- **Bit Pattern**: `??????????????????????10???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  001 000000 Rn  Rd  |
```

### Variant: `Floating-point (FCVTZU_64D_float2int)` (Double-precision to 64-bit)
- **Condition**: `sf == 1 && ftype == 01`
- **Assembly**: `FCVTZU  <Xd>, <Dn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`01`
- **Bit Pattern**: `??????????????????????10???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  001 000000 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the SIMD&FP source register, encoded in the "Rn" field. |

### Operational Notes

If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the general-purpose register written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvtzu_float_int.xml`
</details>