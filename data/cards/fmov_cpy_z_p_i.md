## CPY `[ALIAS]`
_ARM A64 Instruction_ (Alias of cpy_z_p_i.xml)

**Title**: FMOV (zero, predicated) -- A64 | **Class**: `sve` | **XML ID**: `fmov_cpy_z_p_i`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move floating-point +0.0 to vector elements (predicated)

**Description**:
Move floating-point constant +0.0 to each active element in
the destination vector. Inactive elements in the destination vector register remain unmodified.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `FMOV  <Zd>.<T>, <Pg>/M, #0.0`
- **Alias of**: `CPY  <Zd>.<T>, <Pg>/M, #0`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  19  15 14 13 12   4  |
|-----------------------------------|
| 000 0010 1   size 01  Pg  0   1   0   00000000 Zd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register, encoded in the "Pg" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
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
                
              
            
          
        
        This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first source element size in the preferred disassembly of this instructio
... (truncated)

---
<details><summary>Metadata</summary>

- alias_mnemonic: `FMOV`
- isa: `A64`
- source: `fmov_cpy_z_p_i.xml`
</details>