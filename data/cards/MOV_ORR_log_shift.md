## ORR `[ALIAS]`
_ARM A64 Instruction_ (Alias of orr_log_shift.xml)

**Title**: MOV (register) -- A64 | **Class**: `general` | **XML ID**: `MOV_ORR_log_shift`

**Summary**: Move register value

**Description**:
This instruction copies the value in a source register to the destination register.

### Variant: `Not setting the condition flags (MOV_ORR_32_log_shift)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `MOV  <Wd>, <Wm>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `ORR  <Wd>, WZR, <Wm>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  21 20  15   9   4  |
|-----------------------------|
| sf  01  01010 00  0   Rm  000000 11111 Rd  |
```

### Variant: `Not setting the condition flags (MOV_ORR_64_log_shift)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `MOV  <Xd>, <Xm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `ORR  <Xd>, XZR, <Xm>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  21 20  15   9   4  |
|-----------------------------|
| sf  01  01010 00  0   Rm  000000 11111 Rd  |
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

- alias_mnemonic: `MOV`
- cond-setting: `no-s`
- isa: `A64`
- reguse: `shifted-reg`
- source: `mov_orr_log_shift.xml`
</details>