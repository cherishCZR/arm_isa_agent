## LASTA
_ARM A64 Instruction_

**Title**: LASTA (SIMD&FP scalar) -- A64 | **Class**: `sve` | **XML ID**: `lasta_v_p_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Extract element after last to SIMD&FP scalar register

**Description**:
If there is an active element then extract the
element after the last active element
modulo the number of elements from the final source vector register.
If there are no active elements, extract
element zero.
Then  place the extracted element
in the destination SIMD&FP scalar register.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `LASTA  <V><d>, <Pg>, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  16 15  13 12   9   4  |
|-----------------------------------------|
| 000 0010 1   size 1   0   001 0   10  0   Pg  Zn  Vd  |
```

#### Decode (A64.sve.sve_perm_pred.sve_int_perm_last_v.lasta_v_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Vd);
constant boolean isBefore = FALSE;
```

#### Execute (A64.sve.sve_perm_pred.sve_int_perm_last_v.lasta_v_p_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = Z[n, VL];
integer last = LastActiveElement(mask, esize);

if isBefore then
    if last < 0 then last = elements - 1;
else
    last = last + 1;
    if last >= elements then last = 0;
V[d, esize] = Elem[operand, last, esize];
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `size` | Is a width specifier, |
| `<d>` | `unknown` | `Vd` | Is the number [0-31] of the destination SIMD&FP register, encoded in the "Vd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

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
- source: `lasta_v_p_z.xml`
</details>