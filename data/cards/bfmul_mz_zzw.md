## BFMUL
_ARM A64 Instruction_

**Title**: BFMUL (multiple vectors) -- A64 | **Class**: `mortlach2` | **XML ID**: `bfmul_mz_zzw`

**Architecture**: `FEAT_SME2 && FEAT_SVE_BFSCALE` (FEAT_SME2 && FEAT_SVE_BFSCALE)

**Summary**: Multi-vector BFloat16 multiply

**Description**:
This instruction multiplies all the BFloat16 elements of the two or four first source vectors with the
corresponding elements of the two or four second source vectors and places
the results in the corresponding elements of the two or four destination vectors.

This instruction follows SME2 non-widening BFloat16 numerical behaviors
corresponding to instructions that place their results in two or four SVE Z vectors.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two registers`
- **Assembly**: `BFMUL  { <Zd1>.H-<Zd2>.H }, { <Zn1>.H-<Zn2>.H }, { <Zm1>.H-<Zm2>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  16 15   9   5  4   0 |
|-----------------------------------------|
| 1   10  0000 1   00  1   Zm  0   111001 Zn  0   Zd  0   |
```

#### Decode (A64.sme.mortlach_multi_sve_5a.mortlach_multi2_fmul_mm.bfmul_mz_zzw_2x2)

```
if !IsFeatureImplemented(FEAT_SME2) || !IsFeatureImplemented(FEAT_SVE_BFSCALE) then
    EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Zd:'0');
constant integer n = UInt(Zn:'0');
constant integer m = UInt(Zm:'0');
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_sve_5a.mortlach_multi2_fmul_mm.bfmul_mz_zzw_2x2)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
array [0..3] of bits(VL) results;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[n+r, VL];
    constant bits(VL) operand2 = Z[m+r, VL];
    for e = 0 to elements-1
        constant bits(16) element1 = Elem[operand1, e, 16];
        constant bits(16) element2 = Elem[operand2, e, 16];
        Elem[results[r], e, 16] = BFMul(element1, element2, FPCR);

for r = 0 to nreg-1
    Z[d+r, VL] = results[r];
```

### Variant: `Four registers`
- **Assembly**: `BFMUL  { <Zd1>.H-<Zd4>.H }, { <Zn1>.H-<Zn4>.H }, { <Zm1>.H-<Zm4>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   6  5  4   1  0 |
|-----------------------------------------------|
| 1   10  0000 1   00  1   Zm  01  111001 Zn  0   0   Zd  0   0   |
```

#### Decode (A64.sme.mortlach_multi_sve_5a.mortlach_multi4_fmul_mm.bfmul_mz_zzw_4x4)

```
if !IsFeatureImplemented(FEAT_SME2) || !IsFeatureImplemented(FEAT_SVE_BFSCALE) then
    EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Zd:'00');
constant integer n = UInt(Zn:'00');
constant integer m = UInt(Zm:'00');
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Two registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Four registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 4. |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Two registers" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" times 2. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Four registers" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" times 4. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Two registers" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" times 2. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Four registers" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" times 4. |
| `<Zm2>` | `register (128-bit)` | `Zm` | Is the name of the second scalable vector register of the second source multi-vector group, encoded as "Zm" times 2 plus 1. |
| `<Zd4>` | `register (128-bit)` | `Zd` | Is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus 3. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" times 4 plus 3. |
| `<Zm4>` | `register (128-bit)` | `Zm` | Is the name of the fourth scalable vector register of the second source multi-vector group, encoded as "Zm" times 4 plus 3. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) && IsFeatureImplemented(FEAT_SVE_BFSCALE)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfmul_mz_zzw.xml`
</details>