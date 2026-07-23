## FMAXV
_ARM A64 Instruction_

**Title**: FMAXV -- A64 | **Class**: `advsimd` | **XML ID**: `FMAXV_advsimd`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point maximum across vector

**Description**:
This instruction compares all the
vector elements in the source SIMD&FP register,
and writes the largest of the values
as a scalar to the destination SIMD&FP register.
All the values in this instruction are floating-point values.

When FPCR.AH is 0,
the behavior is as follows:

When FPCR.AH is 1,
the behavior is as follows:

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
- **Assembly**: `FMAXV  <V><d>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21  16  11   9   4  |
|-----------------------------------------|
| 0   Q   0   0   111 0   0   0   11000 01111 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdall.FMAXV_asimdall_only_H)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 16;
constant integer datasize = 64 << UInt(Q);
```

#### Execute (A64.simd_dp.asimdall.FMAXV_asimdall_only_H)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[n, datasize];
V[d, esize] = FPReduce(ReduceOp_FMAX, operand, esize, FPCR);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Single-precision`
- **Assembly**: `FMAXV  S<d>, <Vn>.4S`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21  16  11   9   4  |
|-----------------------------------------|
| 0   1   1   0   111 0   0   0   11000 01111 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdall.FMAXV_asimdall_only_SD)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if sz:Q != '01' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 32;
constant integer datasize = 64 << UInt(Q);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `sz:Q == '01'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `` | Is the destination width specifier, H. |
| `<d>` | `register (32-bit)` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<T>` | `unknown` | `Q` | Is an arrangement specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4H |
| 1 | 8H |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmaxv_advsimd.xml`
</details>