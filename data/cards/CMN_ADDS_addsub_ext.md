## ADDS `[ALIAS]`
_ARM A64 Instruction_ (Alias of adds_addsub_ext.xml)

**Title**: CMN (extended register) -- A64 | **Class**: `general` | **XML ID**: `CMN_ADDS_addsub_ext`

**Summary**: Compare negative (extended register)

**Description**:
This instruction adds a register value and a
sign or zero-extended register value, followed by an optional
left shift amount. The argument that is extended from the
<Rm> register can be a byte, halfword, word, or
doubleword. It updates the condition flags based on the
result, and discards the result.

### Variant: `Setting the condition flags (CMN_ADDS_32S_addsub_ext)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `CMN  <Wn|WSP>, <Wm>{, <extend> {#<amount>}}`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `ADDS  WZR, <Wn|WSP>, <Wm>{, <extend> {#<amount>}}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  12   9   4  |
|-----------------------------------|
| sf  0   1   01011 00  1   Rm  option imm3 Rn  11111 |
```

### Variant: `Setting the condition flags (CMN_ADDS_64S_addsub_ext)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `CMN  <Xn|SP>, <R><m>{, <extend> {#<amount>}}`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `ADDS  XZR, <Xn|SP>, <R><m>{, <extend> {#<amount>}}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  12   9   4  |
|-----------------------------------|
| sf  0   1   01011 00  1   Rm  option imm3 Rn  11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wn\|WSP>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<extend>` | `shift` | `option` | For the "32-bit" variant: is the extension to be applied to the second source operand, |
| `<extend>` | `shift` | `option` | For the "64-bit" variant: is the extension to be applied to the second source operand, |
| `<amount>` | `unknown` | `imm3` | Is the left shift amount to be applied after extension in the range 0 to 4, defaulting to 0, encoded in the "imm3" field. It must be absent when <exte |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<R>` | `unknown` | `option` | Is a width specifier, |
| `<m>` | `unknown` | `Rm` | Is the number [0-30] of the second general-purpose source register or the name ZR (31), encoded in the "Rm" field. |

**<extend> Value Table**:

| bitfield | symbol |
|---|---|
| 000 | UXTB |
| 001 | UXTH |
| 010 | LSL\|UXTW |
| 011 | UXTX |
| 100 | SXTB |
| 101 | SXTH |
| 110 | SXTW |
| 111 | SXTX |

**<extend> Value Table**:

| bitfield | symbol |
|---|---|
| 000 | UXTB |
| 001 | UXTH |
| 010 | UXTW |
| 011 | LSL\|UXTX |
| 100 | SXTB |
| 101 | SXTH |
| 110 | SXTW |
| 111 | SXTX |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| 00x | W |
| 010 | W |
| x11 | X |
| 10x | W |
| 110 | W |

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

- alias_mnemonic: `CMN`
- cond-setting: `S`
- isa: `A64`
- source: `cmn_adds_addsub_ext.xml`
</details>