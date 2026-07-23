## SBFM `[ALIAS]`
_ARM A64 Instruction_ (Alias of sbfm.xml)

**Title**: SXTW -- A64 | **Class**: `general` | **XML ID**: `SXTW_SBFM`

**Summary**: Sign extend word

**Description**:
This instruction sign-extends a word to the size of the register, and writes the result to
the destination register.

### Variant: `With sign replication to left and zeros to right` (64-bit)
- **Assembly**: `SXTW  <Xd>, <Wn>`
- **Alias of**: `SBFM  <Xd>, <Xn>, #0, #31`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  25  22 21  15   9   4  |
|-----------------------------|
| 1   00  100 110 1   000000 011111 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
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

- alias_mnemonic: `SXTW`
- bitfield-fill: `signed-fill`
- datatype: `64`
- isa: `A64`
- source: `sxtw_sbfm.xml`
</details>