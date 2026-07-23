## SBC `[ALIAS]`
_ARM A64 Instruction_ (Alias of sbc.xml)

**Title**: NGC -- A64 | **Class**: `general` | **XML ID**: `NGC_SBC`

**Summary**: Negate with carry

**Description**:
This instruction negates the sum of a register value and
the value of NOT (Carry flag), and writes the result
to the destination register.

### Variant: `Not setting the condition flags (NGC_SBC_32_addsub_carry)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `NGC  <Wd>, <Wm>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `SBC  <Wd>, WZR, <Wm>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15   9   4  |
|--------------------------|
| sf  1   0   11010000 Rm  000000 11111 Rd  |
```

### Variant: `Not setting the condition flags (NGC_SBC_64_addsub_carry)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `NGC  <Xd>, <Xm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `SBC  <Xd>, XZR, <Xm>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15   9   4  |
|--------------------------|
| sf  1   0   11010000 Rm  000000 11111 Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the general-purpose source register, encoded in the "Rm" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the general-purpose source register, encoded in the "Rm" field. |

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

- alias_mnemonic: `NGC`
- cond-setting: `no-s`
- isa: `A64`
- source: `ngc_sbc.xml`
</details>