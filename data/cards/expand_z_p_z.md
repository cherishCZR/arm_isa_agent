## EXPAND
_ARM A64 Instruction_

**Title**: EXPAND -- A64 | **Class**: `sve2` | **XML ID**: `expand_z_p_z`

**Architecture**: `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2)

**Summary**: Copy lower-numbered vector elements to active elements

**Description**:
In order of increasing element number, unpack consecutive elements
from the source vector into increasing active elements of the destination vector,
setting any inactive elements to zero.

This instruction is illegal when executed in
Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled,
or FEAT_SME2p2 is implemented.

**Attributes**: Predicated; SM Policy: `SM_0_or_SME2p2`

### Variant: `SVE2`
- **Assembly**: `EXPAND  <Zd>.<T>, <Pg>, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  16 15  13 12   9   4  |
|-----------------------------------------|
| 000 0010 1   size 1   1   000 1   10  0   Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_pred.sve_int_perm_expand.expand_z_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_perm_pred.sve_int_perm_expand.expand_z_p_z_)

```
if IsFeatureImplemented(FEAT_SME2p2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand1 = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(VL) result;
integer x = 0;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        Elem[result, e, esize] = Elem[operand1, x, esize];
        x = x + 1;
    else
        Elem[result, e, esize] = Zeros(esize);

Z[d, VL] = result;
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

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `expand_z_p_z.xml`
</details>