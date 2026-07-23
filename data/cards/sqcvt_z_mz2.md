## SQCVT
_ARM A64 Instruction_

**Title**: SQCVT (two registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `sqcvt_z_mz2`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector signed saturating extract narrow

**Description**:
This instruction saturates the signed integer value in each element of the two source
vectors to  half the original source element width, and places the   results in the half-width
destination elements.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `SQCVT  <Zd>.H, { <Zn1>.S-<Zn2>.S }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23 22 21 20  17  15   9   5  4  |
|-----------------------------------------|
| 1   10  0000 1   0   0   1   000 11  111000 Zn  0   Zd  |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi2_narrow_int_cvrt.sqcvt_z_mz2_)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer n = UInt(Zn:'0');
constant integer d = UInt(Zd);
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi2_narrow_int_cvrt.sqcvt_z_mz2_)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV (2 * esize);
bits(VL) result;

for r = 0 to 1
    constant bits(VL) operand = Z[n+r, VL];
    for e = 0 to elements-1
        constant integer element = SInt(Elem[operand, e, 2 * esize]);
        Elem[result, r*elements + e, esize] = SignedSat(element, esize);

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
- source: `sqcvt_z_mz2.xml`
</details>