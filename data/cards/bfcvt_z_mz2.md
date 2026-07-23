## BFCVT
_ARM A64 Instruction_

**Title**: BFCVT (single-precision to BFloat16) -- A64 | **Class**: `mortlach2` | **XML ID**: `bfcvt_z_mz2`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector convert from single-precision to packed BFloat16 format

**Description**:
This instruction converts each element of the
two source vectors from single-precision to BFloat16 floating-point, and places the  results
in the half-width destination elements.

This instruction follows SME2 floating-point numerical behaviors
corresponding to instructions that place their results in one or more
SVE Z vectors.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `BFCVT  <Zd>.H, { <Zn1>.S-<Zn2>.S }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23 22 21 20  17  15   9   5  4  |
|-----------------------------------------|
| 1   10  0000 1   0   1   1   000 00  111000 Zn  0   Zd  |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi2_narrow_fp_cvrt.bfcvt_z_mz2_)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn:'0');
constant integer d = UInt(Zd);
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi2_narrow_fp_cvrt.bfcvt_z_mz2_)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 32;
bits(VL) result;

constant bits(VL) operand1 = Z[n+0, VL];
constant bits(VL) operand2 = Z[n+1, VL];
for e = 0 to elements-1
    constant bits(32) element1 = Elem[operand1, e, 32];
    constant bits(32) element2 = Elem[operand2, e, 32];
    constant bits(16) res1 = FPConvertBF(element1, FPCR);
    constant bits(16) res2 = FPConvertBF(element2, FPCR);
    Elem[result, e, 16] = res1;
    Elem[result, elements+e, 16] = res2;

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 2. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zn" times 2 plus 1. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfcvt_z_mz2.xml`
</details>