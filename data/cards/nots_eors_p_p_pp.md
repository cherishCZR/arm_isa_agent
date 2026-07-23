## EORS `[ALIAS]`
_ARM A64 Instruction_ (Alias of eors_p_p_pp.xml)

**Title**: NOTS -- A64 | **Class**: `sve` | **XML ID**: `nots_eors_p_p_pp`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Bitwise invert predicate, setting the condition flags

**Description**:
Bitwise invert each active element of the source predicate,
and place the results in the corresponding elements of the destination predicate. Inactive elements in the destination predicate register are set to zero. Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `Setting the condition flags`
- **Assembly**: `NOTS  <Pd>.B, <Pg>/Z, <Pn>.B`
- **Alias of**: `EORS  <Pd>.B, <Pg>/Z, <Pn>.B, <Pg>.B`
  Condition: Pm == Pg
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21  19  15  13   9  8   4  3  |
|-----------------------------------------|
| 001 0010 1   0   1   00  Pm  01  Pg  1   Pn  0   Pd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register, encoded in the "Pg" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the source scalable predicate register, encoded in the "Pn" field. |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the NZCV condition flags written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- alias_mnemonic: `NOTS`
- cond-setting: `s`
- isa: `A64`
- source: `nots_eors_p_p_pp.xml`
</details>