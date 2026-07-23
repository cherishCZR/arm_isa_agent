## MOVN `[ALIAS]`
_ARM A64 Instruction_ (Alias of movn.xml)

**Title**: MOV (inverted wide immediate) -- A64 | **Class**: `general` | **XML ID**: `MOV_MOVN`

**Summary**: Move inverted wide immediate value

**Description**:
This instruction moves an inverted 16-bit immediate
value to a register.

### Variant: `Immediate packed into 16-bit value and 2-bit shift (MOV_MOVN_32_movewide)` (32-bit)
- **Condition**: `sf == 0 && hw == 0x`
- **Assembly**: `MOV  <Wd>, #<imm>`
- **Fixed bits**: `sf`=`0`, `hw`=`0`
- **Bit Pattern**: `??????????????????????0????????0`
- **Alias of**: `MOVN  <Wd>, #<imm16>, LSL  #<shift>`
  Condition: !(
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22  20   4  |
|--------------------|
| sf  00  100101 hw  imm16 Rd  |
```

### Variant: `Immediate packed into 16-bit value and 2-bit shift (MOV_MOVN_64_movewide)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `MOV  <Xd>, #<imm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `MOVN  <Xd>, #<imm16>, LSL  #<shift>`
  Condition: !(
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22  20   4  |
|--------------------|
| sf  00  100101 hw  imm16 Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<imm>` | `immediate` | `imm16:hw` | For the "32-bit" variant: is a 32-bit immediate, the bitwise inverse of which can be encoded in "imm16:hw", but excluding 0xFFFF0000 and 0x0000FFFF |
| `<imm>` | `immediate` | `imm16:hw` | For the "64-bit" variant: is a 64-bit immediate, the bitwise inverse of which can be encoded in "imm16:hw". |
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

- alias_mnemonic: `MOV`
- immediate-type: `imm18-packed`
- isa: `A64`
- source: `mov_movn.xml`
</details>