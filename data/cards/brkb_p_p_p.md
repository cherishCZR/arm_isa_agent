## BRKB
_ARM A64 Instruction_

**Title**: BRKB -- A64 | **Class**: `sve` | **XML ID**: `brkb_p_p_p`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Break before first true condition

**Description**:
Sets destination predicate elements up to but not
including the first active and true source element to true,
then sets subsequent elements to false.

Inactive elements in the destination predicate register remain unmodified or
are set to zero, depending on whether merging or zeroing
predication is selected.
Does not set the condition flags.

**Attributes**: Predicated

### Variant: `Not setting the condition flags`
- **Assembly**: `BRKB  <Pd>.B, <Pg>/<ZM>, <Pn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21  19  15  13   9  8   4  3  |
|-----------------------------------------|
| 001 0010 1   1   0   01  0000 01  Pg  0   Pn  M   Pd  |
```

#### Decode (A64.sve.sve_pred_gen_c.sve_int_break.brkb_p_p_p_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8;
constant integer g = UInt(Pg);
constant integer n = UInt(Pn);
constant integer d = UInt(Pd);
constant boolean merging = (M == '1');
constant boolean setflags = FALSE;
```

#### Execute (A64.sve.sve_pred_gen_c.sve_int_break.brkb_p_p_p_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(PL) operand = P[n, PL];
constant bits(PL) operand2 = if merging then P[d, PL] else Zeros(PL);
boolean break = FALSE;
bits(PL) result;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    constant boolean element = ActivePredicateElement(operand, e, esize);
    if ActivePredicateElement(mask, e, esize) then
        break = break || element;
        constant bit pbit = if !break then '1' else '0';
        Elem[result, e, psize] = ZeroExtend(pbit, psize);
    elsif merging then
        constant bit pbit = PredicateElement(operand2, e, esize);
        Elem[result, e, psize] = ZeroExtend(pbit, psize);
    else
        Elem[result, e, psize] = ZeroExtend('0', psize);

if setflags then
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
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register, encoded in the "Pg" field. |
| `<ZM>` | `register (128-bit)` | `M` | Is the predication qualifier, |
| `<Pn>` | `unknown` | `Pn` | Is the name of the source scalable predicate register, encoded in the "Pn" field. |

**<ZM> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | Z |
| 1 | M |

---
<details><summary>Metadata</summary>

- cond-setting: `no-s`
- isa: `A64`
- source: `brkb_p_p_p.xml`
</details>