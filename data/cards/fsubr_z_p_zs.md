## FSUBR
_ARM A64 Instruction_

**Title**: FSUBR (immediate) -- A64 | **Class**: `sve` | **XML ID**: `fsubr_z_p_zs`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point reversed subtract from immediate (predicated)

**Description**:
Reversed subtract from an immediate each active floating-point element of the source vector,
and destructively place the results in the corresponding elements of the  source vector.
The immediate may take the value +0.5 or +1.0 only.
Inactive elements in the destination vector register remain unmodified.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `FSUBR  <Zdn>.<T>, <Pg>/M, <Zdn>.<T>, <const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  12   9   5  4  |
|--------------------------------------|
| 011 0010 1   size 0   11  011 100 Pg  0000 i1  Zdn |
```

#### Decode (A64.sve.sve_fp_pred.sve_fp_2op_i_p_zds.fsubr_z_p_zs_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer dn = UInt(Zdn);
constant bits(esize) imm = if i1 == '0' then FPPointFive('0', esize) else FPOne('0', esize);
```

#### Execute (A64.sve.sve_fp_pred.sve_fp_2op_i_p_zds.fsubr_z_p_zs_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand1 = Z[dn, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize) element1 = Elem[operand1, e, esize];
    if ActivePredicateElement(mask, e, esize) then
        Elem[result, e, esize] = FPSub(imm, element1, FPCR);
    else
        Elem[result, e, esize] = element1;

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
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the source and destination scalable vector register, encoded in the "Zdn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<const>` | `unknown` | `i1` | Is the floating-point immediate value, |

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
| 0 | #0.5 |
| 1 | #1.0 |

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
- source: `fsubr_z_p_zs.xml`
</details>