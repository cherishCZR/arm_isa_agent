## WHILEGT
_ARM A64 Instruction_

**Title**: WHILEGT (predicate) -- A64 | **Class**: `sve2` | **XML ID**: `whilegt_p_p_rr`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: While decrementing signed scalar greater than scalar

**Description**:
Generate a predicate that starting from the highest numbered element is
true while the decrementing value of the first, signed
 scalar operand is greater than the second scalar operand and
false thereafter down to the
lowest numbered element.

The full  width of the scalar operands is significant
for the purposes of comparison, and the full width 
first operand is decremented by one for each destination
predicate element, irrespective of the predicate result
element size. The first general-purpose source register is not
itself updated.

The predicate result is placed in the predicate
destination register. Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

### Variant: `SVE2`
- **Assembly**: `WHILEGT  <Pd>.<T>, <R><n>, <R><m>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  13 12 11 10  9   4  3  |
|--------------------------------------------|
| 001 0010 1   size 1   Rm  00  0   sf  0   0   Rn  1   Pd  |
```

#### Decode (A64.sve.sve_cmpgpr.sve_int_while_rr.whilegt_p_p_rr_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer rsize = 32 << UInt(sf);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer d = UInt(Pd);
constant boolean unsigned = FALSE;
constant CmpOp op = Cmp_GT;
```

#### Execute (A64.sve.sve_cmpgpr.sve_int_while_rr.whilegt_p_p_rr_)

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

for e = elements-1 downto 0
    boolean cond;
    case op of
        when Cmp_GT cond = (Int(operand1, unsigned) >  Int(operand2, unsigned));
        when Cmp_GE cond = (Int(operand1, unsigned) >= Int(operand2, unsigned));

    last = last && cond;
    constant bit pbit = if last then '1' else '0';
    Elem[result, e, psize] = ZeroExtend(pbit, psize);
    operand1 = operand1 - 1;

PSTATE.<N,Z,C,V> = PredTest(mask, result, esize);
P[d, PL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

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
- source: `whilegt_p_p_rr.xml`
</details>