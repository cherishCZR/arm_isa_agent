## URSHL
_ARM A64 Instruction_

**Title**: URSHL (multiple vectors) -- A64 | **Class**: `mortlach2` | **XML ID**: `urshl_mz_zzw`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector unsigned rounding shift left

**Description**:
This instruction shifts the unsigned elements of the two or four first source vectors by corresponding
elements of the two or four second source vectors and destructively places the rounded
results in the corresponding elements of the two or four first source vectors. A positive
shift amount performs a left shift, otherwise a right shift by the negated shift amount is performed.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two registers`
- **Assembly**: `URSHL  { <Zdn1>.<T>-<Zdn2>.<T> }, { <Zdn1>.<T>-<Zdn2>.<T> }, { <Zm1>.<T>-<Zm2>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  16   9   7   4   0 |
|--------------------------------------|
| 1   10  0000 1   size 1   Zm  0101100 10  001 Zdn 1   |
```

#### Decode (A64.sme.mortlach_multi_sve_2c0.mortlach_multi2_z_z_shift_mm.urshl_mz_zzw_2x2)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer dn = UInt(Zdn:'0');
constant integer m = UInt(Zm:'0');
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_sve_2c0.mortlach_multi2_z_z_shift_mm.urshl_mz_zzw_2x2)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
array [0..3] of bits(VL) results;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[dn+r, VL];
    constant bits(VL) operand2 = Z[m+r, VL];
    for e = 0 to elements-1
        constant integer element =  UInt(Elem[operand1, e, esize]);
        integer shift = ShiftSat(SInt(Elem[operand2, e, esize]), esize);
        integer res;
        if shift >= 0 then
            res = element << shift;
        else
            shift = -shift;
            res = (element + (1 << (shift - 1))) >> shift;
        Elem[results[r], e, esize] = res<esize-1:0>;

for r = 0 to nreg-1
    Z[dn+r, VL] = results[r];
```

### Variant: `Four registers`
- **Assembly**: `URSHL  { <Zdn1>.<T>-<Zdn4>.<T> }, { <Zdn1>.<T>-<Zdn4>.<T> }, { <Zm1>.<T>-<Zm4>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17   9   7   4   1  0 |
|-----------------------------------------|
| 1   10  0000 1   size 1   Zm  00101110 10  001 Zdn 0   1   |
```

#### Decode (A64.sme.mortlach_multi_sve_2d0.mortlach_multi4_z_z_shift_mm.urshl_mz_zzw_4x4)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
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
| 00 | B |
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
- source: `urshl_mz_zzw.xml`
</details>