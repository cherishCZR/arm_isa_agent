## CDOT
_ARM A64 Instruction_

**Title**: CDOT (indexed) -- A64 | **Class**: `sve2` | **XML ID**: `cdot_z_zzzi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Complex integer dot product (indexed)

**Description**:
The complex integer dot product
instructions delimit the source vectors into pairs of
8-bit or 16-bit signed integer complex numbers.
Within each pair, the complex numbers in the first
source vector are multiplied by the corresponding
complex numbers in the second source vector and the
resulting wide real or wide imaginary part of the
product is accumulated into a 32-bit or 64-bit
destination vector element which overlaps all four of
the elements that comprise a pair of complex number
values in the first source vector.

As a result each instruction implicitly deinterleaves
the real and imaginary components of their complex
number inputs, so that the destination vector
accumulates 4×wide real sums or 4×wide
imaginary sums.

The complex numbers in the second source vector are
rotated by 0, 90, 180 or 270 degrees in the direction
from the positive real axis towards the positive
imaginary axis, when considered in polar
representation, by performing the following
transformations prior to the dot product operations:

The indexed form of these instructions select a
single pair of complex numbers within each 128-bit
segment of the second source vector as the multiplier
for all pairs of complex numbers within the
corresponding 128-bit segment of the first source
vector.
The complex number pairs within the second source vector are specified using
an immediate index which selects the same complex number pair position within
each 128-bit vector segment.  The index range is from 0 to
one less than the number of complex number pairs per 128-bit segment.

Each complex number is represented in a vector register as an
even/odd pair of elements with the real part in the
even-numbered element and the imaginary part in the
odd-numbered element.

### Variant: `8-bit to 32-bit`
- **Assembly**: `CDOT  <Zda>.S, <Zn>.B, <Zm>.B[<imm>], <const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  11   9   4  |
|-----------------------------------|
| 010 0010 0   10  1   i2  Zm  0100 rot Zn  Zda |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_cdot_by_indexed_elem.cdot_z_zzzi_s)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer index = UInt(i2);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer sel_a = UInt(rot<0>);
constant integer sel_b = UInt(NOT(rot<0>));
constant boolean sub_i = (rot<0> == rot<1>);
```

#### Execute (A64.sve.sve_intx_by_indexed_elem.sve_intx_cdot_by_indexed_elem.cdot_z_zzzi_s)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer eltspersegment = 128 DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer segmentbase = e - (e MOD eltspersegment);
    constant integer s = segmentbase + index;
    bits(esize) res = Elem[operand3, e, esize];
    for i = 0 to 1
        constant integer elt1_r = SInt(Elem[operand1, 4 * e + 2 * i + 0, esize DIV 4]);
        constant integer elt1_i = SInt(Elem[operand1, 4 * e + 2 * i + 1, esize DIV 4]);
        constant integer elt2_a = SInt(Elem[operand2, 4 * s + 2 * i + sel_a, esize DIV 4]);
        constant integer elt2_b = SInt(Elem[operand2, 4 * s + 2 * i + sel_b, esize DIV 4]);
        if sub_i then
            res = (res + (elt1_r * elt2_a)) - (elt1_i * elt2_b);
        else
            res = res + (elt1_r * elt2_a) + (elt1_i * elt2_b);
    Elem[result, e, esize] = res;

Z[da, VL] = result;
```

### Variant: `16-bit to 64-bit`
- **Assembly**: `CDOT  <Zda>.D, <Zn>.H, <Zm>.H[<imm>], <const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  11   9   4  |
|-----------------------------------|
| 010 0010 0   11  1   i1  Zm  0100 rot Zn  Zda |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_cdot_by_indexed_elem.cdot_z_zzzi_d)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer index = UInt(i1);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer sel_a = UInt(rot<0>);
constant integer sel_b = UInt(NOT(rot<0>));
constant boolean sub_i = (rot<0> == rot<1>);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "8-bit to 32-bit" variant: is the name of the second source scalable vector register Z0-Z7, encoded in the "Zm" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "16-bit to 64-bit" variant: is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `i2` | For the "8-bit to 32-bit" variant: is the immediate index of a 32-bit group of four 8-bit values within each 128-bit vector segment, in the range 0 to |
| `<imm>` | `immediate` | `i1` | For the "16-bit to 64-bit" variant: is the immediate index of a 64-bit group of four 16-bit values within each 128-bit vector segment, in the range 0  |
| `<const>` | `unknown` | `rot` | Is the const specifier, |

**<const> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | #0 |
| 01 | #90 |
| 10 | #180 |
| 11 | #270 |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `cdot_z_zzzi.xml`
</details>