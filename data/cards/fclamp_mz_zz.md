## FCLAMP
_ARM A64 Instruction_

**Title**: FCLAMP -- A64 | **Class**: `mortlach2` | **XML ID**: `fclamp_mz_zz`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector floating-point clamp to minimum/maximum number

**Description**:
This instruction clamps each floating-point element in the two or four destination vectors
to between the floating-point minimum value in the corresponding element of the
first source vector and the floating-point maximum value in the corresponding element
of the second source vector and destructively places the clamped results
in the corresponding elements of the two or four destination vectors.

Regardless of the value of FPCR.AH, the behavior is as follows for each minimum number and maximum number operation:

This instruction follows SME2 floating-point numerical behaviors
corresponding to instructions that place their results in one or more
SVE Z vectors.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two registers`
- **Assembly**: `FCLAMP  { <Zd1>.<T>-<Zd2>.<T> }, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   ?   1   Zm  110 000 Zn  Zd  0   |
```

#### Decode (A64.sme.mortlach_multi_sve_3.mortlach_multi2_fclamp.fclamp_mz_zz_2)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd:'0');
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_sve_3.mortlach_multi2_fclamp.fclamp_mz_zz_2)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
array [0..3] of bits(VL) results;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[n, VL];
    constant bits(VL) operand2 = Z[m, VL];
    constant bits(VL) operand3 = Z[d+r, VL];
    for e = 0 to elements-1
        constant bits(esize) element1 = Elem[operand1, e, esize];
        constant bits(esize) element2 = Elem[operand2, e, esize];
        constant bits(esize) element3 = Elem[operand3, e, esize];
        constant bits(esize) maxelement = FPMaxNum(element1, element3, FPCR);
        Elem[results[r], e, esize] = FPMinNum(maxelement, element2, FPCR);

for r = 0 to nreg-1
    Z[d+r, VL] = results[r];
```

### Variant: `Four registers`
- **Assembly**: `FCLAMP  { <Zd1>.<T>-<Zd4>.<T> }, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4   1  0 |
|-----------------------------------------|
| 1   10  0000 1   ?   1   Zm  110 010 Zn  Zd  0   0   |
```

#### Decode (A64.sme.mortlach_multi_sve_3.mortlach_multi4_fclamp.fclamp_mz_zz_4)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
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
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<Zd4>` | `register (128-bit)` | `Zd` | Is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus 3. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 01 | H |
| 10 | S |
| 11 | D |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fclamp_mz_zz.xml`
</details>