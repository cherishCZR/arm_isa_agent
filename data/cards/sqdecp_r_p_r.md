## SQDECP
_ARM A64 Instruction_

**Title**: SQDECP (scalar) -- A64 | **Class**: `sve` | **XML ID**: `sqdecp_r_p_r`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Signed saturating decrement scalar by count of true predicate elements

**Description**:
Counts the number of true elements in the source predicate and
then uses the result to decrement the
  scalar destination.
The
  result is
  saturated to the
     source general-purpose register's
  signed integer range.
  A 32-bit saturated result is then sign-extended to 64 bits.

### Variant: `32-bit`
- **Assembly**: `SQDECP  <Xdn>, <Pm>.<T>, <Wdn>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17 16 15  11 10  9  8   4  |
|--------------------------------------------|
| 001 0010 1   size 101 0   1   0   1000 1   0   0   Pm  Rdn |
```

#### Decode (A64.sve.sve_pred_count_b.sve_int_count_r_sat.sqdecp_r_p_r_sx)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer m = UInt(Pm);
constant integer dn = UInt(Rdn);
constant boolean unsigned = FALSE;
constant integer ssize = 32;
```

#### Execute (A64.sve.sve_pred_count_b.sve_int_count_r_sat.sqdecp_r_p_r_sx)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(ssize) operand1 = X[dn, ssize];
constant bits(PL) operand2 = P[m, PL];
bits(ssize) result;
integer count = 0;

for e = 0 to elements-1
    if ActivePredicateElement(operand2, e, esize) then
        count = count + 1;

constant integer element = Int(operand1, unsigned);
(result, -) = SatQ(element - count, ssize, unsigned);
X[dn, 64] = Extend(result, 64, unsigned);
```

### Variant: `64-bit`
- **Assembly**: `SQDECP  <Xdn>, <Pm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17 16 15  11 10  9  8   4  |
|--------------------------------------------|
| 001 0010 1   size 101 0   1   0   1000 1   1   0   Pm  Rdn |
```

#### Decode (A64.sve.sve_pred_count_b.sve_int_count_r_sat.sqdecp_r_p_r_x)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer m = UInt(Pm);
constant integer dn = UInt(Rdn);
constant boolean unsigned = FALSE;
constant integer ssize = 64;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xdn>` | `register (64-bit)` | `Rdn` | Is the 64-bit name of the source and destination general-purpose register, encoded in the "Rdn" field. |
| `<Pm>` | `unknown` | `Pm` | Is the name of the source scalable predicate register, encoded in the "Pm" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Wdn>` | `register (32-bit)` | `Rdn` | Is the 32-bit name of the source and destination general-purpose register, encoded in the "Rdn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operational Notes

If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the general-purpose register written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqdecp_r_p_r.xml`
</details>