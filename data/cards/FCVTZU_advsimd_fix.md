## FCVTZU
_ARM A64 Instruction_

**Title**: FCVTZU (vector, fixed-point) -- A64 | **Class**: `advsimd` | **XML ID**: `FCVTZU_advsimd_fix`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point convert to unsigned fixed-point, rounding toward zero (vector)

**Description**:
This instruction converts a scalar or each element in a vector
from floating-point to
fixed-point unsigned integer
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

### Variant: `Scalar`
- **Assembly**: `FCVTZU  <V><d>, <V><n>, #<fbits>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24  22  18  15  10  9   4  |
|-----------------------------------|
| 01  1   1   111 10  ?   immb 11111 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdshf.FCVTZU_asisdshf_C)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if immh IN {'000x'} || (immh IN {'001x'} && !IsFeatureImplemented(FEAT_FP16)) then
    EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = if immh IN {'1xxx'} then 64 else if immh IN {'01xx'} then 32 else 16;
constant integer datasize = esize;
constant integer elements = 1;

constant integer fracbits = (esize * 2) - UInt(immh:immb);
constant boolean unsigned = TRUE;
constant FPRounding rounding = FPRounding_ZERO;
```

#### Execute (A64.simd_dp.asisdshf.FCVTZU_asisdshf_C)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand  = V[n, datasize];

constant boolean merge = elements == 1 && IsMerging(FPCR);
bits(128) result = if merge then V[d, 128] else Zeros(128);
bits(esize) element;

for e = 0 to elements-1
    element = Elem[operand, e, esize];
    Elem[result, e, esize] = FPToFixed(element, fracbits, unsigned, FPCR, rounding, esize);

V[d, 128] = result;
```

### Variant: `Vector`
- **Assembly**: `FCVTZU  <Vd>.<T>, <Vn>.<T>, #<fbits>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  18  15  10  9   4  |
|--------------------------------------|
| 0   Q   1   0   111 10  ?   immb 11111 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdshf.FCVTZU_asimdshf_C)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if immh == '0000' then SEE(asimdimm);
if immh IN {'000x'} || (immh IN {'001x'} && !IsFeatureImplemented(FEAT_FP16)) then
    EndOfDecode(Decode_UNDEF);
if immh<3>:Q == '10' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = if immh IN {'1xxx'} then 64 else if immh IN {'01xx'} then 32 else 16;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;

constant integer fracbits = (esize * 2) - UInt(immh:immb);
constant boolean unsigned = TRUE;
constant FPRounding rounding = FPRounding_ZERO;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `immh<3>:Q != '10'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `immh` | Is a width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `unknown` | `Rn` | Is the number of the SIMD&FP source register, encoded in the "Rn" field. |
| `<fbits>` | `unknown` | `immh:immb` | For the "Scalar" variant: is the number of fractional bits, in the range 1 to the operand width, |
| `<fbits>` | `unknown` | `immh:immb` | For the "Vector" variant: is the number of fractional bits, in the range 1 to the element width, |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `immh:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | RESERVED |
| 001x | H |
| 01xx | S |
| 1xxx | D |

**<fbits> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | RESERVED |
| 001x | 32 - UInt(immh:immb) |
| 01xx | 64 - UInt(immh:immb) |
| 1xxx | 128 - UInt(immh:immb) |

**<fbits> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | RESERVED |
| 001x | 32 - UInt(immh:immb) |
| 01xx | 64 - UInt(immh:immb) |
| 1xxx | 128 - UInt(immh:immb) |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| x | RESERVED |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| 0 | RESERVED |
| 1 | 2D |

### Encoding Constraints
_2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🔒 FEATURE_GATE | `immh IN{'000x'} && (immh IN{'001x'} \|\| IsFeatureImplemented(FEAT_FP16))` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvtzu_advsimd_fix.xml`
</details>