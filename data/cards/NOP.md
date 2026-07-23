## NOP
_ARM A64 Instruction_

**Title**: NOP -- A64 | **Class**: `system` | **XML ID**: `NOP`

**Summary**: No operation

**Description**:
This instruction does nothing, other than advance the value of the
program counter by 4. This instruction can be used for instruction
alignment purposes.

### Variant: `System`
- **Assembly**: `NOP`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0000 000 11111 |
```

#### Decode (A64.control.hints.NOP_HI_hints)

```
// Empty.
```

#### Execute (A64.control.hints.NOP_HI_hints)

```
return; // Do nothing
```

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `nop.xml`
</details>