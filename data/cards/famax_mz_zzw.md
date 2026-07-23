## FAMAX
_ARM A64 Instruction_

**Title**: FAMAX -- A64 | **Class**: `mortlach2` | **XML ID**: `famax_mz_zzw`

**Architecture**: `FEAT_SME2 && FEAT_FAMINMAX` (FEAT_SME2 && FEAT_FAMINMAX)

**Summary**: Multi-vector floating-point absolute maximum

**Description**:
This instruction determines the maximum absolute value from floating-point elements of the
two or four second source vectors and
the corresponding floating-point elements of the two or four
first source vectors and destructively places the results in the corresponding elements of the two or four first
source vectors.

Regardless of the value of FPCR.AH, the behavior is as follows:

This instruction follows SME2 floating-point numerical behaviors
corresponding to instructions that place their results in one or more
SVE Z vectors.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two registers`
- **Assembly**: `FAMAX  { <Zdn1>.<T>-<Zdn2>.<T> }, { <Zdn1>.<T>-<Zdn2>.<T> }, { <Zm1>.<T>-<Zm2>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  16   9   6   4   0 |
|--------------------------------------|
| 1   10  0000 1   size 1   Zm  0101100 010 10  Zdn 0   |
```

#### Decode (A64.sme.mortlach_multi_sve_2c0.mortlach_multi2_z_z_fminmax_mm.famax_mz_zzw_2x2)

```
if !IsFeatureImplemented(FEAT_SME2) || !IsFeatureImplemented(FEAT_FAMINMAX) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer dn = UInt(Zdn:'0');
constant integer m = UInt(Zm:'0');
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_sve_2c0.mortlach_multi2_z_z_fminmax_mm.famax_mz_zzw_2x2)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
array [0..3] of bits(VL) results;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[dn+r, VL];
    constant bits(VL) operand2 = Z[m+r, VL];
    for e = 0 to elements-1
        constant bits(esize) element1 = Elem[operand1, e, esize];
        constant bits(esize) element2 = Elem[operand2, e, esize];
        Elem[results[r], e, esize] = FPAbsMax(element1, element2, FPCR);

for r = 0 to nreg-1
    Z[dn+r, VL] = results[r];
```

### Variant: `Four registers`
- **Assembly**: `FAMAX  { <Zdn1>.<T>-<Zdn4>.<T> }, { <Zdn1>.<T>-<Zdn4>.<T> }, { <Zm1>.<T>-<Zm4>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17   9   6   4   1  0 |
|-----------------------------------------|
| 1   10  0000 1   size 1   Zm  00101110 010 10  Zdn 0   0   |
```

#### Decode (A64.sme.mortlach_multi_sve_2d0.mortlach_multi4_z_z_fminmax_mm.famax_mz_zzw_4x4)

```
if !IsFeatureImplemented(FEAT_SME2) || !IsFeatureImplemented(FEAT_FAMINMAX) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer dn = UInt(Zdn:'00');
constant integer m = UInt(Zm:'00');
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn1>` | `register (128-bit)` | `Zdn` | For the "Two registers" variant: is the name of the first scalable vector register of the destination and first source multi-vector group, encoded as  |
| `<Zdn1>` | `register (128-bit)` | `Zdn` | For the "Four registers" variant: is the name of the first scalable vector register of the destination and first source multi-vector group, encoded as |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zdn2>` | `register (128-bit)` | `Zdn` | Is the name of the second scalable vector register of the destination and first source multi-vector group, encoded as "Zdn" times 2 plus 1. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Two registers" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" times 2. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Four registers" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" times 4. |
| `<Zm2>` | `register (128-bit)` | `Zm` | Is the name of the second scalable vector register of the second source multi-vector group, encoded as "Zm" times 2 plus 1. |
| `<Zdn4>` | `register (128-bit)` | `Zdn` | Is the name of the fourth scalable vector register of the destination and first source multi-vector group, encoded as "Zdn" times 4 plus 3. |
| `<Zm4>` | `register (128-bit)` | `Zm` | Is the name of the fourth scalable vector register of the second source multi-vector group, encoded as "Zm" times 4 plus 3. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) && IsFeatureImplemented(FEAT_FAMINMAX)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `famax_mz_zzw.xml`
</details>