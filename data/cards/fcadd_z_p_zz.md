## FCADD
_ARM A64 Instruction_

**Title**: FCADD -- A64 | **Class**: `sve` | **XML ID**: `fcadd_z_p_zz`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point complex add with rotate (predicated)

**Description**:
Add the real and imaginary components of the active
floating-point complex numbers from the first source vector to
the complex numbers from the second source vector which have
first been rotated by 90 or 270 degrees in the direction from
the positive real axis towards the positive imaginary axis,
when considered in polar representation, equivalent to
multiplying the complex numbers in the second source vector by
±j beforehand. Destructively place the results
in the corresponding elements of the first source vector.
Inactive elements in the destination vector register remain unmodified.

Each complex number is represented in a vector register as an
even/odd pair of elements with the real part in the
even-numbered element and the imaginary part in the
odd-numbered element.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `FCADD  <Zdn>.<T>, <Pg>/M, <Zdn>.<T>, <Zm>.<T>, <const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  16 15  12   9   4  |
|--------------------------------|
| 011 0010 0   size 00000 rot 100 Pg  Zm  Zdn |
```

#### Decode (A64.sve.sve_fp_fcadd.sve_fp_fcadd.fcadd_z_p_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer dn = UInt(Zdn);
constant integer m = UInt(Zm);
constant boolean sub_i = (rot == '0');
constant boolean sub_r = (rot == '1');
```

#### Execute (A64.sve.sve_fp_fcadd.sve_fp_fcadd.fcadd_z_p_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer pairs = VL DIV (2 * esize);
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand1 = Z[dn, VL];
constant bits(VL) operand2 = if AnyActiveElement(mask, esize) then Z[m, VL] else Zeros(VL);
bits(VL) result;

for p = 0 to pairs-1
    bits(esize) acc_r = Elem[operand1, 2 * p + 0, esize];
    bits(esize) acc_i = Elem[operand1, 2 * p + 1, esize];
    if ActivePredicateElement(mask, 2 * p + 0, esize) then
        bits(esize) elt2_i = Elem[operand2, 2 * p + 1, esize];
        if sub_i then elt2_i = FPNeg(elt2_i, FPCR);
        acc_r = FPAdd(acc_r, elt2_i, FPCR);
    if ActivePredicateElement(mask, 2 * p + 1, esize) then
        bits(esize) elt2_r = Elem[operand2, 2 * p + 0, esize];
        if sub_r then elt2_r = FPNeg(elt2_r, FPCR);
        acc_i = FPAdd(acc_i, elt2_r, FPCR);
    Elem[result, 2 * p + 0, esize] = acc_r;
    Elem[result, 2 * p + 1, esize] = acc_i;

Z[dn, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the first source and destination scalable vector register, encoded in the "Zdn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<const>` | `unknown` | `rot` | Is the const specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

**<const> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #90 |
| 1 | #270 |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first source element size in the preferred disassembly of this instruction.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcadd_z_p_zz.xml`
</details>