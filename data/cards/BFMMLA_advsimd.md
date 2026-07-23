## BFMMLA
_ARM A64 Instruction_

**Title**: BFMMLA (widening) -- A64 | **Class**: `advsimd` | **XML ID**: `BFMMLA_advsimd`

**Architecture**: `FEAT_BF16` (ARMv8.6)

**Summary**: BFloat16 matrix multiply-accumulate to single-precision

**Description**:
If FEAT_EBF16 is not implemented or FPCR.EBF is 0,
this instruction:

If FEAT_EBF16 is implemented and FPCR.EBF is 1,
then this instruction:

Irrespective of FEAT_EBF16 and FPCR.EBF, this instruction:

ID_AA64ISAR1_EL1.BF16 indicates whether this instruction is supported.

### Variant: `Advanced SIMD`
- **Assembly**: `BFMMLA  <Vd>.4S, <Vn>.8H, <Vm>.8H`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15 14  10  9   4  |
|--------------------------------------------|
| 0   1   1   0   111 0   01  0   Rm  1   1101 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame2.BFMMLA_asimdsame2_E)

```
if !IsFeatureImplemented(FEAT_BF16) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.simd_dp.asimdsame2.BFMMLA_asimdsame2_E)

```
CheckFPAdvSIMDEnabled64();
constant bits(128) op1 = V[n, 128];
constant bits(128) op2 = V[m, 128];
constant bits(128) acc = V[d, 128];

V[d, 128] = BFMatMulAddH(acc, op1, op2, FPCR);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_BF16)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP third source and destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

### Operational Notes

Arm expects that the BFMMLA instruction will deliver a peak BFloat16 multiply throughput that is at least as high as can be achieved using two BFDOT (vector) instructions, with a goal that it should have significantly higher throughput.

---
<details><summary>Metadata</summary>

- advsimd-type: `simd`
- isa: `A64`
- source: `bfmmla_advsimd.xml`
</details>