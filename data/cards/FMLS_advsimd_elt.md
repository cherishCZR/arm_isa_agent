## FMLS
_ARM A64 Instruction_

**Title**: FMLS (by element) -- A64 | **Class**: `advsimd` | **XML ID**: `FMLS_advsimd_elt`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point fused multiply-subtract from accumulator (by element)

**Description**:
This instruction multiplies the vector elements
in the first source SIMD&FP register by the specified
value in the second source SIMD&FP register,
and subtracts the results
from the vector elements of the destination SIMD&FP register.
All the values in this instruction are floating-point values.

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

### Variant: `Scalar, half-precision`
- **Assembly**: `FMLS  <Hd>, <Hn>, <Vm>.H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23  21 20 19  15 14 13  11 10  9   4  |
|--------------------------------------------------|
| 01  0   1   111 1   00  L   M   Rm  0   1   01  H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdelem.FMLS_asisdelem_RH_H)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);

constant integer idxdsize = 64 << UInt(H);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer d = UInt(Rd);
constant integer index = UInt(H:L:M);

constant integer esize = 16;
constant integer datasize = esize;
constant integer elements = 1;
```

#### Execute (A64.simd_dp.asisdelem.FMLS_asisdelem_RH_H)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(idxdsize) operand2 = V[m, idxdsize];
constant bits(datasize) operand3 = V[d, datasize];
bits(esize) element1;
constant bits(esize) element2 = Elem[operand2, index, esize];
constant boolean merge = elements == 1 && IsMerging(FPCR);
bits(128) result = if merge then V[d, 128] else Zeros(128);

for e = 0 to elements-1
    element1 = FPNeg(Elem[operand1, e, esize], FPCR);
    Elem[result, e, esize] = FPMulAdd(Elem[operand3, e, esize], element1, element2, FPCR);

V[d, 128] = result;
```

### Variant: `Scalar, single-precision and double-precision`
- **Assembly**: `FMLS  <V><d>, <V><n>, <Vm>.<Ts>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23 22 21 20 19  15 14 13  11 10  9   4  |
|-----------------------------------------------------|
| 01  0   1   111 1   1   sz  L   M   Rm  0   1   01  H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdelem.FMLS_asisdelem_R_SD)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer idxdsize = 64 << UInt(H);
integer index;
constant bit Rmhi = M;
case sz:L of
    when '0x' index = UInt(H:L);
    when '10' index = UInt(H);
    when '11' EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rmhi:Rm);
constant integer esize = 32 << UInt(sz);
constant integer datasize = esize;
constant integer elements = 1;
```

### Variant: `Vector, half-precision`
- **Assembly**: `FMLS  <Vd>.<T>, <Vn>.<T>, <Vm>.H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20 19  15 14 13  11 10  9   4  |
|-----------------------------------------------------|
| 0   Q   0   0   111 1   00  L   M   Rm  0   1   01  H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.FMLS_asimdelem_RH_H)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);

constant integer idxdsize = 64 << UInt(H);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer d = UInt(Rd);
constant integer index = UInt(H:L:M);

constant integer esize = 16;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

### Variant: `Vector, single-precision and double-precision`
- **Assembly**: `FMLS  <Vd>.<T>, <Vn>.<T>, <Vm>.<Ts>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21 20 19  15 14 13  11 10  9   4  |
|--------------------------------------------------------|
| 0   Q   0   0   111 1   1   sz  L   M   Rm  0   1   01  H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.FMLS_asimdelem_R_SD)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if sz:Q == '10' then EndOfDecode(Decode_UNDEF);
constant integer idxdsize = 64 << UInt(H);
integer index;
constant bit Rmhi = M;
case sz:L of
    when '0x' index = UInt(H:L);
    when '10' index = UInt(H);
    when '11' EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rmhi:Rm);
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
| `<Vm>` | `register (128-bit)` | `Rm` | For the "Scalar, half-precision" and "Vector, half-precision" variants: is the name of the second SIMD&FP source register, in the range V0 to V15, enc |
| `<Vm>` | `register (128-bit)` | `M:Rm` | For the "Scalar, single-precision and double-precision" and "Vector, single-precision and double-precision" variants: is the name of the second SIMD&F |
| `<index>` | `unknown` | `H:L:M` | For the "Scalar, half-precision" and "Vector, half-precision" variants: is the element index, in the range 0 to 7, encoded in the "H:L:M" fields. |
| `<index>` | `unknown` | `sz:L:H` | For the "Scalar, single-precision and double-precision" and "Vector, single-precision and double-precision" variants: is the element index, |
| `<V>` | `register (128-bit)` | `sz` | Is a width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `unknown` | `Rn` | Is the number of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Ts>` | `unknown` | `sz` | Is an element size specifier, |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | For the "Vector, half-precision" variant: is an arrangement specifier, |
| `<T>` | `arrangement` | `Q:sz` | For the "Vector, single-precision and double-precision" variant: is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |

**<index> Value Table**:

| bitfield | symbol |
|---|---|
| x | UInt(H:L) |
| 0 | UInt(H) |
| 1 | RESERVED |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

**<Ts> Value Table**:

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
| 1 | RESERVED |
| 0 | 4S |
| 1 | 2D |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_FP16)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `sz:L != '11'` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmls_advsimd_elt.xml`
</details>