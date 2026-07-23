## SQNEG
_ARM A64 Instruction_

**Title**: SQNEG -- A64 | **Class**: `sve2` | **XML ID**: `sqneg_z_p_z`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME), `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2)

**Summary**: Signed saturating negate

**Description**:
Negate the signed integer value in each active element of the source
vector, and place the results in the corresponding elements of the
destination vector. Each result element is saturated to the
 N-bit element's
signed integer range -2(N-1)  to (2(N-1))-1. 
Inactive elements in the destination vector register remain unmodified or
are set to zero, depending on whether merging or zeroing
predication is selected.

**Attributes**: Predicated

### Variant: `Merging`
- **Assembly**: `SQNEG  <Zd>.<T>, <Pg>/M, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19 18 17 16 15  13 12   9   4  |
|-----------------------------------------------|
| 010 0010 0   size 0   0   1   0   0   1   10  1   Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_predicated.sve_intx_pred_arith_unary.sqneg_z_p_z_m)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = TRUE;
```

#### Execute (A64.sve.sve_intx_predicated.sve_intx_pred_arith_unary.sqneg_z_p_z_m)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(VL) result = if merging then Z[d, VL] else Zeros(VL);

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        integer element = SInt(Elem[operand, e, esize]);
        element = -element;
        Elem[result, e, esize] = SignedSat(element, esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Variant: `Zeroing`
- **Assembly**: `SQNEG  <Zd>.<T>, <Pg>/Z, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19 18 17 16 15  13 12   9   4  |
|-----------------------------------------------|
| 010 0010 0   size 0   0   1   0   1   1   10  1   Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_predicated.sve_intx_pred_arith_unary.sqneg_z_p_z_z)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = FALSE;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p2) \|\| IsFeatureImplemented(FEAT_SME2p2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

The merging variant of this instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and the merging variant of this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as the merging variant this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first source element size in the preferred disassembly of the merging variant of this instruction.
          
          
            The MOVPRFX must specify the same destination register as the merging variant of this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of the merging variant of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqneg_z_p_z.xml`
</details>