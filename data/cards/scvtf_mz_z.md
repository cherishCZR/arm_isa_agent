## SCVTF
_ARM A64 Instruction_

**Title**: SCVTF -- A64 | **Class**: `mortlach2` | **XML ID**: `scvtf_mz_z`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector signed integer convert to floating-point

**Description**:
This instruction converts each element of the two or four source vectors from signed 32-bit
integer to single-precision floating-point, and places the results
in the corresponding elements of the two or four destination vectors.

This instruction follows SME2 floating-point numerical behaviors
corresponding to instructions that place their results in one or more
SVE Z vectors.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two registers`
- **Assembly**: `SCVTF  { <Zd1>.S-<Zd2>.S }, { <Zn1>.S-<Zn2>.S }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   5  4   0 |
|-----------------------------------------|
| 1   10  0000 1   00  1   000 10  111000 Zn  0   Zd  0   |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi2_intfp_cvrt.scvtf_mz_z_2)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn:'0');
constant integer d = UInt(Zd:'0');
constant integer nreg = 2;
constant boolean unsigned = FALSE;
constant FPRounding rounding = FPRoundingMode(FPCR);
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi2_intfp_cvrt.scvtf_mz_z_2)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 32;
array [0..3] of bits(VL) results;

for r = 0 to nreg-1
    constant bits(VL) operand = Z[n+r, VL];
    for e = 0 to elements-1
        constant bits(32) element = Elem[operand, e, 32];
        Elem[results[r], e, 32] = FixedToFP(element, 0, unsigned, FPCR, rounding, 32);

for r = 0 to nreg-1
    Z[d+r, VL] = results[r];
```

### Variant: `Four registers`
- **Assembly**: `SCVTF  { <Zd1>.S-<Zd4>.S }, { <Zn1>.S-<Zn4>.S }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   6  5  4   1  |
|--------------------------------------------|
| 1   10  0000 1   00  1   100 10  111000 Zn  0   0   Zd  00  |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi4_intfp_cvrt.scvtf_mz_z_4)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn:'00');
constant integer d = UInt(Zd:'00');
constant integer nreg = 4;
constant boolean unsigned = FALSE;
constant FPRounding rounding = FPRoundingMode(FPCR);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Two registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Four registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 4. |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Two registers" variant: is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 2. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Four registers" variant: is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 4. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zd4>` | `register (128-bit)` | `Zd` | Is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus 3. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the source multi-vector group, encoded as "Zn" times 4 plus 3. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `scvtf_mz_z.xml`
</details>