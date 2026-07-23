## CNTP
_ARM A64 Instruction_

**Title**: CNTP (predicate) -- A64 | **Class**: `sve` | **XML ID**: `cntp_r_p_p`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Set scalar to count of true predicate elements

**Description**:
Counts the number of active and true elements in the source predicate
and places the scalar result in the destination general-purpose register.
Inactive predicate elements are not counted.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `CNTP  <Xd>, <Pg>, <Pn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15  13   9  8   4  |
|-----------------------------------|
| 001 0010 1   size 100 000 10  Pg  0   Pn  Rd  |
```

#### Decode (A64.sve.sve_pred_count_a.sve_int_pcount_pred.cntp_r_p_p_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Pn);
constant integer d = UInt(Rd);
```

#### Execute (A64.sve.sve_pred_count_a.sve_int_pcount_pred.cntp_r_p_p_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(PL) operand = P[n, PL];
bits(64) sum = Zeros(64);

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) && ActivePredicateElement(operand, e, esize) then
        sum = sum + 1;
X[d, 64] = sum;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register, encoded in the "Rd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register, encoded in the "Pg" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the source scalable predicate register, encoded in the "Pn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |

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
- source: `cntp_r_p_p.xml`
</details>