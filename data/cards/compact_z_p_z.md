## COMPACT
_ARM A64 Instruction_

**Title**: COMPACT -- A64 | **Class**: `sve` | **XML ID**: `compact_z_p_z`

**Architecture**: `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2), `FEAT_SVE || FEAT_SME2p2` (FEAT_SVE || FEAT_SME2p2)

**Summary**: Copy active vector elements to lower-numbered elements

**Description**:
In order of increasing element number, pack active elements
from the source vector into increasing consecutive elements of the destination vector,
setting any remaining elements to zero.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is
implemented and enabled, or FEAT_SME2p2 is implemented.

**Attributes**: Predicated; SM Policy: `SM_0_or_SME2p2`

### Variant: `Byte and halfword`
- **Assembly**: `COMPACT  <Zd>.<T>, <Pg>, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20 19  16 15  13 12   9   4  |
|--------------------------------------------|
| 000 0010 1   0   sz  1   0   000 1   10  0   Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_pred.sve_int_perm_compact.compact_z_p_z_s)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(sz);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_perm_pred.sve_int_perm_compact.compact_z_p_z_s)

```
if IsFeatureImplemented(FEAT_SME2p2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand1 = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(VL) result = Zeros(VL);
integer x = 0;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant bits(esize) element = Elem[operand1, e, esize];
        Elem[result, x, esize] = element;
        x = x + 1;

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p2) \|\| IsFeatureImplemented(FEAT_SME2p2)` |

### Variant: `Word and doubleword`
- **Assembly**: `COMPACT  <Zd>.<T>, <Pg>, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20 19  16 15  13 12   9   4  |
|--------------------------------------------|
| 000 0010 1   1   sz  1   0   000 1   10  0   Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_pred.sve_int_perm_compact.compact_z_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32 << UInt(sz);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME2p2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `sz` | For the "Byte and halfword" variant: is the size specifier, |
| `<T>` | `unknown` | `sz` | For the "Word and doubleword" variant: is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | B |
| 1 | H |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `compact_z_p_z.xml`
</details>