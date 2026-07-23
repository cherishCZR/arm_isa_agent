## ORR `[ALIAS]`
_ARM A64 Instruction_ (Alias of orr_p_p_pp.xml)

**Title**: MOV -- A64 | **Class**: `sve` | **XML ID**: `mov_orr_p_p_pp`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move predicate (unpredicated)

**Description**:
Read all elements from the source predicate and place in the
destination predicate.
This instruction is unpredicated. Does not set the condition flags.

For programmer convenience, an assembler must also accept
      predicate-as-counter register names for the source and destination
      predicate registers.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `Not setting the condition flags`
- **Assembly**: `MOV  <Pd>.B, <Pn>.B`
- **Alias of**: `ORR  <Pd>.B, <Pn>/Z, <Pn>.B, <Pn>.B`
  Condition: S == '0' && Pn == Pm && Pm == Pg
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21  19  15  13   9  8   4  3  |
|-----------------------------------------|
| 001 0010 1   1   0   00  Pm  01  Pg  0   Pn  0   Pd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the source scalable predicate register, encoded in the "Pn" field. |

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

- alias_mnemonic: `MOV`
- cond-setting: `no-s`
- isa: `A64`
- source: `mov_orr_p_p_pp.xml`
</details>