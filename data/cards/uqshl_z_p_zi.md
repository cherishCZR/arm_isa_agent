## UQSHL
_ARM A64 Instruction_

**Title**: UQSHL (immediate) -- A64 | **Class**: `sve2` | **XML ID**: `uqshl_z_p_zi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Unsigned saturating shift left by immediate

**Description**:
Shift left by immediate each active unsigned element of the source
vector, and destructively place the results in the corresponding
elements of the source vector. Each result element is saturated to the
 N-bit element's
unsigned integer range 0 to (2N)-1. The immediate shift amount is an unsigned value in the range 0
to number of bits per element minus 1. Inactive elements in the destination vector register remain unmodified.

**Attributes**: Predicated

### Variant: `SVE2`
- **Assembly**: `UQSHL  <Zdn>.<T>, <Pg>/M, <Zdn>.<T>, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  17 16 15  12   9   7   4  |
|--------------------------------------------|
| 000 0010 0   tszh 0   0   01  1   1   100 Pg  tszl imm3 Zdn |
```

#### Decode (A64.sve.sve_int_pred_shift.sve_int_bin_pred_shift_0.uqshl_z_p_zi_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant bits(4) tsize = tszh:tszl;
if tsize == '0000' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << HighestSetBit(tsize);
constant integer g = UInt(Pg);
constant integer dn = UInt(Zdn);
constant integer shift = UInt(tsize:imm3) - esize;
```

#### Execute (A64.sve.sve_int_pred_shift.sve_int_bin_pred_shift_0.uqshl_z_p_zi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[dn, VL];
constant bits(PL) mask = P[g, PL];
bits(VL) result;

for e = 0 to elements-1
    constant integer element1 = UInt(Elem[operand1, e, esize]);
    if ActivePredicateElement(mask, e, esize) then
        constant integer res = element1 << shift;
        Elem[result, e, esize] = UnsignedSat(res, esize);
    else
        Elem[result, e, esize] = Elem[operand1, e, esize];

Z[dn, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `tszh:tszl != '0000'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the source and destination scalable vector register, encoded in the "Zdn" field. |
| `<T>` | `arrangement` | `tszh:tszl` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<const>` | `unknown` | `tszh:tszl:imm3` | Is the immediate shift amount, in the range 0 to number of bits per element minus 1, encoded in "tszh:tszl:imm3". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | B |
| 1x | H |
| xx | S |
| xx | D |

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
- source: `uqshl_z_p_zi.xml`
</details>