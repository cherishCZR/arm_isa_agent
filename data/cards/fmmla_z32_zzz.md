## FMMLA
_ARM A64 Instruction_

**Title**: FMMLA (widening, FP16 to FP32) -- A64 | **Class**: `sve2` | **XML ID**: `fmmla_z32_zzz`

**Architecture**: `FEAT_SVE_F16F32MM` (ARMv9.6)

**Summary**: Half-precision matrix multiply-accumulate to single-precision

**Description**:
This half-precision widening matrix multiply-accumulate
instruction performs two fused sums-of-products within each two pairs
of adjacent half-precision elements while
multiplying the 2×4 matrix of half-precision values held in each
128-bit segment of the first source vector by the 4×2 matrix of
half-precision values in the corresponding segment of the second source vector.
The intermediate sums-of-products are rounded before they are summed,
and their intermediate sum is rounded before accumulation into the 2×2 single-precision
matrix in the corresponding segment of the destination vector.
This is equivalent to performing a 4-way dot product per destination element.

This instruction is unpredicated.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: SM Policy: `SM_0_only`

### Variant: `SVE2`
- **Assembly**: `FMMLA  <Zda>.S, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15   9   4  |
|-----------------------------|
| 011 0010 0   00  1   Zm  111001 Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fmmla.sve_fp_fmmla.fmmla_z32_zzz_h)

```
if !IsFeatureImplemented(FEAT_SVE_F16F32MM) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Execute (A64.sve.sve_fp_fmmla.sve_fp_fmmla.fmmla_z32_zzz_h)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments =  VL DIV 128;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

for s = 0 to segments-1
    constant bits(128) op1    = Elem[operand1, s, 128];
    constant bits(128) op2    = Elem[operand2, s, 128];
    constant bits(128) addend = Elem[operand3, s, 128];
    Elem[result, s, 128] = FPMatMulAddH(addend, op1, op2, FPCR);

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_F16F32MM)` |

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
- source: `fmmla_z32_zzz.xml`
</details>