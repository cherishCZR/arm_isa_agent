## ANDS `[ALIAS]`
_ARM A64 Instruction_ (Alias of ands_log_imm.xml)

**Title**: TST (immediate) -- A64 | **Class**: `general` | **XML ID**: `TST_ANDS_log_imm`

**Summary**: Test bits (immediate)

**Description**:
This instruction performs a bitwise AND of a register value and an
immediate value, and discards the results. It updates the condition
flags based on the result.

### Variant: `Setting the condition flags (TST_ANDS_32S_log_imm)` (32-bit)
- **Condition**: `sf == 0 && N == 0`
- **Assembly**: `TST  <Wn>, #<imm>`
- **Fixed bits**: `sf`=`0`, `N`=`0`
- **Bit Pattern**: `??????????????????????0????????0`
- **Alias of**: `ANDS  WZR, <Wn>, #<imm>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  11  100100 N   immr imms Rn  11111 |
```

### Variant: `Setting the condition flags (TST_ANDS_64S_log_imm)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `TST  <Xn>, #<imm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `ANDS  XZR, <Xn>, #<imm>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  11  100100 N   immr imms Rn  11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `immr:imms` | For the "32-bit" variant: is the bitmask immediate, encoded in "imms:immr". |
| `<imm>` | `immediate` | `N:immr:imms` | For the "64-bit" variant: is the bitmask immediate, encoded in "N:imms:immr". |
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

- alias_mnemonic: `TST`
- cond-setting: `S`
- immediate-type: `imm12-bitfield`
- isa: `A64`
- source: `tst_ands_log_imm.xml`
</details>