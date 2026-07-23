## ORR `[ALIAS]`
_ARM A64 Instruction_ (Alias of orr_log_imm.xml)

**Title**: MOV (bitmask immediate) -- A64 | **Class**: `general` | **XML ID**: `MOV_ORR_log_imm`

**Summary**: Move bitmask immediate value

**Description**:
This instruction writes a bitmask immediate
value to a register.

### Variant: `Not setting the condition flags (MOV_ORR_32_log_imm)` (32-bit)
- **Condition**: `sf == 0 && N == 0`
- **Assembly**: `MOV  <Wd|WSP>, #<imm>`
- **Fixed bits**: `sf`=`0`, `N`=`0`
- **Bit Pattern**: `??????????????????????0????????0`
- **Alias of**: `ORR  <Wd|WSP>, WZR, #<imm>`
  Condition: !
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  01  100100 N   immr imms 11111 Rd  |
```

### Variant: `Not setting the condition flags (MOV_ORR_64_log_imm)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `MOV  <Xd|SP>, #<imm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `ORR  <Xd|SP>, XZR, #<imm>`
  Condition: !
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  01  100100 N   immr imms 11111 Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd\|WSP>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the destination general-purpose register or stack pointer, encoded in the "Rd" field. |
| `<imm>` | `immediate` | `immr:imms` | For the "32-bit" variant: is the bitmask immediate, encoded in "imms:immr", but excluding values which could be encoded by MOVZ or MOVN. |
| `<imm>` | `immediate` | `N:immr:imms` | For the "64-bit" variant: is the bitmask immediate, encoded in "N:imms:immr", but excluding values which could be encoded by MOVZ or MOVN. |
| `<Xd\|SP>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register or stack pointer, encoded in the "Rd" field. |

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
- immediate-type: `imm12-bitfield`
- isa: `A64`
- source: `mov_orr_log_imm.xml`
</details>