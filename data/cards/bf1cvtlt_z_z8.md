## bf1cvtlt_z_z8
_ARM A64 Instruction_

**Title**: BF1CVTLT, BF2CVTLT -- A64 | **Class**: `sve2` | **XML ID**: `bf1cvtlt_z_z8`

**Architecture**: `(FEAT_SVE2 || FEAT_SME2) && FEAT_FP8` ((FEAT_SVE2 || FEAT_SME2) && FEAT_FP8)

**Summary**: 8-bit floating-point convert to BFloat16 (top)

**Description**:
Convert each odd-numbered 8-bit floating-point element of the source vector
to BFloat16 while downscaling the value, and place the results
in the overlapping 16-bit elements of the destination vector.
BF1CVTLT scales the values by 2-UInt(FPMR.LSCALE[5:0]).
BF2CVTLT scales the values by 2-UInt(FPMR.LSCALE2[5:0]).

The 8-bit floating-point encoding format for BF1CVTLT is selected by FPMR.F8S1.
The 8-bit floating-point encoding format for BF2CVTLT is selected by FPMR.F8S2.

This instruction is unpredicated.

### Variant: `BF1CVTLT`
- **Assembly**: `BF1CVTLT  <Zd>.H, <Zn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  16 15  11   9   4  |
|-----------------------------------|
| 011 0010 1   00  001 00  1   0011 10  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unary_unpred.sve_fp8_fcvt_wide.bf1cvtlt_z_z8_b2bf)

```
if ((!IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME2)) ||
      !IsFeatureImplemented(FEAT_FP8)) then EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean issrc2 = FALSE;
```

#### Execute (A64.sve.sve_fp_unary_unpred.sve_fp8_fcvt_wide.bf1cvtlt_z_z8_b2bf)

```
CheckFPMREnabled();
if IsFeatureImplemented(FEAT_SME2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand = Z[n, VL];
bits(VL) result;
for e = 0 to elements-1
    constant bits(esize DIV 2) element = Elem[operand, 2*e + 1, esize DIV 2];
    Elem[result, e, esize] = FP8ConvertBF(element, issrc2, FPCR, FPMR);

Z[d, VL] = result;
```

### Variant: `BF2CVTLT`
- **Assembly**: `BF2CVTLT  <Zd>.H, <Zn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  16 15  11   9   4  |
|-----------------------------------|
| 011 0010 1   00  001 00  1   0011 11  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unary_unpred.sve_fp8_fcvt_wide.bf2cvtlt_z_z8_b2bf)

```
if ((!IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME2)) ||
      !IsFeatureImplemented(FEAT_FP8)) then EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean issrc2 = TRUE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `((IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME2)) && IsFeatureImplemented(FEAT_FP8))` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bf1cvtlt_z_z8.xml`
</details>