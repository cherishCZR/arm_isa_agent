## FDIV
_ARM A64 Instruction_

**Title**: FDIV (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `FDIV_advsimd`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point divide (vector)

**Description**:
This instruction divides the floating-point values in the elements in the first source SIMD&FP register,
by the floating-point values in the corresponding elements in the second source SIMD&FP register,
places the results in a vector,
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

### Variant: `Half-precision`
- **Assembly**: `FDIV  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22  20  15  13  10  9   4  |
|--------------------------------------------|
| 0   Q   1   0   111 0   0   10  Rm  00  111 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsamefp16.FDIV_asimdsamefp16_only)

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

#### Execute (A64.simd_dp.asimdsamefp16.FDIV_asimdsamefp16_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];
bits(datasize) result;
bits(esize) element1;
bits(esize) element2;

for e = 0 to elements-1
    element1 = Elem[operand1, e, esize];
    element2 = Elem[operand2, e, esize];
    Elem[result, e, esize] = FPDiv(element1, element2, FPCR);

V[d, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Single-precision and double-precision`
- **Assembly**: `FDIV  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21 20  15  10  9   4  |
|--------------------------------------------|
| 0   Q   1   0   111 0   0   sz  1   Rm  11111 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame.FDIV_asimdsame_only)

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
- source: `fdiv_advsimd.xml`
</details>