## DECP
_ARM A64 Instruction_

**Title**: DECP (scalar) -- A64 | **Class**: `sve` | **XML ID**: `decp_r_p_r`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Decrement scalar by count of true predicate elements

**Description**:
Counts the number of true elements in the source predicate and
then uses the result to decrement the
  scalar destination.

### Variant: `SVE`
- **Assembly**: `DECP  <Xdn>, <Pm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17 16 15  11 10   8   4  |
|-----------------------------------------|
| 001 0010 1   size 101 1   0   1   1000 1   00  Pm  Rdn |
```

#### Decode (A64.sve.sve_pred_count_b.sve_int_count_r.decp_r_p_r_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer m = UInt(Pm);
constant integer dn = UInt(Rdn);
```

#### Execute (A64.sve.sve_pred_count_b.sve_int_count_r.decp_r_p_r_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(64) operand1 = X[dn, 64];
constant bits(PL) operand2 = P[m, PL];
integer count = 0;

for e = 0 to elements-1
    if ActivePredicateElement(operand2, e, esize) then
        count = count + 1;

X[dn, 64] = operand1 - count;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xdn>` | `register (64-bit)` | `Rdn` | Is the 64-bit name of the source and destination general-purpose register, encoded in the "Rdn" field. |
| `<Pm>` | `unknown` | `Pm` | Is the name of the source scalable predicate register, encoded in the "Pm" field. |
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
- source: `decp_r_p_r.xml`
</details>