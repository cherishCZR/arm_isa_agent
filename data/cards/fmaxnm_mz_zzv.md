## FMAXNM
_ARM A64 Instruction_

**Title**: FMAXNM (multiple and single vector) -- A64 | **Class**: `mortlach2` | **XML ID**: `fmaxnm_mz_zzv`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector floating-point maximum number by vector

**Description**:
This instruction determines the maximum number value of
floating-point elements of the
second source vector and
the corresponding floating-point elements of the two or four first source vectors and
destructively places the results in the corresponding elements of the two or four first
source vectors.

Regardless of the value of FPCR.AH, the behavior is as follows:

This instruction follows SME2 floating-point numerical behaviors
corresponding to instructions that place their results in one or more
SVE Z vectors.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two registers`
- **Assembly**: `FMAXNM  { <Zdn1>.<T>-<Zdn2>.<T> }, { <Zdn1>.<T>-<Zdn2>.<T> }, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15  10  9   7   5  4   0 |
|--------------------------------------------|
| 1   10  0000 1   ?   10  Zm  10100 0   01  00  1   Zdn 0   |
```

#### Decode (A64.sme.mortlach_multi_sve_2a.mortlach_multi2_z_z_fminmax_sm.fmaxnm_mz_zzv_2x1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer dn = UInt(Zdn:'0');
constant integer m = UInt('0':Zm);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_sve_2a.mortlach_multi2_z_z_fminmax_sm.fmaxnm_mz_zzv_2x1)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
array [0..3] of bits(VL) results;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[dn+r, VL];
    constant bits(VL) operand2 = Z[m, VL];
    for e = 0 to elements-1
        constant bits(esize) element1 = Elem[operand1, e, esize];
        constant bits(esize) element2 = Elem[operand2, e, esize];
        Elem[results[r], e, esize] = FPMaxNum(element1, element2, FPCR);

for r = 0 to nreg-1
    Z[dn+r, VL] = results[r];
```

### Variant: `Four registers`
- **Assembly**: `FMAXNM  { <Zdn1>.<T>-<Zdn4>.<T> }, { <Zdn1>.<T>-<Zdn4>.<T> }, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15  10  9   7   5  4   1  0 |
|-----------------------------------------------|
| 1   10  0000 1   ?   10  Zm  10101 0   01  00  1   Zdn 0   0   |
```

#### Decode (A64.sme.mortlach_multi_sve_2b.mortlach_multi4_z_z_fminmax_sm.fmaxnm_mz_zzv_4x1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer dn = UInt(Zdn:'00');
constant integer m = UInt('0':Zm);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn1>` | `register (128-bit)` | `Zdn` | For the "Two registers" variant: is the name of the first scalable vector register of the destination and first source multi-vector group, encoded as  |
| `<Zdn1>` | `register (128-bit)` | `Zdn` | For the "Four registers" variant: is the name of the first scalable vector register of the destination and first source multi-vector group, encoded as |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zdn2>` | `register (128-bit)` | `Zdn` | Is the name of the second scalable vector register of the destination and first source multi-vector group, encoded as "Zdn" times 2 plus 1. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<Zdn4>` | `register (128-bit)` | `Zdn` | Is the name of the fourth scalable vector register of the destination and first source multi-vector group, encoded as "Zdn" times 4 plus 3. |

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
- source: `fmaxnm_mz_zzv.xml`
</details>