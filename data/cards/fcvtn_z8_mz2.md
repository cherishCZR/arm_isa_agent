## FCVTN
_ARM A64 Instruction_

**Title**: FCVTN -- A64 | **Class**: `sve2` | **XML ID**: `fcvtn_z8_mz2`

**Architecture**: `(FEAT_SVE2 || FEAT_SME2) && FEAT_FP8` ((FEAT_SVE2 || FEAT_SME2) && FEAT_FP8)

**Summary**: Half-precision convert, narrow and interleave to 8-bit floating-point

**Description**:
Convert each half-precision element of the group of two source vectors to 8-bit
floating-point while scaling the value by 2SInt(FPMR.NSCALE[4:0]),
and place the two-way interleaved results in the corresponding 8-bit elements
of the destination vector. The 8-bit floating-point encoding format is selected by FPMR.F8D.

This instruction is unpredicated.

### Variant: `SVE2`
- **Assembly**: `FCVTN  <Zd>.B, { <Zn1>.H-<Zn2>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15  11   9   5  4  |
|-----------------------------------|
| 011 0010 1   00  001 010 0011 00  Zn  0   Zd  |
```

#### Decode (A64.sve.sve_fp_unary_unpred.sve_fp8_fcvt_narrow.fcvtn_z8_mz2_h2b)

```
if ((!IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME2)) ||
      !IsFeatureImplemented(FEAT_FP8)) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn:'0');
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_fp_unary_unpred.sve_fp8_fcvt_narrow.fcvtn_z8_mz2_h2b)

```
CheckFPMREnabled();
if IsFeatureImplemented(FEAT_SME2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
bits(VL) result;

constant bits(VL) operand1 = Z[n+0, VL];
constant bits(VL) operand2 = Z[n+1, VL];
for e = 0 to elements-1
    constant bits(16) element1 = Elem[operand1, e, 16];
    constant bits(16) element2 = Elem[operand2, e, 16];
    Elem[result, 2*e + 0, 8] = FPConvertFP8(element1, FPCR, FPMR, 8);
    Elem[result, 2*e + 1, 8] = FPConvertFP8(element2, FPCR, FPMR, 8);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `((IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME2)) && IsFeatureImplemented(FEAT_FP8))` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 2. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zn" times 2 plus 1. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvtn_z8_mz2.xml`
</details>