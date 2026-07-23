## WHILELS
_ARM A64 Instruction_

**Title**: WHILELS (predicate) -- A64 | **Class**: `sve` | **XML ID**: `whilels_p_p_rr`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: While incrementing unsigned scalar lower or same as scalar

**Description**:
Generate a predicate that starting from the lowest numbered element is
true while the incrementing value of the first, unsigned
 scalar operand is lower or same as the second scalar operand and
false thereafter up to the highest numbered element.

If the second scalar operand is equal to the
maximum unsigned
 integer value then a condition which includes
an equality test can never fail and the result will be
an all-true predicate.

The full  width of the scalar operands is significant
for the purposes of comparison, and the full width 
first operand is incremented by one for each destination
predicate element, irrespective of the predicate result
element size. The first general-purpose source register is not
itself updated.

The predicate result is placed in the predicate
destination register. Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

### Variant: `SVE`
- **Assembly**: `WHILELS  <Pd>.<T>, <R><n>, <R><m>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  13 12 11 10  9   4  3  |
|--------------------------------------------|
| 001 0010 1   size 1   Rm  00  0   sf  1   1   Rn  1   Pd  |
```

#### Decode (A64.sve.sve_cmpgpr.sve_int_while_rr.whilels_p_p_rr_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer rsize = 32 << UInt(sf);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer d = UInt(Pd);
constant boolean unsigned = TRUE;
constant CmpOp op = Cmp_LE;
```

#### Execute (A64.sve.sve_cmpgpr.sve_int_while_rr.whilels_p_p_rr_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = Ones(PL);
bits(rsize) operand1 = X[n, rsize];
constant bits(rsize) operand2 = X[m, rsize];
bits(PL) result;
boolean last = TRUE;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    boolean cond;
    case op of
        when Cmp_LT cond = (Int(operand1, unsigned) <  Int(operand2, unsigned));
        when Cmp_LE cond = (Int(operand1, unsigned) <= Int(operand2, unsigned));

    last = last && cond;
    constant bit pbit = if last then '1' else '0';
    Elem[result, e, psize] = ZeroExtend(pbit, psize);
    operand1 = operand1 + 1;

PSTATE.<N,Z,C,V> = PredTest(mask, result, esize);
P[d, PL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<R>` | `unknown` | `sf` | Is a width specifier, |
| `<n>` | `unknown` | `Rn` | Is the number [0-30] of the source general-purpose register or the name ZR (31), encoded in the "Rn" field. |
| `<m>` | `unknown` | `Rm` | Is the number [0-30] of the source general-purpose register or the name ZR (31), encoded in the "Rm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | W |
| 1 | X |

---
<details><summary>Metadata</summary>

- isa: `A64`
- sve-elem-type: `8-64-elem`
- source: `whilels_p_p_rr.xml`
</details>