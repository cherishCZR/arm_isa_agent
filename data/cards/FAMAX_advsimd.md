## FAMAX
_ARM A64 Instruction_

**Title**: FAMAX -- A64 | **Class**: `advsimd` | **XML ID**: `FAMAX_advsimd`

**Architecture**: `FEAT_AdvSIMD && FEAT_FAMINMAX` (FEAT_AdvSIMD && FEAT_FAMINMAX)

**Summary**: Floating-point absolute maximum

**Description**:
This instruction determines the maximum absolute value from floating-point elements
of the first source vector and the corresponding floating-point elements
of the second source vector, and places the results in the corresponding elements
of the destination vector.

Regardless of the value of FPCR.AH, the behavior is as follows:

### Variant: `Half-precision`
- **Assembly**: `FAMAX  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22  20  15  13  10  9   4  |
|--------------------------------------------|
| 0   Q   0   0   111 0   1   10  Rm  00  011 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsamefp16.FAMAX_asimdsamefp16_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FAMINMAX) then
    EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 16;
constant integer datasize = if Q == '1' then 128 else 64;
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimdsamefp16.FAMAX_asimdsamefp16_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];
bits(datasize) result;

for e = 0 to elements-1
    constant bits(esize) op1 = Elem[operand1, e, esize];
    constant bits(esize) op2 = Elem[operand2, e, esize];
    Elem[result, e, esize] = FPAbsMax(op1, op2, FPCR);
V[d, datasize] = result;
```

### Variant: `Single-precision and double-precision`
- **Assembly**: `FAMAX  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15  10  9   4  |
|-----------------------------------------|
| 0   Q   0   0   111 0   1x  1   Rm  11011 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame.FAMAX_asimdsame_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FAMINMAX) then
    EndOfDecode(Decode_UNDEF);
if Q == '0' && size == '11' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 8 << UInt(size);
constant integer datasize = if Q == '1' then 128 else 64;
constant integer elements = datasize DIV esize;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `Q != '0' \|\| size != '11'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | For the "Half-precision" variant: is an arrangement specifier, |
| `<T>` | `arrangement` | `size<0>:Q` | For the "Single-precision and double-precision" variant: is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

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
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_FAMINMAX)` |

---
<details><summary>Metadata</summary>

- advsimd-reguse: `3reg-same`
- advsimd-type: `simd`
- isa: `A64`
- source: `famax_advsimd.xml`
</details>