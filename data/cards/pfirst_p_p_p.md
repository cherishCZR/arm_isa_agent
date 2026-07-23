## PFIRST
_ARM A64 Instruction_

**Title**: PFIRST -- A64 | **Class**: `sve` | **XML ID**: `pfirst_p_p_p`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Set the first active predicate element to true

**Description**:
Sets the first active element in the destination predicate
to true, otherwise elements from the source
predicate are passed through unchanged.
Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `PFIRST  <Pdn>.B, <Pg>, <Pdn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21  19  15  13  10   8   4  3  |
|-----------------------------------------|
| 001 0010 1   0   1   01  1000 11  000 00  Pg  0   Pdn |
```

#### Decode (A64.sve.sve_pred_gen_d.sve_int_pfirst.pfirst_p_p_p_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8;
constant integer g = UInt(Pg);
constant integer dn = UInt(Pdn);
```

#### Execute (A64.sve.sve_pred_gen_d.sve_int_pfirst.pfirst_p_p_p_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
bits(PL) result = P[dn, PL];
integer first = -1;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) && first == -1 then
        first = e;

if first >= 0 then
    Elem[result, first, psize] = ZeroExtend('1', psize);

PSTATE.<N,Z,C,V> = PredTest(mask, result, esize);
P[dn, PL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pdn>` | `unknown` | `Pdn` | Is the name of the source and destination scalable predicate register, encoded in the "Pdn" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register, encoded in the "Pg" field. |

### Operational Notes

If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the NZCV condition flags written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `pfirst_p_p_p.xml`
</details>