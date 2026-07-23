## SEL
_ARM A64 Instruction_

**Title**: SEL (predicates) -- A64 | **Class**: `sve` | **XML ID**: `sel_p_p_pp`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Conditionally select elements from two predicates

**Description**:
Read active elements from the first source predicate and
inactive elements from the second source predicate and place
in the corresponding elements of the destination predicate.
Does not set the condition flags.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `SEL  <Pd>.B, <Pg>, <Pn>.B, <Pm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21  19  15  13   9  8   4  3  |
|-----------------------------------------|
| 001 0010 1   0   0   00  Pm  01  Pg  1   Pn  1   Pd  |
```

#### Decode (A64.sve.sve_pred_gen_a.sve_int_pred_log.sel_p_p_pp_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8;
constant integer g = UInt(Pg);
constant integer n = UInt(Pn);
constant integer m = UInt(Pm);
constant integer d = UInt(Pd);
```

#### Execute (A64.sve.sve_pred_gen_a.sve_int_pred_log.sel_p_p_pp_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(PL) operand1 = P[n, PL];
constant bits(PL) operand2 = P[m, PL];
bits(PL) result;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    constant bit element1 = PredicateElement(operand1, e, esize);
    constant bit element2 = PredicateElement(operand2, e, esize);
    if ActivePredicateElement(mask, e, esize) then
        Elem[result, e, psize] = ZeroExtend(element1, psize);
    else
        Elem[result, e, psize] = ZeroExtend(element2, psize);

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

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sel_p_p_pp.xml`
</details>