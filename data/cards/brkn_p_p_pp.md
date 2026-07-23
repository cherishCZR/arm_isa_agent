## BRKN
_ARM A64 Instruction_

**Title**: BRKN -- A64 | **Class**: `sve` | **XML ID**: `brkn_p_p_pp`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Propagate break to next partition

**Description**:
If the last active element of the first source predicate is false then
set the destination predicate to all-false.
Otherwise leaves the destination and second source predicate unchanged. Does not set the condition flags.

**Attributes**: Predicated

### Variant: `Not setting the condition flags`
- **Assembly**: `BRKN  <Pdm>.B, <Pg>/Z, <Pn>.B, <Pdm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21  19  15  13   9  8   4  3  |
|-----------------------------------------|
| 001 0010 1   0   0   01  1000 01  Pg  0   Pn  0   Pdm |
```

#### Decode (A64.sve.sve_pred_gen_c.sve_int_brkn.brkn_p_p_pp_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer g = UInt(Pg);
constant integer n = UInt(Pn);
constant integer dm = UInt(Pdm);
constant boolean setflags = FALSE;
```

#### Execute (A64.sve.sve_pred_gen_c.sve_int_brkn.brkn_p_p_pp_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant bits(PL) mask = P[g, PL];
constant bits(PL) operand1 = P[n, PL];
constant bits(PL) operand2 = P[dm, PL];
bits(PL) result;

if LastActive(mask, operand1, 8) == '1' then
    result = operand2;
else
    result = Zeros(PL);

if setflags then
    PSTATE.<N,Z,C,V> = PredTest(Ones(PL), result, 8);
P[dm, PL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pdm>` | `unknown` | `Pdm` | Is the name of the second source and destination scalable predicate register, encoded in the "Pdm" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register, encoded in the "Pg" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the first source scalable predicate register, encoded in the "Pn" field. |

---
<details><summary>Metadata</summary>

- cond-setting: `no-s`
- isa: `A64`
- source: `brkn_p_p_pp.xml`
</details>