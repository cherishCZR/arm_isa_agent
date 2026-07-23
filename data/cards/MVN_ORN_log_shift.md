## ORN `[ALIAS]`
_ARM A64 Instruction_ (Alias of orn_log_shift.xml)

**Title**: MVN -- A64 | **Class**: `general` | **XML ID**: `MVN_ORN_log_shift`

**Summary**: Bitwise NOT

**Description**:
This instruction writes the bitwise inverse of a register
value to the destination register.

### Variant: `Not setting the condition flags (MVN_ORN_32_log_shift)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `MVN  <Wd>, <Wm>{, <shift> #<amount>}`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `ORN  <Wd>, WZR, <Wm>{, <shift> #<amount>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  21 20  15   9   4  |
|-----------------------------|
| sf  01  01010 shift 1   Rm  imm6 11111 Rd  |
```

### Variant: `Not setting the condition flags (MVN_ORN_64_log_shift)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `MVN  <Xd>, <Xm>{, <shift> #<amount>}`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `ORN  <Xd>, XZR, <Xm>{, <shift> #<amount>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  21 20  15   9   4  |
|-----------------------------|
| sf  01  01010 shift 1   Rm  imm6 11111 Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the general-purpose source register, encoded in the "Rm" field. |
| `<shift>` | `shift` | `shift` | Is the optional shift to be applied to the final source, defaulting to LSL and |
| `<amount>` | `unknown` | `imm6` | For the "32-bit" variant: is the shift amount, in the range 0 to 31, defaulting to 0 and encoded in the "imm6" field. |
| `<amount>` | `unknown` | `imm6` | For the "64-bit" variant: is the shift amount, in the range 0 to 63, defaulting to 0 and encoded in the "imm6" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the general-purpose source register, encoded in the "Rm" field. |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | LSL |
| 01 | LSR |
| 10 | ASR |
| 11 | ROR |

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

- alias_mnemonic: `MVN`
- cond-setting: `no-s`
- isa: `A64`
- reguse: `shifted-reg`
- source: `mvn_orn_log_shift.xml`
</details>