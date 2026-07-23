## ANDS `[ALIAS]`
_ARM A64 Instruction_ (Alias of ands_log_shift.xml)

**Title**: TST (shifted register) -- A64 | **Class**: `general` | **XML ID**: `TST_ANDS_log_shift`

**Summary**: Test (shifted register)

**Description**:
This instruction performs a bitwise AND operation on a register value
and an optionally-shifted register value. It updates the condition flags based
on the result, and discards the result.

### Variant: `Setting the condition flags (TST_ANDS_32_log_shift)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `TST  <Wn>, <Wm>{, <shift> #<amount>}`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `ANDS  WZR, <Wn>, <Wm>{, <shift> #<amount>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  21 20  15   9   4  |
|-----------------------------|
| sf  11  01010 shift 0   Rm  imm6 Rn  11111 |
```

### Variant: `Setting the condition flags (TST_ANDS_64_log_shift)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `TST  <Xn>, <Xm>{, <shift> #<amount>}`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `ANDS  XZR, <Xn>, <Xm>{, <shift> #<amount>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  21 20  15   9   4  |
|-----------------------------|
| sf  11  01010 shift 0   Rm  imm6 Rn  11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<shift>` | `shift` | `shift` | Is the optional shift to be applied to the final source, defaulting to LSL and |
| `<amount>` | `unknown` | `imm6` | For the "32-bit" variant: is the shift amount, in the range 0 to 31, defaulting to 0 and encoded in the "imm6" field. |
| `<amount>` | `unknown` | `imm6` | For the "64-bit" variant: is the shift amount, in the range 0 to 63, defaulting to 0 and encoded in the "imm6" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register, encoded in the "Rm" field. |

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

- alias_mnemonic: `TST`
- cond-setting: `S`
- isa: `A64`
- reguse: `shifted-reg`
- source: `tst_ands_log_shift.xml`
</details>