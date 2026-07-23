## LASTB
_ARM A64 Instruction_

**Title**: LASTB (scalar) -- A64 | **Class**: `sve` | **XML ID**: `lastb_r_p_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Extract last element to general-purpose register

**Description**:
If there is an active element then extract the
 last active element
 from the final source vector register.
If there are no active elements, extract
the highest-numbered element.
Then zero-extend and place the extracted element
in the destination general-purpose register.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `LASTB  <R><d>, <Pg>, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  16 15  13 12   9   4  |
|-----------------------------------------|
| 000 0010 1   size 1   0   000 1   10  1   Pg  Zn  Rd  |
```

#### Decode (A64.sve.sve_perm_pred.sve_int_perm_last_r.lastb_r_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer rsize = if esize < 64 then 32 else 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Rd);
constant boolean isBefore = TRUE;
```

#### Execute (A64.sve.sve_perm_pred.sve_int_perm_last_r.lastb_r_p_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = Z[n, VL];
bits(rsize) result;
integer last = LastActiveElement(mask, esize);

if isBefore then
    if last < 0 then last = elements - 1;
else
    last = last + 1;
    if last >= elements then last = 0;
result = ZeroExtend(Elem[operand, last, esize], rsize);

X[d, rsize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<R>` | `unknown` | `size` | Is a width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number [0-30] of the destination general-purpose register or the name ZR (31), encoded in the "Rd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | W |
| 01 | W |
| 10 | W |
| 11 | X |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the general-purpose register written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `lastb_r_p_z.xml`
</details>