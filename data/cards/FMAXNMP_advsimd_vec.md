## FMAXNMP
_ARM A64 Instruction_

**Title**: FMAXNMP (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `FMAXNMP_advsimd_vec`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point maximum number pairwise (vector)

**Description**:
This instruction creates a vector by
concatenating the vector elements of the first source SIMD&FP register
after the vector elements of the second source SIMD&FP register,
reads each pair of adjacent vector elements in the
two source SIMD&FP registers,
writes the largest of each pair of values
into a vector, and writes the vector to the destination SIMD&FP register.
All the values in this instruction are floating-point values.

Regardless of the value of FPCR.AH,
the behavior is as follows for each pairwise operation:

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
- **Assembly**: `FMAXNMP  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22  20  15  13  10  9   4  |
|--------------------------------------------|
| 0   Q   1   0   111 0   0   10  Rm  00  000 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsamefp16.FMAXNMP_asimdsamefp16_only)

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

#### Execute (A64.simd_dp.asimdsamefp16.FMAXNMP_asimdsamefp16_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];
bits(datasize) result;
constant bits(2*datasize) concat = operand2:operand1;
bits(esize) element1;
bits(esize) element2;

for e = 0 to elements-1
    element1 = Elem[concat, 2*e, esize];
    element2 = Elem[concat, (2*e)+1, esize];
    Elem[result, e, esize] = FPMaxNum(element1, element2, FPCR);
V[d, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Single-precision and double-precision`
- **Assembly**: `FMAXNMP  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21 20  15  10  9   4  |
|--------------------------------------------|
| 0   Q   1   0   111 0   0   sz  1   Rm  11000 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame.FMAXNMP_asimdsame_only)

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
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `sz:Q != '10'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | For the "Half-precision" variant: is an arrangement specifier, |
| `<T>` | `arrangement` | `sz:Q` | For the "Single-precision and double-precision" variant: is an arrangement specifier, |
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

---
<details><summary>Metadata</summary>

- advsimd-reguse: `3reg-same`
- advsimd-type: `simd`
- isa: `A64`
- source: `fmaxnmp_advsimd_vec.xml`
</details>