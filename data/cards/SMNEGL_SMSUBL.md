## SMSUBL `[ALIAS]`
_ARM A64 Instruction_ (Alias of smsubl.xml)

**Title**: SMNEGL -- A64 | **Class**: `general` | **XML ID**: `SMNEGL_SMSUBL`

**Summary**: Signed multiply-negate long

**Description**:
This instruction multiplies two 32-bit register values, negates the
product, and writes the result to the 64-bit destination register.

### Variant: `64-bit`
- **Assembly**: `SMNEGL  <Xd>, <Wn>, <Wm>`
- **Alias of**: `SMSUBL  <Xd>, <Wn>, <Wm>, XZR`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28 27  24 23 22  20  15 14   9   4  |
|--------------------------------------|
| 1   00  1   101 1   0   01  Rm  1   11111 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register holding the multiplicand, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register holding the multiplier, encoded in the "Rm" field. |

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

- alias_mnemonic: `SMNEGL`
- datatype: `64`
- isa: `A64`
- source: `smnegl_smsubl.xml`
</details>