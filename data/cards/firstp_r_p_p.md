## FIRSTP
_ARM A64 Instruction_

**Title**: FIRSTP -- A64 | **Class**: `sve2` | **XML ID**: `firstp_r_p_p`

**Architecture**: `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2)

**Summary**: Scalar index of first true predicate element (predicated)

**Description**:
Determines the index of the first active and true element of the source
predicate, or minus one if there are no active and true elements, and
places the scalar result in the destination general-purpose register.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `FIRSTP  <Xd>, <Pg>, <Pn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15  13   9  8   4  |
|-----------------------------------|
| 001 0010 1   size 100 001 10  Pg  0   Pn  Rd  |
```

#### Decode (A64.sve.sve_pred_count_a.sve_int_pcount_pred.firstp_r_p_p_)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Pn);
constant integer d = UInt(Rd);
```

#### Execute (A64.sve.sve_pred_count_a.sve_int_pcount_pred.firstp_r_p_p_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(PL) operand = P[n, PL];
integer index = -1;

for e = 0 to elements-1
    if (index == -1 && ActivePredicateElement(mask, e, esize) &&
          ActivePredicateElement(operand, e, esize)) then
        index = e;

X[d, 64] = index<63:0>;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p2) \|\| IsFeatureImplemented(FEAT_SME2p2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register, encoded in the "Rd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register, encoded in the "Pg" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the source scalable predicate register, encoded in the "Pn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the general-purpose register written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `firstp_r_p_p.xml`
</details>