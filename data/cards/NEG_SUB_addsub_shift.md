## SUB `[ALIAS]`
_ARM A64 Instruction_ (Alias of sub_addsub_shift.xml)

**Title**: NEG (shifted register) -- A64 | **Class**: `general` | **XML ID**: `NEG_SUB_addsub_shift`

**Summary**: Negate (shifted register)

**Description**:
This instruction negates an optionally-shifted register value,
and writes the result to the destination register.

### Variant: `Not setting the condition flags (NEG_SUB_32_addsub_shift)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `NEG  <Wd>, <Wm>{, <shift> #<amount>}`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `SUB  <Wd>, WZR, <Wm>{, <shift> #<amount>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15   9   4  |
|--------------------------------|
| sf  1   0   01011 shift 0   Rm  imm6 11111 Rd  |
```

### Variant: `Not setting the condition flags (NEG_SUB_64_addsub_shift)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `NEG  <Xd>, <Xm>{, <shift> #<amount>}`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `SUB  <Xd>, XZR, <Xm>{, <shift> #<amount>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15   9   4  |
|--------------------------------|
| sf  1   0   01011 shift 0   Rm  imm6 11111 Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the general-purpose source register, encoded in the "Rm" field. |
| `<shift>` | `shift` | `shift` | Is the optional shift type to be applied to the second source operand, defaulting to LSL and |
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
| 11 | RESERVED |

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

- alias_mnemonic: `NEG`
- cond-setting: `no-s`
- isa: `A64`
- source: `neg_sub_addsub_shift.xml`
</details>