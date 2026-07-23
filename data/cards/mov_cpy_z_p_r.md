## CPY `[ALIAS]`
_ARM A64 Instruction_ (Alias of cpy_z_p_r.xml)

**Title**: MOV (scalar, predicated) -- A64 | **Class**: `sve` | **XML ID**: `mov_cpy_z_p_r`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move general-purpose register to vector elements (predicated)

**Description**:
Move the general-purpose scalar source register
to each active element in the destination vector. Inactive elements in the destination vector register remain unmodified.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `MOV  <Zd>.<T>, <Pg>/M, <R><n|SP>`
- **Alias of**: `CPY  <Zd>.<T>, <Pg>/M, <R><n|SP>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  16 15  13 12   9   4  |
|-----------------------------------------|
| 000 0010 1   size 1   0   100 0   10  1   Pg  Rn  Zd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<R>` | `unknown` | `size` | Is a width specifier, |
| `<n\|SP>` | `unknown` | `Rn` | Is the number [0-30] of the general-purpose source register or the name SP (31), encoded in the "Rn" field. |

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
| 00 | W |
| 01 | W |
| 10 | W |
| 11 | X |

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

- alias_mnemonic: `MOV`
- isa: `A64`
- source: `mov_cpy_z_p_r.xml`
</details>