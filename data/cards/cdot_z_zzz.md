## CDOT
_ARM A64 Instruction_

**Title**: CDOT (vectors) -- A64 | **Class**: `sve2` | **XML ID**: `cdot_z_zzz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Complex integer dot product

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

Each complex number is represented in a vector register as an
even/odd pair of elements with the real part in the
even-numbered element and the imaginary part in the
odd-numbered element.

### Variant: `SVE2`
- **Assembly**: `CDOT  <Zda>.<T>, <Zn>.<Tb>, <Zm>.<Tb>, <const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14  11   9   4  |
|-----------------------------------|
| 010 0010 0   size 0   Zm  0   001 rot Zn  Zda |
```

#### Decode (A64.sve.sve_intx_muladd_unpred.sve_intx_cdot.cdot_z_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size IN {'0x'} then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer sel_a = UInt(rot<0>);
constant integer sel_b = UInt(NOT(rot<0>));
constant boolean sub_i = (rot<0> == rot<1>);
```

#### Execute (A64.sve.sve_intx_muladd_unpred.sve_intx_cdot.cdot_z_zzz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    bits(esize) res = Elem[operand3, e, esize];
    for i = 0 to 1
        constant integer elt1_r = SInt(Elem[operand1, 4 * e + 2 * i + 0, esize DIV 4]);
        constant integer elt1_i = SInt(Elem[operand1, 4 * e + 2 * i + 1, esize DIV 4]);
        constant integer elt2_a = SInt(Elem[operand2, 4 * e + 2 * i + sel_a, esize DIV 4]);
        constant integer elt2_b = SInt(Elem[operand2, 4 * e + 2 * i + sel_b, esize DIV 4]);
        if sub_i then
            res = (res + (elt1_r * elt2_a)) - (elt1_i * elt2_b);
        else
            res = res + (elt1_r * elt2_a) + (elt1_i * elt2_b);
    Elem[result, e, esize] = res;

Z[da, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size IN{'0x'}` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<T>` | `unknown` | `size<0>` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Tb>` | `unknown` | `size<0>` | Is the size specifier, |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<const>` | `unknown` | `rot` | Is the const specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | B |
| 1 | H |

**<const> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | #0 |
| 01 | #90 |
| 10 | #180 |
| 11 | #270 |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `cdot_z_zzz.xml`
</details>