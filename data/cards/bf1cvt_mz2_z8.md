## bf1cvt_mz2_z8
_ARM A64 Instruction_

**Title**: BF1CVT, BF2CVT -- A64 | **Class**: `mortlach2` | **XML ID**: `bf1cvt_mz2_z8`

**Architecture**: `FEAT_SME2 && FEAT_FP8` (FEAT_SME2 && FEAT_FP8)

**Summary**: Multi-vector convert from 8-bit floating-point to BFloat16 (in-order)

**Description**:
This instruction converts each 8-bit floating-point element of the source vector to BFloat16 while downscaling the value,
and places the  results in the corresponding 16-bit elements
of the destination vectors. BF1CVT scales the values by 2-UInt(FPMR.LSCALE[5:0]).
BF2CVT scales the values by 2-UInt(FPMR.LSCALE2[5:0]).
The 8-bit floating-point encoding format for BF1CVT is selected by FPMR.F8S1.
The 8-bit floating-point encoding format for BF2CVT is selected by FPMR.F8S2.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `BF1CVT`
- **Assembly**: `BF1CVT  { <Zd1>.H-<Zd2>.H }, <Zn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   01  1   001 10  111000 Zn  Zd  0   |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_fp8_cvrt.bf1cvt_mz2_z8_)

```
if !IsFeatureImplemented(FEAT_SME2) || !IsFeatureImplemented(FEAT_FP8) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd: '0');
constant boolean issrc2 = FALSE;
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_fp8_cvrt.bf1cvt_mz2_z8_)

```
CheckFPMREnabled();
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 8;
constant bits(VL) operand = Z[n, VL];
bits(2*VL) result;

for e = 0 to elements-1
    constant bits(8) element = Elem[operand, e, 8];
    Elem[result, e, 16] = FP8ConvertBF(element, issrc2, FPCR, FPMR);

Z[d+0, VL] = result<VL-1:0>;
Z[d+1, VL] = result<2*VL-1:VL>;
```

### Variant: `BF2CVT`
- **Assembly**: `BF2CVT  { <Zd1>.H-<Zd2>.H }, <Zn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   11  1   001 10  111000 Zn  Zd  0   |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_fp8_cvrt.bf2cvt_mz2_z8_)

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
- source: `bf1cvt_mz2_z8.xml`
</details>