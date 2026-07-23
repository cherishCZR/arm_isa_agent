## FCMLA
_ARM A64 Instruction_

**Title**: FCMLA (indexed) -- A64 | **Class**: `sve` | **XML ID**: `fcmla_z_zzzi`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point complex multiply-add by indexed values with rotate

**Description**:
Multiply the duplicated real components for rotations 0
and 180, or imaginary components for rotations 90 and
270, of the floating-point complex numbers in each 128-bit segment of the first source vector by the specified complex number in the corresponding the second source vector
segment rotated by 0, 90, 180 or 270
degrees in the direction from the positive real axis towards
the positive imaginary axis, when considered in polar
representation.

Then destructively add the products to the corresponding
components of the complex numbers in the addend and
destination vector, without intermediate rounding.

These transformations permit the creation of a variety of
multiply-add and multiply-subtract operations on complex numbers by
combining two of these instructions with the same vector operands
but with rotations that are 90 degrees apart.

Each complex number is represented in a vector register as an
even/odd pair of elements with the real part in the
even-numbered element and the imaginary part in the
odd-numbered element.

The complex numbers within the second source vector are specified using
an immediate index which selects the same complex number position within
each 128-bit vector segment.  The index range is from 0 to
one less than the number of complex numbers per 128-bit segment.
This instruction is unpredicated.

### Variant: `Half-precision`
- **Assembly**: `FCMLA  <Zda>.H, <Zn>.H, <Zm>.H[<imm>], <const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  11   9   4  |
|-----------------------------------|
| 011 0010 0   10  1   i2  Zm  0001 rot Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fcmla_by_indexed_elem.sve_fp_fcmla_by_indexed_elem.fcmla_z_zzzi_h)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer index = UInt(i2);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer sel_a = UInt(rot<0>);
constant integer sel_b = UInt(NOT(rot<0>));
constant boolean neg_i = (rot<1> == '1');
constant boolean neg_r = (rot<0> != rot<1>);
```

#### Execute (A64.sve.sve_fp_fcmla_by_indexed_elem.sve_fp_fcmla_by_indexed_elem.fcmla_z_zzzi_h)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer pairs = VL DIV (2 * esize);
constant integer pairspersegment = 128 DIV (2 * esize);
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

for p = 0 to pairs-1
    constant integer segmentbase = p - (p MOD pairspersegment);
    constant integer s = segmentbase + index;
    bits(esize) addend_r = Elem[operand3, 2 * p + 0, esize];
    bits(esize) addend_i = Elem[operand3, 2 * p + 1, esize];
    constant bits(esize) elt1_a = Elem[operand1, 2 * p + sel_a, esize];
    bits(esize) elt2_a   = Elem[operand2, 2 * s + sel_a, esize];
    bits(esize) elt2_b   = Elem[operand2, 2 * s + sel_b, esize];
    if neg_r then elt2_a = FPNeg(elt2_a, FPCR);
    if neg_i then elt2_b = FPNeg(elt2_b, FPCR);
    addend_r = FPMulAdd(addend_r, elt1_a, elt2_a, FPCR);
    addend_i = FPMulAdd(addend_i, elt1_a, elt2_b, FPCR);
    Elem[result, 2 * p + 0, esize] = addend_r;
    Elem[result, 2 * p + 1, esize] = addend_i;

Z[da, VL] = result;
```

### Variant: `Single-precision`
- **Assembly**: `FCMLA  <Zda>.S, <Zn>.S, <Zm>.S[<imm>], <const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  11   9   4  |
|-----------------------------------|
| 011 0010 0   11  1   i1  Zm  0001 rot Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fcmla_by_indexed_elem.sve_fp_fcmla_by_indexed_elem.fcmla_z_zzzi_s)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer index = UInt(i1);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer sel_a = UInt(rot<0>);
constant integer sel_b = UInt(NOT(rot<0>));
constant boolean neg_i = (rot<1> == '1');
constant boolean neg_r = (rot<0> != rot<1>);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "Half-precision" variant: is the name of the second source scalable vector register Z0-Z7, encoded in the "Zm" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "Single-precision" variant: is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `i2` | For the "Half-precision" variant: is the index of a Real and Imaginary pair, in the range 0 to 3, encoded in the "i2" field. |
| `<imm>` | `immediate` | `i1` | For the "Single-precision" variant: is the index of a Real and Imaginary pair, in the range 0 to 1, encoded in the "i1" field. |
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
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcmla_z_zzzi.xml`
</details>