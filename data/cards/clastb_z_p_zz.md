## CLASTB
_ARM A64 Instruction_

**Title**: CLASTB (vectors) -- A64 | **Class**: `sve` | **XML ID**: `clastb_z_p_zz`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Conditionally extract last element to vector register

**Description**:
From the second source vector register extract the
   last active element, and then replicate that element to
   destructively fill the destination and first source
   vector.

If there are no active elements then leave the
   destination and source vector unmodified.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `CLASTB  <Zdn>.<T>, <Pg>, <Zdn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  16 15  13 12   9   4  |
|-----------------------------------------|
| 000 0010 1   size 1   0   100 1   10  0   Pg  Zm  Zdn |
```

#### Decode (A64.sve.sve_perm_pred.sve_int_perm_clast_zz.clastb_z_p_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer dn = UInt(Zdn);
constant integer m = UInt(Zm);
constant boolean isBefore = TRUE;
```

#### Execute (A64.sve.sve_perm_pred.sve_int_perm_clast_zz.clastb_z_p_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand1 = Z[dn, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;
integer last = LastActiveElement(mask, esize);

if last < 0 then
    result = operand1;
else
    if !isBefore then
        last = last + 1;
        if last >= elements then last = 0;
    for e = 0 to elements-1
        Elem[result, e, esize] = Elem[operand2, last, esize];

Z[dn, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the first source and destination scalable vector register, encoded in the "Zdn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `clastb_z_p_zz.xml`
</details>