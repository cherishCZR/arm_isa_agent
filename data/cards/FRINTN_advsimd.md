## FRINTN
_ARM A64 Instruction_

**Title**: FRINTN (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `FRINTN_advsimd`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point round to integral, to nearest with ties to even (vector)

**Description**:
This instruction rounds a vector of floating-point values
in the SIMD&FP source register
to integral floating-point values of the same size using the
Round to Nearest rounding mode, and writes the
result to the SIMD&FP destination register.

A zero input
gives a zero result with the same sign, an infinite input gives an infinite
result with the same sign, and a NaN is
propagated as for normal arithmetic.

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

### Variant: `Half-precision`
- **Assembly**: `FRINTN  <Vd>.<T>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22  18  16  12 11   9   4  |
|--------------------------------------------|
| 0   Q   0   0   111 0   0   1111 00  1100 0   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmiscfp16.FRINTN_asimdmiscfp16_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 16;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;

constant boolean exact = FALSE;
constant FPRounding rounding = FPRounding_TIEEVEN;
```

#### Execute (A64.simd_dp.asimdmiscfp16.FRINTN_asimdmiscfp16_R)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[n, datasize];
bits(datasize) result;
bits(esize) element;

for e = 0 to elements-1
    element = Elem[operand, e, esize];
    Elem[result, e, esize] = FPRoundInt(element, FPCR, rounding, exact);

V[d, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Single-precision and double-precision`
- **Assembly**: `FRINTN  <Vd>.<T>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21  16  12 11   9   4  |
|--------------------------------------------|
| 0   Q   0   0   111 0   0   sz  10000 1100 0   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.FRINTN_asimdmisc_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if sz:Q == '10' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 32 << UInt(sz);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;

constant boolean exact = FALSE;
constant FPRounding rounding = FPRounding_TIEEVEN;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `sz:Q != '10'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | For the "Half-precision" variant: is an arrangement specifier, |
| `<T>` | `arrangement` | `sz:Q` | For the "Single-precision and double-precision" variant: is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

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
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

---
<details><summary>Metadata</summary>

- advsimd-type: `simd`
- isa: `A64`
- source: `frintn_advsimd.xml`
</details>