## FNEG
_ARM A64 Instruction_

**Title**: FNEG (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `FNEG_advsimd`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point negate (vector)

**Description**:
This instruction negates the value of each vector element
in the source SIMD&FP register,
writes the result to a vector,
and writes the vector to the destination SIMD&FP register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Half-precision`
- **Assembly**: `FNEG  <Vd>.<T>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22  18  16  11   9   4  |
|-----------------------------------------|
| 0   Q   1   0   111 0   1   1111 00  01111 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmiscfp16.FNEG_asimdmiscfp16_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 16;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimdmiscfp16.FNEG_asimdmiscfp16_R)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[n, datasize];
bits(datasize) result;

for e = 0 to elements-1
    constant bits(esize) element = Elem[operand, e, esize];
    Elem[result, e, esize] = FPNeg(element, FPCR);

V[d, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Single-precision and double-precision`
- **Assembly**: `FNEG  <Vd>.<T>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21  16  11   9   4  |
|-----------------------------------------|
| 0   Q   1   0   111 0   1   sz  10000 01111 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.FNEG_asimdmisc_R)

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

---
<details><summary>Metadata</summary>

- advsimd-type: `simd`
- isa: `A64`
- source: `fneg_advsimd.xml`
</details>