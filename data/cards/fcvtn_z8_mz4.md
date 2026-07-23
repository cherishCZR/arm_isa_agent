## FCVTN
_ARM A64 Instruction_

**Title**: FCVTN (FP32 to FP8) -- A64 | **Class**: `mortlach2` | **XML ID**: `fcvtn_z8_mz4`

**Architecture**: `FEAT_SME2 && FEAT_FP8` (FEAT_SME2 && FEAT_FP8)

**Summary**: Multi-vector convert from single-precision to interleaved 8-bit floating-point format

**Description**:
This instruction converts each single-precision element of the four source vectors to 8-bit floating-point while
scaling the value by 2SInt(FPMR.NSCALE), and places the four-way interleaved results in the quarter-width
elements of the destination vector.
The 8-bit floating-point encoding format is selected by FPMR.F8D.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `FCVTN  <Zd>.B, { <Zn1>.S-<Zn4>.S }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   6  5  4  |
|-----------------------------------------|
| 1   10  0000 1   00  1   101 00  111000 Zn  0   1   Zd  |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi4_narrow_fp8_cvrt.fcvtn_z8_mz4_)

```
if !IsFeatureImplemented(FEAT_SME2) || !IsFeatureImplemented(FEAT_FP8) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn:'00');
constant integer d = UInt(Zd);
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi4_narrow_fp8_cvrt.fcvtn_z8_mz4_)

```
CheckFPMREnabled();
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 32;
bits(VL) result;

constant bits(VL) operand1 = Z[n+0, VL];
constant bits(VL) operand2 = Z[n+1, VL];
constant bits(VL) operand3 = Z[n+2, VL];
constant bits(VL) operand4 = Z[n+3, VL];
for e = 0 to elements-1
    constant bits(32) element1 = Elem[operand1, e, 32];
    constant bits(32) element2 = Elem[operand2, e, 32];
    constant bits(32) element3 = Elem[operand3, e, 32];
    constant bits(32) element4 = Elem[operand4, e, 32];
    Elem[result, 4*e + 0, 8] = FPConvertFP8(element1, FPCR, FPMR, 8);
    Elem[result, 4*e + 1, 8] = FPConvertFP8(element2, FPCR, FPMR, 8);
    Elem[result, 4*e + 2, 8] = FPConvertFP8(element3, FPCR, FPMR, 8);
    Elem[result, 4*e + 3, 8] = FPConvertFP8(element4, FPCR, FPMR, 8);

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
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 4. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the source multi-vector group, encoded as "Zn" times 4 plus 3. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvtn_z8_mz4.xml`
</details>