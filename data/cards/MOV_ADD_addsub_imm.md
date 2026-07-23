## ADD `[ALIAS]`
_ARM A64 Instruction_ (Alias of add_addsub_imm.xml)

**Title**: MOV (to/from SP) -- A64 | **Class**: `general` | **XML ID**: `MOV_ADD_addsub_imm`

**Summary**: Move register value to or from SP

**Description**:
This instruction copies the value of a register to or from the stack pointer.

### Variant: `Not setting the condition flags (MOV_ADD_32_addsub_imm)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `MOV  <Wd|WSP>, <Wn|WSP>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `ADD  <Wd|WSP>, <Wn|WSP>, #0`
  Condition: Rd == '11111' || Rn == '11111'
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  22 21   9   4  |
|--------------------------|
| sf  0   0   100010 0   000000000000 Rn  Rd  |
```

### Variant: `Not setting the condition flags (MOV_ADD_64_addsub_imm)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `MOV  <Xd|SP>, <Xn|SP>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `ADD  <Xd|SP>, <Xn|SP>, #0`
  Condition: Rd == '11111' || Rn == '11111'
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  22 21   9   4  |
|--------------------------|
| sf  0   0   100010 0   000000000000 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd\|WSP>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the destination general-purpose register or stack pointer, encoded in the "Rd" field. |
| `<Wn\|WSP>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<Xd\|SP>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register or stack pointer, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the source general-purpose register or stack pointer, encoded in the "Rn" field. |

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
- immediate-type: `imm12u`
- isa: `A64`
- source: `mov_add_addsub_imm.xml`
</details>