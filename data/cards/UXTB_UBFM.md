## UBFM `[ALIAS]`
_ARM A64 Instruction_ (Alias of ubfm.xml)

**Title**: UXTB -- A64 | **Class**: `general` | **XML ID**: `UXTB_UBFM`

**Summary**: Unsigned extend byte

**Description**:
This instruction extracts an 8-bit value from a register, zero-extends it
to the size of the register, and writes the result to the destination register.

### Variant: `With zeros to left and right` (32-bit)
- **Assembly**: `UXTB  <Wd>, <Wn>`
- **Alias of**: `UBFM  <Wd>, <Wn>, #0, #7`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  25  22 21  15   9   4  |
|-----------------------------|
| 0   10  100 110 0   000000 000111 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |

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

- alias_mnemonic: `UXTB`
- bitfield-fill: `zero-fill`
- datatype: `32`
- isa: `A64`
- source: `uxtb_ubfm.xml`
</details>