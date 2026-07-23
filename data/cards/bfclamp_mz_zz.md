## BFCLAMP
_ARM A64 Instruction_

**Title**: BFCLAMP -- A64 | **Class**: `mortlach2` | **XML ID**: `bfclamp_mz_zz`

**Architecture**: `FEAT_SME2 && FEAT_SVE_B16B16` (FEAT_SME2 && FEAT_SVE_B16B16)

**Summary**: Multi-vector BFloat16 clamp to minimum/maximum number

**Description**:
This instruction clamps each BFloat16 element in the two or four destination vectors
to between the BFloat16 minimum value in the corresponding element of the
first source vector and the BFloat16 maximum value in the corresponding element
of the second source vector and destructively places the clamped results
in the corresponding elements of the two or four destination vectors.

Regardless of the value of FPCR.AH, the behavior is as follows for each minimum number and maximum number operation:

This instruction follows SME2 non-widening BFloat16 numerical behaviors
corresponding to instructions that place their results in two or four SVE Z vectors.

This instruction is unpredicated.

ID_AA64ZFR0_EL1.B16B16 indicates whether this instruction is implemented.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two registers`
- **Assembly**: `BFCLAMP  { <Zd1>.H-<Zd2>.H }, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   00  1   Zm  110 000 Zn  Zd  0   |
```

#### Decode (A64.sme.mortlach_multi_sve_3.mortlach_multi2_fclamp.bfclamp_mz_zz_2)

```
if !IsFeatureImplemented(FEAT_SME2) || !IsFeatureImplemented(FEAT_SVE_B16B16) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd:'0');
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_sve_3.mortlach_multi2_fclamp.bfclamp_mz_zz_2)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
array [0..3] of bits(VL) results;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[n, VL];
    constant bits(VL) operand2 = Z[m, VL];
    constant bits(VL) operand3 = Z[d+r, VL];
    for e = 0 to elements-1
        constant bits(16) element1 = Elem[operand1, e, 16];
        constant bits(16) element2 = Elem[operand2, e, 16];
        constant bits(16) element3 = Elem[operand3, e, 16];
        constant bits(16) maxelement = BFMaxNum(element1, element3, FPCR);
        Elem[results[r], e, 16] = BFMinNum(maxelement, element2, FPCR);

for r = 0 to nreg-1
    Z[d+r, VL] = results[r];
```

### Variant: `Four registers`
- **Assembly**: `BFCLAMP  { <Zd1>.H-<Zd4>.H }, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4   1  0 |
|-----------------------------------------|
| 1   10  0000 1   00  1   Zm  110 010 Zn  Zd  0   0   |
```

#### Decode (A64.sme.mortlach_multi_sve_3.mortlach_multi4_fclamp.bfclamp_mz_zz_4)

```
if !IsFeatureImplemented(FEAT_SME2) || !IsFeatureImplemented(FEAT_SVE_B16B16) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd:'00');
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Two registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Four registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 4. |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<Zd4>` | `register (128-bit)` | `Zd` | Is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus 3. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) && IsFeatureImplemented(FEAT_SVE_B16B16)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfclamp_mz_zz.xml`
</details>