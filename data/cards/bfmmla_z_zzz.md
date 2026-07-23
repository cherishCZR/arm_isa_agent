## BFMMLA
_ARM A64 Instruction_

**Title**: BFMMLA (widening) -- A64 | **Class**: `sve` | **XML ID**: `bfmmla_z_zzz`

**Architecture**: `FEAT_SVE && FEAT_BF16` (FEAT_SVE && FEAT_BF16)

**Summary**: BFloat16 matrix multiply-accumulate to single-precision

**Description**:
If FEAT_EBF16 is not implemented or FPCR.EBF is 0,
this instruction:

If FEAT_EBF16 is implemented and FPCR.EBF is 1,
then this instruction:

Irrespective of FEAT_EBF16 and FPCR.EBF, this instruction:

This instruction is unpredicated and
vector length agnostic.

ID_AA64ZFR0_EL1.BF16 indicates whether this instruction is implemented.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: SM Policy: `SM_0_only`

### Variant: `SVE`
- **Assembly**: `BFMMLA  <Zda>.S, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15   9   4  |
|-----------------------------|
| 011 0010 0   01  1   Zm  111001 Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fmmla.sve_fp_fmmla.bfmmla_z_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE) || !IsFeatureImplemented(FEAT_BF16) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Execute (A64.sve.sve_fp_fmmla.sve_fp_fmmla.bfmmla_z_zzz_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments =  VL DIV 128;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;
bits(128) op1, op2;
bits(128) res, addend;

for s = 0 to segments-1
    op1    = Elem[operand1, s, 128];
    op2    = Elem[operand2, s, 128];
    addend = Elem[operand3, s, 128];
    res    = BFMatMulAddH(addend, op1, op2,  FPCR);
    Elem[result, s, 128] = res;

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) && IsFeatureImplemented(FEAT_BF16)` |

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
- source: `bfmmla_z_zzz.xml`
</details>