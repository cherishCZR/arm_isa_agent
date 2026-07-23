## FCMGT
_ARM A64 Instruction_

**Title**: FCMGT (zero) -- A64 | **Class**: `advsimd` | **XML ID**: `FCMGT_advsimd_zero`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point compare greater than zero (vector)

**Description**:
This instruction reads each floating-point value
in the source SIMD&FP register
and if the value is greater than zero
sets every bit of the corresponding vector element
in the destination SIMD&FP register to one,
otherwise sets every bit of the corresponding vector element
in the destination SIMD&FP register to zero.

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
- **Assembly**: `FCMGT  <Hd>, <Hn>, #0.0`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23 22  18  16  12 11   9   4  |
|-----------------------------------------|
| 01  0   1   111 0   1   1111 00  0110 0   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdmiscfp16.FCMGT_asisdmiscfp16_FZ)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 16;
constant integer datasize = esize;
constant integer elements = 1;
```

#### Execute (A64.simd_dp.asisdmiscfp16.FCMGT_asisdmiscfp16_FZ)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[n, datasize];
bits(datasize) result;
constant bits(esize) zero = FPZero('0', esize);
bits(esize) element;
boolean test_passed;

for e = 0 to elements-1
    element = Elem[operand, e, esize];
    test_passed = FPCompareGT(element, zero, FPCR);
    Elem[result, e, esize] = if test_passed then Ones(esize) else Zeros(esize);

V[d, datasize] = result;
```

### Variant: `Scalar single-precision and double-precision`
- **Assembly**: `FCMGT  <V><d>, <V><n>, #0.0`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23 22 21  16  12 11   9   4  |
|-----------------------------------------|
| 01  0   1   111 0   1   sz  10000 0110 0   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdmisc.FCMGT_asisdmisc_FZ)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 32 << UInt(sz);
constant integer datasize = esize;
constant integer elements = 1;
```

### Variant: `Vector half-precision`
- **Assembly**: `FCMGT  <Vd>.<T>, <Vn>.<T>, #0.0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22  18  16  12 11   9   4  |
|--------------------------------------------|
| 0   Q   0   0   111 0   1   1111 00  0110 0   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmiscfp16.FCMGT_asimdmiscfp16_FZ)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 16;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

### Variant: `Vector single-precision and double-precision`
- **Assembly**: `FCMGT  <Vd>.<T>, <Vn>.<T>, #0.0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21  16  12 11   9   4  |
|--------------------------------------------|
| 0   Q   0   0   111 0   1   sz  10000 0110 0   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.FCMGT_asimdmisc_FZ)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if sz:Q == '10' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

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
- source: `fcmgt_advsimd_zero.xml`
</details>