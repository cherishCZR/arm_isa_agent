## FRINT64X
_ARM A64 Instruction_

**Title**: FRINT64X (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `FRINT64X_advsimd`

**Architecture**: `FEAT_FRINTTS` (ARMv8.5)

**Summary**: Floating-point round to 64-bit integer, using current rounding mode (vector)

**Description**:
This instruction rounds a vector of floating-point values in the SIMD&FP source register to integral floating-point
values that fit into a 64-bit integer size using the rounding mode that is determined by the FPCR,
and writes the result to the SIMD&FP destination register.

A zero input returns a zero result with the same sign. When one of the result values is not numerically equal to
the corresponding input value, an Inexact exception is raised. When an input is infinite, NaN or out-of-range,
the instruction returns for the corresponding result value the most negative integer representable in the destination size,
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

### Variant: `Vector single-precision and double-precision`
- **Assembly**: `FRINT64X  <Vd>.<T>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21  16  12 11   9   4  |
|--------------------------------------------|
| 0   Q   1   0   111 0   0   sz  10000 1111 1   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.FRINT64X_asimdmisc_R)

```
if !IsFeatureImplemented(FEAT_FRINTTS) then EndOfDecode(Decode_UNDEF);
if sz:Q == '10' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 32 << UInt(sz);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
constant integer intsize = 64;
```

#### Execute (A64.simd_dp.asimdmisc.FRINT64X_asimdmisc_R)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[n, datasize];
bits(datasize) result;
constant FPRounding rounding = FPRoundingMode(FPCR);
bits(esize) element;

for e = 0 to elements-1
    element = Elem[operand, e, esize];
    Elem[result, e, esize] = FPRoundIntN(element, FPCR, rounding, intsize);

V[d, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FRINTTS)` |
| 🚫 ENCODING_UNDEF | `sz:Q != '10'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `sz:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2S |
| 1 | 4S |
| 0 | RESERVED |
| 1 | 2D |

---
<details><summary>Metadata</summary>

- advsimd-datatype: `simd-single-and-double`
- advsimd-type: `simd`
- datatype: `single-and-double`
- isa: `A64`
- source: `frint64x_advsimd.xml`
</details>