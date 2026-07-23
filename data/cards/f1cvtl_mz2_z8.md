## f1cvtl_mz2_z8
_ARM A64 Instruction_

**Title**: F1CVTL, F2CVTL -- A64 | **Class**: `mortlach2` | **XML ID**: `f1cvtl_mz2_z8`

**Architecture**: `FEAT_SME2 && FEAT_FP8` (FEAT_SME2 && FEAT_FP8)

**Summary**: Multi-vector convert from 8-bit floating-point to deinterleaved half-precision

**Description**:
This instruction converts each 8-bit floating-point element of the source vector to half-precision while downscaling the value,
and places the two-way deinterleaved results in the corresponding 16-bit elements
of the destination vectors. F1CVTL scales the values by 2-UInt(FPMR.LSCALE[3:0]).
F2CVTL scales the values by 2-UInt(FPMR.LSCALE2[3:0]).
The 8-bit floating-point encoding format for F1CVTL is selected by FPMR.F8S1.
The 8-bit floating-point encoding format for F2CVTL is selected by FPMR.F8S2.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `F1CVTL`
- **Assembly**: `F1CVTL  { <Zd1>.H-<Zd2>.H }, <Zn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   00  1   001 10  111000 Zn  Zd  1   |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_fp8_cvrt.f1cvtl_mz2_z8_)

```
if !IsFeatureImplemented(FEAT_SME2) || !IsFeatureImplemented(FEAT_FP8) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd: '0');
constant boolean issrc2 = FALSE;
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_fp8_cvrt.f1cvtl_mz2_z8_)

```
CheckFPMREnabled();
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer pairs = VL DIV 16;
constant bits(VL) operand = Z[n, VL];
bits(VL) result1;
bits(VL) result2;

for p = 0 to pairs-1
    constant bits(8) element1 = Elem[operand, 2*p + 0, 8];
    constant bits(8) element2 = Elem[operand, 2*p + 1, 8];
    Elem[result1, p, 16] = FP8ConvertFP(element1, issrc2, FPCR, FPMR);
    Elem[result2, p, 16] = FP8ConvertFP(element2, issrc2, FPCR, FPMR);

Z[d+0, VL] = result1;
Z[d+1, VL] = result2;
```

### Variant: `F2CVTL`
- **Assembly**: `F2CVTL  { <Zd1>.H-<Zd2>.H }, <Zn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   10  1   001 10  111000 Zn  Zd  1   |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_fp8_cvrt.f2cvtl_mz2_z8_)

```
if !IsFeatureImplemented(FEAT_SME2) || !IsFeatureImplemented(FEAT_FP8) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd: '0');
constant boolean issrc2 = TRUE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | Is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) && IsFeatureImplemented(FEAT_FP8)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `f1cvtl_mz2_z8.xml`
</details>