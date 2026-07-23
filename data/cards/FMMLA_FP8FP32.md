## FMMLA
_ARM A64 Instruction_

**Title**: FMMLA (widening, 8-bit floating-point to single-precision) -- A64 | **Class**: `advsimd` | **XML ID**: `FMMLA_FP8FP32`

**Architecture**: `FEAT_F8F32MM` (ARMv9.6)

**Summary**: 8-bit floating-point matrix multiply-accumulate to single-precision

**Description**:
This instruction performs the fused sum-of-products within each eight adjacent 8-bit
elements while multiplying the 2×8 matrix of 8-bit floating-point values
in the first source vector by the 8×2 matrix of 8-bit floating-point
values in the second source vector. The single-precision sum-of-products
are scaled by 2-UInt(FPMR.LSCALE), before being destructively
added without intermediate rounding to the 2x2 single-precision matrix in
the destination vector. This is equivalent to accumulating 8-way dot
product per destination element.

The 8-bit floating-point encoding format for the elements of the first source
vector is selected by FPMR.F8S1. The 8-bit floating-point
encoding format for the elements of the second source vector is selected by
FPMR.F8S2.

### Variant: `Advanced SIMD`
- **Assembly**: `FMMLA  <Vd>.4S, <Vn>.16B, <Vm>.16B`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15 14  10  9   4  |
|--------------------------------------------|
| 0   1   1   0   111 0   10  0   Rm  1   1101 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame2.FMMLA_asimd_FP8FP32)

```
if !IsFeatureImplemented(FEAT_F8F32MM) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer d = UInt(Rd);
```

#### Execute (A64.simd_dp.asimdsame2.FMMLA_asimd_FP8FP32)

```
CheckFPMREnabled();
CheckFPAdvSIMDEnabled64();
constant bits(128) op1 = V[n, 128];
constant bits(128) op2 = V[m, 128];
constant bits(128) acc = V[d, 128];

V[d, 128] = FP8MatMulAddFP(acc, op1, op2, 8, FPCR, FPMR);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_F8F32MM)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP third source and destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

---
<details><summary>Metadata</summary>

- advsimd-type: `simd`
- isa: `A64`
- source: `fmmla_fp8fp32.xml`
</details>