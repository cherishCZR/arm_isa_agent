## BRKPBS
_ARM A64 Instruction_

**Title**: BRKPBS -- A64 | **Class**: `sve` | **XML ID**: `brkpbs_p_p_pp`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Break before first true condition, propagating from previous partition and setting the condition flags

**Description**:
If the last active element of the first source predicate is false then
set the destination predicate to all-false.
Otherwise sets destination predicate elements up to but not
including the first active and true source element to true,
then sets subsequent elements to false. Inactive elements in the destination predicate register are set to zero. Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

**Attributes**: Predicated

### Variant: `Setting the condition flags`
- **Assembly**: `BRKPBS  <Pd>.B, <Pg>/Z, <Pn>.B, <Pm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21  19  15  13   9  8   4  3  |
|-----------------------------------------|
| 001 0010 1   0   1   00  Pm  11  Pg  0   Pn  1   Pd  |
```

#### Decode (A64.sve.sve_pred_gen_b.sve_int_brkp.brkpbs_p_p_pp_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8;
constant integer g = UInt(Pg);
constant integer n = UInt(Pn);
constant integer m = UInt(Pm);
constant integer d = UInt(Pd);
constant boolean setflags = TRUE;
```

#### Execute (A64.sve.sve_pred_gen_b.sve_int_brkp.brkpbs_p_p_pp_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(PL) operand1 = P[n, PL];
constant bits(PL) operand2 = P[m, PL];
bits(PL) result;
boolean last = (LastActive(mask, operand1, 8) == '1');

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, 8) then
        last = last && (!ActivePredicateElement(operand2, e, 8));
        constant bit pbit = if last then '1' else '0';
        Elem[result, e, 1] = ZeroExtend(pbit, 1);
    else
        Elem[result, e, 1] = ZeroExtend('0', 1);

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
| `<Pn>` | `unknown` | `Pn` | Is the name of the first source scalable predicate register, encoded in the "Pn" field. |
| `<Pm>` | `unknown` | `Pm` | Is the name of the second source scalable predicate register, encoded in the "Pm" field. |

### Operational Notes

If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the NZCV condition flags written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- cond-setting: `s`
- isa: `A64`
- source: `brkpbs_p_p_pp.xml`
</details>