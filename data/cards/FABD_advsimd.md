## FABD
_ARM A64 Instruction_

**Title**: FABD -- A64 | **Class**: `advsimd` | **XML ID**: `FABD_advsimd`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point absolute difference (vector)

**Description**:
This instruction subtracts the floating-point values
in the elements of the second source SIMD&FP register,
from the corresponding floating-point values in the elements
of the first source SIMD&FP register,
places the absolute value of each result in a vector,
and writes the vector to the destination SIMD&FP register.

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
- **Assembly**: `FABD  <Hd>, <Hn>, <Hm>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23 22  20  15  13  10  9   4  |
|-----------------------------------------|
| 01  1   1   111 0   1   10  Rm  00  010 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdsamefp16.FABD_asisdsamefp16_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 16;
constant integer datasize = esize;
constant integer elements = 1;
```

#### Execute (A64.simd_dp.asisdsamefp16.FABD_asisdsamefp16_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];

bits(esize) element1;
bits(esize) element2;
constant boolean merge = elements == 1 && IsMerging(FPCR);
bits(128) result = if merge then V[n, 128] else Zeros(128);

for e = 0 to elements-1
    element1 = Elem[operand1, e, esize];
    element2 = Elem[operand2, e, esize];
    constant bits(esize) diff = FPSub(element1, element2, FPCR);
    Elem[result, e, esize] = FPAbs(diff, FPCR);

V[d, 128] = result;
```

### Variant: `Scalar single-precision and double-precision`
- **Assembly**: `FABD  <V><d>, <V><n>, <V><m>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23 22 21 20  15  10  9   4  |
|-----------------------------------------|
| 01  1   1   111 0   1   sz  1   Rm  11010 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdsame.FABD_asisdsame_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 32 << UInt(sz);
constant integer datasize = esize;
constant integer elements = 1;
```

### Variant: `Vector half-precision`
- **Assembly**: `FABD  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22  20  15  13  10  9   4  |
|--------------------------------------------|
| 0   Q   1   0   111 0   1   10  Rm  00  010 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsamefp16.FABD_asimdsamefp16_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 16;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

### Variant: `Vector single-precision and double-precision`
- **Assembly**: `FABD  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21 20  15  10  9   4  |
|--------------------------------------------|
| 0   Q   1   0   111 0   1   sz  1   Rm  11010 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame.FABD_asimdsame_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if sz:Q == '10' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 32 << UInt(sz);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
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
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Hm>` | `register (16-bit)` | `Rm` | Is the 16-bit name of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<V>` | `register (128-bit)` | `sz` | Is a width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `unknown` | `Rn` | Is the number of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<m>` | `unknown` | `Rm` | Is the number of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | For the "Vector half-precision" variant: is an arrangement specifier, |
| `<T>` | `arrangement` | `sz:Q` | For the "Vector single-precision and double-precision" variant: is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

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
- source: `fabd_advsimd.xml`
</details>