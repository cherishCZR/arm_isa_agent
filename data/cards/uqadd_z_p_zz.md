## UQADD
_ARM A64 Instruction_

**Title**: UQADD (vectors, predicated) -- A64 | **Class**: `sve2` | **XML ID**: `uqadd_z_p_zz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Unsigned saturating addition (predicated)

**Description**:
Add active unsigned elements of the first source vector to corresponding
unsigned elements of the second source vector and destructively place
the results in the corresponding elements of the first source vector.
Each result element is saturated to the
 N-bit element's
unsigned integer range 0 to (2N)-1. Inactive elements in the destination vector register remain unmodified.

**Attributes**: Predicated

### Variant: `SVE2`
- **Assembly**: `UQADD  <Zdn>.<T>, <Pg>/M, <Zdn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18 17 16 15  13 12   9   4  |
|--------------------------------------------|
| 010 0010 0   size 0   11  0   0   1   10  0   Pg  Zm  Zdn |
```

#### Decode (A64.sve.sve_intx_predicated.sve_intx_pred_arith_binary_sat.uqadd_z_p_zz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer dn = UInt(Zdn);
constant integer m = UInt(Zm);
```

#### Execute (A64.sve.sve_intx_predicated.sve_intx_pred_arith_binary_sat.uqadd_z_p_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand1 = Z[dn, VL];
constant bits(VL) operand2 = if AnyActiveElement(mask, esize) then Z[m, VL] else Zeros(VL);
bits(VL) result;

for e = 0 to elements-1
    constant integer element1 = UInt(Elem[operand1, e, esize]);
    constant integer element2 = UInt(Elem[operand2, e, esize]);
    if ActivePredicateElement(mask, e, esize) then
        Elem[result, e, esize] = UnsignedSat(element1 + element2, esize);
    else
        Elem[result, e, esize] = Elem[operand1, e, esize];

Z[dn, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

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
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first source element size in the preferred disassembly of this instruction.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `uqadd_z_p_zz.xml`
</details>