## WHILELE
_ARM A64 Instruction_

**Title**: WHILELE (predicate pair) -- A64 | **Class**: `sve2` | **XML ID**: `whilele_pp_rr`

**Architecture**: `FEAT_SME2 || FEAT_SVE2p1` (FEAT_SME2 || FEAT_SVE2p1)

**Summary**: While incrementing signed scalar less than or equal to scalar (pair of predicates)

**Description**:
Generate a pair of predicates that starting from the lowest numbered element of the pair
is true while the incrementing value of the first, signed
 scalar operand is less than or equal to the second scalar operand and
false thereafter up to the highest numbered element of the pair.

If the second scalar operand is equal to the
maximum signed
 integer value then a condition which includes
an equality test can never fail and the result will be
an all-true predicate.

The full  width of the scalar operands is significant
for the purposes of comparison, and the full width 
first operand is incremented by one for each destination
predicate element, irrespective of the predicate result
element size. The first general-purpose source register is not
itself updated.

The lower-numbered elements are placed in the first predicate
destination register, and the higher-numbered elements in the
second predicate destination register. Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

### Variant: `SVE2`
- **Assembly**: `WHILELE  { <Pd1>.<T>, <Pd2>.<T> }, <Xn>, <Xm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  13  11 10  9   4  3   0 |
|--------------------------------------------|
| 001 0010 1   size 1   Rm  01  01  0   1   Rn  1   Pd  1   |
```

#### Decode (A64.sve.sve_while_pn.sve_int_while_rr_pair.whilele_pp_rr_)

```
if !IsFeatureImplemented(FEAT_SME2) && !IsFeatureImplemented(FEAT_SVE2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer rsize = 64;
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer d0 = UInt(Pd:'0');
constant integer d1 = UInt(Pd:'1');
constant boolean unsigned = FALSE;
constant CmpOp op = Cmp_LE;
```

#### Execute (A64.sve.sve_while_pn.sve_int_while_rr_pair.whilele_pp_rr_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL*2) mask = Ones(PL*2);
bits(rsize) operand1 = X[n, rsize];
constant bits(rsize) operand2 = X[m, rsize];
bits(PL*2) result;
boolean last = TRUE;
constant integer psize = esize DIV 8;

for e = 0 to (elements*2)-1
    boolean cond;
    case op of
        when Cmp_LT cond = (Int(operand1, unsigned) <  Int(operand2, unsigned));
        when Cmp_LE cond = (Int(operand1, unsigned) <= Int(operand2, unsigned));

    last = last && cond;
    constant bit pbit = if last then '1' else '0';
    Elem[result, e, psize] = ZeroExtend(pbit, psize);
    operand1 = operand1 + 1;

PSTATE.<N,Z,C,V> = PredTest(mask, result, esize);
P[d0, PL] = result<PL-1:0>;
P[d1, PL] = result<PL*2-1:PL>;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) \|\| IsFeatureImplemented(FEAT_SVE2p1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd1>` | `unknown` | `Pd` | Is the name of the first destination scalable predicate register, encoded as "Pd" times 2. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pd2>` | `unknown` | `Pd` | Is the name of the second destination scalable predicate register, encoded as "Pd" times 2 plus 1. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first source general-purpose register, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second source general-purpose register, encoded in the "Rm" field. |

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
- sve-elem-type: `8-64-elem`
- source: `whilele_pp_rr.xml`
</details>