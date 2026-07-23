## PNEXT
_ARM A64 Instruction_

**Title**: PNEXT -- A64 | **Class**: `sve` | **XML ID**: `pnext_p_p_p`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Find next active predicate

**Description**:
An instruction used to construct a loop which iterates over all
true elements in the vector select predicate register. If all
elements in the first source predicate register are false it
determines the first true element in the vector select predicate
register, otherwise it determines the next true element in the
vector select predicate register that follows the last true
element in the first source predicate register. All elements of
the destination predicate register are set to false, except the
element corresponding to the determined vector select element, if
any, which is set to true. Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

### Variant: `SVE`
- **Assembly**: `PNEXT  <Pdn>.<T>, <Pv>, <Pdn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  19  15  13  10   8   4  3  |
|--------------------------------------|
| 001 0010 1   size 01  1001 11  000 10  Pv  0   Pdn |
```

#### Decode (A64.sve.sve_pred_gen_d.sve_int_pnext.pnext_p_p_p_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer v = UInt(Pv);
constant integer dn = UInt(Pdn);
```

#### Execute (A64.sve.sve_pred_gen_d.sve_int_pnext.pnext_p_p_p_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[v, PL];
constant bits(PL) operand = P[dn, PL];
bits(PL) result;
constant integer psize = esize DIV 8;

integer next = LastActiveElement(operand, esize) + 1;

while next < elements && (!ActivePredicateElement(mask, next, esize)) do
    next = next + 1;

result = Zeros(PL);
if next < elements then
    Elem[result, next, psize] = ZeroExtend('1', psize);

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
| `<Pdn>` | `unknown` | `Pdn` | Is the name of the first source and destination scalable predicate register, encoded in the "Pdn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pv>` | `unknown` | `Pv` | Is the name of the vector select predicate register, encoded in the "Pv" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the NZCV condition flags written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `pnext_p_p_p.xml`
</details>