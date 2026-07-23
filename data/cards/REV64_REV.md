## REV `[ALIAS]`
_ARM A64 Instruction_ (Alias of rev.xml)

**Title**: REV64 -- A64 | **Class**: `general` | **XML ID**: `REV64_REV`

**Summary**: Reverse bytes

**Description**:
This instruction reverses the byte order in a 64-bit general-purpose
register.

When assembling for Armv8.2, an assembler must support this pseudo-instruction. It is OPTIONAL whether an assembler supports this pseudo-instruction when assembling for an architecture earlier than Armv8.2.

### Variant: `Integer` (64-bit)
- **Assembly**: `REV64  <Xd>, <Xn>`
- **Alias of**: `REV  <Xd>, <Xn>`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  15  11   9   4  |
|-----------------------------------|
| 1   1   0   1   101 0110 00000 0000 11  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register, encoded in the "Rn" field. |

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

- alias_mnemonic: `REV64`
- datatype: `64`
- isa: `A64`
- source: `rev64_rev.xml`
</details>