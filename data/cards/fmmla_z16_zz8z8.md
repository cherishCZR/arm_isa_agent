## FMMLA
_ARM A64 Instruction_

**Title**: FMMLA (widening, FP8 to FP16) -- A64 | **Class**: `sve2` | **XML ID**: `fmmla_z16_zz8z8`

**Architecture**: `FEAT_SVE2 && FEAT_F8F16MM` (FEAT_SVE2 && FEAT_F8F16MM)

**Summary**: 8-bit floating-point matrix multiply-accumulate to half-precision

**Description**:
This 8-bit floating-point widening matrix multiply-accumulate
instruction performs the fused sum-of-products within each four adjacent 8-bit elements
while multiplying the 2×4 matrix of 8-bit floating-point
values held in each 64-bit segment of the first source vector with
the 4×2 matrix of 8-bit floating-point values in the corresponding segment
of the second source vector. The half-precision sum-of-products
are scaled by 2-UInt(FPMR.LSCALE[3:0]),
before being destructively added without intermediate rounding to
the 2×2 half-precision matrix in the corresponding segment of the destination vector.
This is equivalent to accumulating 4-way dot product per destination element.

The 8-bit floating-point encoding format for the elements of the first source vector
and the second source vector is selected by FPMR.F8S1 and FPMR.F8S2
respectively.

This instruction is unpredicated.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: SM Policy: `SM_0_only`

### Variant: `SVE2`
- **Assembly**: `FMMLA  <Zda>.H, <Zn>.B, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24  22 21 20  15   9   4  |
|-----------------------------|
| 011 0010 00  1   1   Zm  111000 Zn  Zda |
```

#### Decode (A64.sve.sve_fp8_fmmla.sve_fp8_fmmla.fmmla_z16_zz8z8_)

```
if !IsFeatureImplemented(FEAT_SVE2) || !IsFeatureImplemented(FEAT_F8F16MM) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Execute (A64.sve.sve_fp8_fmmla.sve_fp8_fmmla.fmmla_z16_zz8z8_)

```
CheckFPMREnabled();
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments =  VL DIV 64;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

for s = 0 to segments-1
    constant bits(64) op1    = Elem[operand1, s, 64];
    constant bits(64) op2    = Elem[operand2, s, 64];
    constant bits(64) addend = Elem[operand3, s, 64];
    constant integer way = 4;
    Elem[result, s, 64] = FP8MatMulAddFP(addend, op1, op2, way, FPCR, FPMR);


Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) && IsFeatureImplemented(FEAT_F8F16MM)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmmla_z16_zz8z8.xml`
</details>