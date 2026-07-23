## FRINT32X
_ARM A64 Instruction_

**Title**: FRINT32X -- A64 | **Class**: `sve2` | **XML ID**: `frint32x_z_p_z`

**Architecture**: `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2)

**Summary**: Floating-point round to 32-bit integer, using current rounding mode (predicated)

**Description**:
Round to integral floating-point values that fit into a 32-bit
integer size using the rounding mode that is determined by the FPCR from each active floating-point element of the source vector,
and place the results in the corresponding elements of the destination vector.

Inactive elements in the destination vector register remain unmodified or
are set to zero, depending on whether merging or zeroing
predication is selected.

**Attributes**: Predicated

### Variant: `Merging`
- **Assembly**: `FRINT32X  <Zd>.<T>, <Pg>/M, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18 17 16 15  12   9   4  |
|-----------------------------------------|
| 011 0010 1   00  0   10  0   sz  1   101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unary.sve_fp_2op_p_zd_c.frint32x_z_p_z_m)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32 << UInt(sz);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer intsize = 32;
constant FPRounding rounding = FPRoundingMode(FPCR);
constant boolean merging = TRUE;
```

#### Execute (A64.sve.sve_fp_unary.sve_fp_2op_p_zd_c.frint32x_z_p_z_m)

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
        constant bits(esize) element = Elem[operand, e, esize];
        Elem[result, e, esize] = FPRoundIntN(element, FPCR, rounding, intsize);

Z[d, VL] = result;
```

### Variant: `Zeroing`
- **Assembly**: `FRINT32X  <Zd>.<T>, <Pg>/Z, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  16 15 14 13 12   9   4  |
|-----------------------------------------|
| 011 0010 0   00  011 10  0   1   sz  1   Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_zeroing_unary.sve_fp_z2op_p_zd_c.frint32x_z_p_z_z)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32 << UInt(sz);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer intsize = 32;
constant FPRounding rounding = FPRoundingMode(FPCR);
constant boolean merging = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `sz` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p2) \|\| IsFeatureImplemented(FEAT_SME2p2)` |

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
- source: `frint32x_z_p_z.xml`
</details>