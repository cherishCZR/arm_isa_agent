## WHILELO
_ARM A64 Instruction_

**Title**: WHILELO (predicate as counter) -- A64 | **Class**: `sve2` | **XML ID**: `whilelo_pn_rr`

**Architecture**: `FEAT_SME2 || FEAT_SVE2p1` (FEAT_SME2 || FEAT_SVE2p1)

**Summary**: While incrementing unsigned scalar lower than scalar (predicate-as-counter)

**Description**:
Generate a predicate for a group of two or four vectors that starting
from the lowest
numbered element of the group is true while the incrementing value
of the first, unsigned  scalar operand is lower than the second scalar
operand and false thereafter up to the highest numbered element of the group.

The full  width of the scalar operands is significant
for the purposes of comparison, and the full width 
first operand is incremented by one for each destination
predicate element, irrespective of the predicate result
element size.

The predicate result is placed in the predicate
destination register using the predicate-as-counter encoding.
Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

**Attributes**: SM Policy: `SM_1_or_SVE2p1`

### Variant: `SVE2`
- **Assembly**: `WHILELO  <PNd>.<T>, <Xn>, <Xm>, <vl>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  13 12 11 10  9   4  3  2  |
|-----------------------------------------------|
| 001 0010 1   size 1   Rm  01  vl  0   1   1   Rn  1   0   PNd |
```

#### Decode (A64.sve.sve_while_pn.sve_int_while_rr_pn.whilelo_pn_rr_)

```
if !IsFeatureImplemented(FEAT_SME2) && !IsFeatureImplemented(FEAT_SVE2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer rsize = 64;
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer d = UInt('1':PNd);
constant boolean unsigned = TRUE;
constant boolean invert = FALSE;
constant CmpOp op = Cmp_LT;
constant integer width = 2 << UInt(vl);
```

#### Execute (A64.sve.sve_while_pn.sve_int_while_rr_pn.whilelo_pn_rr_)

```
if IsFeatureImplemented(FEAT_SVE2p1) then CheckSVEEnabled(); else CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = width * (VL DIV esize);
bits(rsize) operand1 = X[n, rsize];
constant bits(rsize) operand2 = X[m, rsize];
bits(PL) result;
boolean last = TRUE;
integer count = 0;

for e = 0 to elements-1
    boolean cond;
    case op of
        when Cmp_LT cond = (Int(operand1, unsigned) <  Int(operand2, unsigned));
        when Cmp_LE cond = (Int(operand1, unsigned) <= Int(operand2, unsigned));

    last = last && cond;
    if last then count = count + 1;
    operand1 = operand1 + 1;

result = EncodePredCount(esize, elements, count, invert, PL);
PSTATE.<N,Z,C,V> = PredCountTest(elements, count, invert);
P[d, PL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) \|\| IsFeatureImplemented(FEAT_SVE2p1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<PNd>` | `unknown` | `PNd` | Is the name of the destination scalable predicate register PN8-PN15, with predicate-as-counter encoding, encoded in the "PNd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first source general-purpose register, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second source general-purpose register, encoded in the "Rm" field. |
| `<vl>` | `unknown` | `vl` | Is the vl specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<vl> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | VLx2 |
| 1 | VLx4 |

---
<details><summary>Metadata</summary>

- isa: `A64`
- sve-elem-type: `8-64-elem`
- source: `whilelo_pn_rr.xml`
</details>