## SBFM `[ALIAS]`
_ARM A64 Instruction_ (Alias of sbfm.xml)

**Title**: SXTB -- A64 | **Class**: `general` | **XML ID**: `SXTB_SBFM`

**Summary**: Signed extend byte

**Description**:
This instruction extracts an 8-bit value from a register, sign-extends it
to the size of the register, and writes the result to
the destination register.

### Variant: `With sign replication to left and zeros to right (SXTB_SBFM_32M_bitfield)` (32-bit)
- **Condition**: `sf == 0 && N == 0`
- **Assembly**: `SXTB  <Wd>, <Wn>`
- **Fixed bits**: `sf`=`0`, `N`=`0`
- **Bit Pattern**: `??????????????????????0????????0`
- **Alias of**: `SBFM  <Wd>, <Wn>, #0, #7`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  00  100110 N   000000 000111 Rn  Rd  |
```

### Variant: `With sign replication to left and zeros to right (SXTB_SBFM_64M_bitfield)` (64-bit)
- **Condition**: `sf == 1 && N == 1`
- **Assembly**: `SXTB  <Xd>, <Wn>`
- **Fixed bits**: `sf`=`1`, `N`=`1`
- **Bit Pattern**: `??????????????????????1????????1`
- **Alias of**: `SBFM  <Xd>, <Xn>, #0, #7`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  00  100110 N   000000 000111 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |

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

- alias_mnemonic: `SXTB`
- bitfield-fill: `signed-fill`
- isa: `A64`
- source: `sxtb_sbfm.xml`
</details>