## BFCVT
_ARM A64 Instruction_

**Title**: BFCVT (BFloat16 to 8-bit floating-point) -- A64 | **Class**: `mortlach2` | **XML ID**: `bfcvt_z8_mz2`

**Architecture**: `FEAT_SME2 && FEAT_FP8` (FEAT_SME2 && FEAT_FP8)

**Summary**: Multi-vector convert from BFloat16 to packed 8-bit floating-point format

**Description**:
This instruction converts each BFloat16 element of the two source vectors to 8-bit floating-point while
scaling the value by 2SInt(FPMR.NSCALE), and places the  results in the half-width
elements of the destination vector.
The 8-bit floating-point encoding format is selected by FPMR.F8D.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `BFCVT  <Zd>.B, { <Zn1>.H-<Zn2>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23 22 21 20  17  15   9   5  4  |
|-----------------------------------------|
| 1   10  0000 1   0   1   1   001 00  111000 Zn  0   Zd  |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi2_narrow_fp8_cvrt.bfcvt_z8_mz2_)

```
if !IsFeatureImplemented(FEAT_SME2) || !IsFeatureImplemented(FEAT_FP8) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn:'0');
constant integer d = UInt(Zd);
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi2_narrow_fp8_cvrt.bfcvt_z8_mz2_)

```
CheckFPMREnabled();
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
bits(VL) result;

constant bits(VL) operand1 = Z[n+0, VL];
constant bits(VL) operand2 = Z[n+1, VL];
for e = 0 to elements-1
    constant bits(16) element1 = Elem[operand1, e, 16];
    constant bits(16) element2 = Elem[operand2, e, 16];
    Elem[result, 0*elements + e, 8] = BFConvertFP8(element1, FPCR, FPMR);
    Elem[result, 1*elements + e, 8] = BFConvertFP8(element2, FPCR, FPMR);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) && IsFeatureImplemented(FEAT_FP8)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 2. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zn" times 2 plus 1. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfcvt_z8_mz2.xml`
</details>