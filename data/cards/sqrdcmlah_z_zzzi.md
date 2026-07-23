## SQRDCMLAH
_ARM A64 Instruction_

**Title**: SQRDCMLAH (indexed) -- A64 | **Class**: `sve2` | **XML ID**: `sqrdcmlah_z_zzzi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Saturating rounding doubling complex integer multiply-add high with rotate (indexed)

**Description**:
Multiply without saturation the
duplicated real components for rotations 0 and
180, or imaginary components for rotations 90 and
270, of the integral numbers in each
128-bit segment of the first source vector by the specified complex number in the
corresponding the
second source vector segment rotated
by 0, 90, 180 or 270 degrees in the direction from the
positive real axis towards the positive imaginary axis,
when considered in polar representation.

Then double and add the products to
the corresponding components of the complex numbers in
the addend vector.  Destructively place the most significant rounded half of the
results in the corresponding elements of the addend
vector.  Each result element is saturated to the
 N-bit element's
signed integer range -2(N-1)  to (2(N-1))-1. This instruction is unpredicated.

These transformations permit the creation of a variety
of multiply-add and multiply-subtract operations on
complex numbers by combining two of these instructions
with the same vector operands but with rotations that
are 90 degrees apart.

Each complex number is represented in a vector register as an
even/odd pair of elements with the real part in the
even-numbered element and the imaginary part in the
odd-numbered element.

### Variant: `16-bit`
- **Assembly**: `SQRDCMLAH  <Zda>.H, <Zn>.H, <Zm>.H[<imm>], <const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  11   9   4  |
|-----------------------------------|
| 010 0010 0   10  1   i2  Zm  0111 rot Zn  Zda |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_qrdcmla_by_indexed_elem.sqrdcmlah_z_zzzi_h)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer index = UInt(i2);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer sel_a = UInt(rot<0>);
constant integer sel_b = UInt(NOT(rot<0>));
constant boolean sub_r = (rot<0> != rot<1>);
constant boolean sub_i = (rot<1> == '1');
```

#### Execute (A64.sve.sve_intx_by_indexed_elem.sve_intx_qrdcmla_by_indexed_elem.sqrdcmlah_z_zzzi_h)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer pairs = VL DIV (2 * esize);
constant integer pairspersegment = 128 DIV (2 * esize);
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

integer res_r, res_i;
for p = 0 to pairs-1
    constant integer segmentbase = p - (p MOD pairspersegment);
    constant integer s = segmentbase + index;
    constant integer elt1_a = SInt(Elem[operand1, 2 * p + sel_a, esize]);
    constant integer elt2_a = SInt(Elem[operand2, 2 * s + sel_a, esize]);
    constant integer elt2_b = SInt(Elem[operand2, 2 * s + sel_b, esize]);
    constant bits(esize) elt3_r = Elem[operand3, 2 * p + 0, esize];
    constant bits(esize) elt3_i = Elem[operand3, 2 * p + 1, esize];
    constant integer product_r =  elt1_a * elt2_a;
    constant integer product_i =  elt1_a * elt2_b;
    if sub_r then
        res_r = (SInt(elt3_r) << esize) - 2 * product_r;
    else
        res_r = (SInt(elt3_r) << esize) + 2 * product_r;
    res_r = (res_r + (1 << (esize-1))) >> esize;
    Elem[result, 2 * p + 0, esize] = SignedSat(res_r, esize);
    if sub_i then
        res_i = (SInt(elt3_i) << esize) - 2 * product_i;
    else
        res_i = (SInt(elt3_i) << esize) + 2 * product_i;
    res_i = (res_i + (1 << (esize-1))) >> esize;
    Elem[result, 2 * p + 1, esize] = SignedSat(res_i, esize);

Z[da, VL] = result;
```

### Variant: `32-bit`
- **Assembly**: `SQRDCMLAH  <Zda>.S, <Zn>.S, <Zm>.S[<imm>], <const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  11   9   4  |
|-----------------------------------|
| 010 0010 0   11  1   i1  Zm  0111 rot Zn  Zda |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_qrdcmla_by_indexed_elem.sqrdcmlah_z_zzzi_s)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer index = UInt(i1);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer sel_a = UInt(rot<0>);
constant integer sel_b = UInt(NOT(rot<0>));
constant boolean sub_r = (rot<0> != rot<1>);
constant boolean sub_i = (rot<1> == '1');
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "16-bit" variant: is the name of the second source scalable vector register Z0-Z7, encoded in the "Zm" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "32-bit" variant: is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `i2` | For the "16-bit" variant: is the element index, in the range 0 to 3, encoded in the "i2" field. |
| `<imm>` | `immediate` | `i1` | For the "32-bit" variant: is the element index, in the range 0 to 1, encoded in the "i1" field. |
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
- source: `sqrdcmlah_z_zzzi.xml`
</details>