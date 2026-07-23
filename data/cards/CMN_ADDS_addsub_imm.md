## ADDS `[ALIAS]`
_ARM A64 Instruction_ (Alias of adds_addsub_imm.xml)

**Title**: CMN (immediate) -- A64 | **Class**: `general` | **XML ID**: `CMN_ADDS_addsub_imm`

**Summary**: Compare negative (immediate)

**Description**:
This instruction adds a register value and an
optionally-shifted immediate value. It updates the condition flags
based on the result, and discards the result.

### Variant: `Setting the condition flags (CMN_ADDS_32S_addsub_imm)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `CMN  <Wn|WSP>, #<imm>{, <shift>}`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `ADDS  WZR, <Wn|WSP>, #<imm>{, <shift>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  22 21   9   4  |
|--------------------------|
| sf  0   1   100010 sh  imm12 Rn  11111 |
```

### Variant: `Setting the condition flags (CMN_ADDS_64S_addsub_imm)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `CMN  <Xn|SP>, #<imm>{, <shift>}`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `ADDS  XZR, <Xn|SP>, #<imm>{, <shift>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  22 21   9   4  |
|--------------------------|
| sf  0   1   100010 sh  imm12 Rn  11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wn\|WSP>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm12` | Is an unsigned immediate, in the range 0 to 4095, encoded in the "imm12" field. |
| `<shift>` | `shift` | `sh` | Is the optional left shift to apply to the immediate, defaulting to LSL #0 and |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the source general-purpose register or stack pointer, encoded in the "Rn" field. |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | LSL #0 |
| 1 | LSL #12 |

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
- immediate-type: `imm12u`
- isa: `A64`
- source: `cmn_adds_addsub_imm.xml`
</details>