## FCVTMS
_ARM A64 Instruction_

**Title**: FCVTMS (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `FCVTMS_advsimd`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point convert to signed integer, rounding toward minus infinity (vector)

**Description**:
This instruction converts a scalar or each element in a vector from a floating-point
value to a signed integer value
using the Round towards Minus Infinity rounding mode, and
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

### Variant: `Scalar half-precision`
- **Assembly**: `FCVTMS  <Hd>, <Hn>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23 22  18  16  12 11   9   4  |
|-----------------------------------------|
| 01  0   1   111 0   0   1111 00  1101 1   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdmiscfp16.FCVTMS_asisdmiscfp16_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 16;
constant integer datasize = esize;
constant integer elements = 1;
constant FPRounding rounding = FPDecodeRounding(o1:o2);
constant boolean unsigned = FALSE;
```

#### Execute (A64.simd_dp.asisdmiscfp16.FCVTMS_asisdmiscfp16_R)

```
if elements == 1 && IsFeatureImplemented(FEAT_FPRCVT) then
    CheckFPEnabled64();
else
    CheckFPAdvSIMDEnabled64();

constant bits(datasize) operand = V[n, datasize];

constant boolean merge = elements == 1 && IsMerging(FPCR);
bits(128) result = if merge then V[d, 128] else Zeros(128);
constant integer fracbits = 0;
bits(esize) element;

for e = 0 to elements-1
    element = Elem[operand, e, esize];
    Elem[result, e, esize] = FPToFixed(element, fracbits, unsigned, FPCR, rounding, esize);

V[d, 128] = result;
```

### Variant: `Scalar single-precision and double-precision`
- **Assembly**: `FCVTMS  <V><d>, <V><n>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23 22 21  16  12 11   9   4  |
|-----------------------------------------|
| 01  0   1   111 0   0   sz  10000 1101 1   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdmisc.FCVTMS_asisdmisc_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 32 << UInt(sz);
constant integer datasize = esize;
constant integer elements = 1;
constant FPRounding rounding = FPDecodeRounding(o1:o2);
constant boolean unsigned = FALSE;
```

### Variant: `Vector half-precision`
- **Assembly**: `FCVTMS  <Vd>.<T>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22  18  16  12 11   9   4  |
|--------------------------------------------|
| 0   Q   0   0   111 0   0   1111 00  1101 1   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmiscfp16.FCVTMS_asimdmiscfp16_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 16;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
constant FPRounding rounding = FPDecodeRounding(o1:o2);
constant boolean unsigned = FALSE;
```

### Variant: `Vector single-precision and double-precision`
- **Assembly**: `FCVTMS  <Vd>.<T>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21  16  12 11   9   4  |
|--------------------------------------------|
| 0   Q   0   0   111 0   0   sz  10000 1101 1   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.FCVTMS_asimdmisc_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if sz:Q == '10' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 32 << UInt(sz);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
constant FPRounding rounding = FPDecodeRounding(o1:o2);
constant boolean unsigned = FALSE;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `sz:Q != '10'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hd>` | `register (16-bit)` | `Rd` | Is the 16-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<V>` | `register (128-bit)` | `sz` | Is a width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `unknown` | `Rn` | Is the number of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | For the "Vector half-precision" variant: is an arrangement specifier, |
| `<T>` | `arrangement` | `sz:Q` | For the "Vector single-precision and double-precision" variant: is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4H |
| 1 | 8H |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2S |
| 1 | 4S |
| 0 | RESERVED |
| 1 | 2D |

### Encoding Constraints
_2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_FP16)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvtms_advsimd.xml`
</details>