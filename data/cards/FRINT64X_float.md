## FRINT64X
_ARM A64 Instruction_

**Title**: FRINT64X (scalar) -- A64 | **Class**: `float` | **XML ID**: `FRINT64X_float`

**Architecture**: `FEAT_FRINTTS` (ARMv8.5)

**Summary**: Floating-point round to 64-bit integer, using current rounding mode (scalar)

**Description**:
This instruction rounds a floating-point value in the SIMD&FP source register to an
integral floating-point value that fits into a 64-bit integer size using the
rounding mode that is determined by the FPCR,
and writes the result to the SIMD&FP destination register.

A zero input returns a zero result with the same sign. When the result value is not numerically equal to
the input value, an Inexact exception is raised. When the input is infinite, NaN or out-of-range,
the instruction returns {for the corresponding result value} the most negative integer representable in the destination size,
and an Invalid Operation floating-point exception is raised.

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

### Variant: `Floating-point (FRINT64X_S_floatdp1)` (Single-precision)
- **Condition**: `ftype == 00`
- **Assembly**: `FRINT64X  <Sd>, <Sn>`
- **Fixed bits**: `ftype`=`0`
- **Bit Pattern**: `??????????????????????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  14   9   4  |
|--------------------------------|
| 0   0   0   11110 0x  10100 11  10000 Rn  Rd  |
```

#### Decode (A64.simd_dp.floatdp1.FRINT64X_S_floatdp1)

```
if !IsFeatureImplemented(FEAT_FRINTTS) then EndOfDecode(Decode_UNDEF);
if ftype IN {'1x'} then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 32 << UInt(ftype<0>);
constant integer intsize = 64;
```

#### Execute (A64.simd_dp.floatdp1.FRINT64X_S_floatdp1)

```
CheckFPEnabled64();

constant bits(esize) operand = V[n, esize];
constant FPRounding rounding = FPRoundingMode(FPCR);
bits(128) result = if IsMerging(FPCR) then V[d, 128] else Zeros(128);

Elem[result, 0, esize] = FPRoundIntN(operand, FPCR, rounding, intsize);

V[d, 128] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FRINTTS)` |
| 🚫 ENCODING_UNDEF | `ftype IN{'1x'}` |

### Variant: `Floating-point (FRINT64X_D_floatdp1)` (Double-precision)
- **Condition**: `ftype == 01`
- **Assembly**: `FRINT64X  <Dd>, <Dn>`
- **Fixed bits**: `ftype`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  14   9   4  |
|--------------------------------|
| 0   0   0   11110 0x  10100 11  10000 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Sd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Dd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the SIMD&FP source register, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `frint64x_float.xml`
</details>