## CMLA
_ARM A64 Instruction_

**Title**: CMLA (vectors) -- A64 | **Class**: `sve2` | **XML ID**: `cmla_z_zzz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Complex integer multiply-add with rotate

**Description**:
Multiply  the
duplicated real components for rotations 0 and
180, or imaginary components for rotations 90 and
270, of the integral numbers in  the first source vector by the corresponding complex number in the
second source vector  rotated
by 0, 90, 180 or 270 degrees in the direction from the
positive real axis towards the positive imaginary axis,
when considered in polar representation.

Then  add the products to
the corresponding components of the complex numbers in
the addend vector.  Destructively place  the
results in the corresponding elements of the addend
vector.   This instruction is unpredicated.

These transformations permit the creation of a variety
of multiply-add and multiply-subtract operations on
complex numbers by combining two of these instructions
with the same vector operands but with rotations that
are 90 degrees apart.

Each complex number is represented in a vector register as an
even/odd pair of elements with the real part in the
even-numbered element and the imaginary part in the
odd-numbered element.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `CMLA  <Zda>.<T>, <Zn>.<T>, <Zm>.<T>, <const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14  12 11   9   4  |
|--------------------------------------|
| 010 0010 0   size 0   Zm  0   01  0   rot Zn  Zda |
```

#### Decode (A64.sve.sve_intx_muladd_unpred.sve_intx_cmla.cmla_z_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer sel_a = UInt(rot<0>);
constant integer sel_b = UInt(NOT(rot<0>));
constant boolean sub_r = (rot<0> != rot<1>);
constant boolean sub_i = (rot<1> == '1');
```

#### Execute (A64.sve.sve_intx_muladd_unpred.sve_intx_cmla.cmla_z_zzz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer pairs = VL DIV (2 * esize);
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

for p = 0 to pairs-1
    constant integer elt1_a = SInt(Elem[operand1, 2 * p + sel_a, esize]);
    constant integer elt2_a = SInt(Elem[operand2, 2 * p + sel_a, esize]);
    constant integer elt2_b = SInt(Elem[operand2, 2 * p + sel_b, esize]);
    constant bits(esize) elt3_r = Elem[operand3, 2 * p + 0, esize];
    constant bits(esize) elt3_i = Elem[operand3, 2 * p + 1, esize];
    constant integer product_r =  elt1_a * elt2_a;
    constant integer product_i =  elt1_a * elt2_b;
    if sub_r then
        Elem[result, 2 * p + 0, esize] = elt3_r - product_r;
    else
        Elem[result, 2 * p + 0, esize] = elt3_r + product_r;
    if sub_i then
        Elem[result, 2 * p + 1, esize] = elt3_i - product_i;
    else
        Elem[result, 2 * p + 1, esize] = elt3_i + product_i;

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<const>` | `unknown` | `rot` | Is the const specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<const> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | #0 |
| 01 | #90 |
| 10 | #180 |
| 11 | #270 |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `cmla_z_zzz.xml`
</details>