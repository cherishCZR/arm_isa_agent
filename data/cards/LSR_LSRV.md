## LSRV `[ALIAS]`
_ARM A64 Instruction_ (Alias of lsrv.xml)

**Title**: LSR (register) -- A64 | **Class**: `general` | **XML ID**: `LSR_LSRV`

**Summary**: Logical shift right (register)

**Description**:
This instruction shifts a register value right by a
variable number of bits, shifting in zeros, and writes the result to
the destination register. The value of the second source register modulo
the register size in bits gives the number of bits by which
the first source register is right-shifted.

### Variant: `Integer (LSR_LSRV_32_dp_2src)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `LSR  <Wd>, <Wn>, <Wm>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `LSRV  <Wd>, <Wn>, <Wm>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11   9   4  |
|-----------------------------|
| sf  0   0   11010110 Rm  0010 01  Rn  Rd  |
```

### Variant: `Integer (LSR_LSRV_64_dp_2src)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `LSR  <Xd>, <Xn>, <Xm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `LSRV  <Xd>, <Xn>, <Xm>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11   9   4  |
|-----------------------------|
| sf  0   0   11010110 Rm  0010 01  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register holding a shift amount from 0 to 31 in its bottom 5 bits, encoded in the "Rm" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register holding a shift amount from 0 to 63 in its bottom 6 bits, encoded in the "Rm" field. |

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

- alias_mnemonic: `LSR`
- isa: `A64`
- source: `lsr_lsrv.xml`
</details>