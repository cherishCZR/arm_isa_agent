## SBFM `[ALIAS]`
_ARM A64 Instruction_ (Alias of sbfm.xml)

**Title**: ASR (immediate) -- A64 | **Class**: `general` | **XML ID**: `ASR_SBFM`

**Summary**: Arithmetic shift right (immediate)

**Description**:
This instruction shifts a register value right by an
immediate number of bits, shifting in copies of the sign bit in the upper
bits and zeros in the lower bits, and writes the result to the destination
register.

### Variant: `With sign replication to left and zeros to right (ASR_SBFM_32M_bitfield)` (32-bit)
- **Condition**: `sf == 0 && N == 0 && imms == 011111`
- **Assembly**: `ASR  <Wd>, <Wn>, #<shift>`
- **Fixed bits**: `sf`=`0`, `N`=`0`, `imms`=`0`
- **Bit Pattern**: `???????????????0??????0????????0`
- **Alias of**: `SBFM  <Wd>, <Wn>, #<shift>, #31`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  00  100110 N   immr x11111 Rn  Rd  |
```

### Variant: `With sign replication to left and zeros to right (ASR_SBFM_64M_bitfield)` (64-bit)
- **Condition**: `sf == 1 && N == 1 && imms == 111111`
- **Assembly**: `ASR  <Xd>, <Xn>, #<shift>`
- **Fixed bits**: `sf`=`1`, `N`=`1`, `imms`=`1`
- **Bit Pattern**: `???????????????1??????1????????1`
- **Alias of**: `SBFM  <Xd>, <Xn>, #<shift>, #63`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  00  100110 N   immr x11111 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<shift>` | `shift` | `immr` | For the "32-bit" variant: is the shift amount, in the range 0 to 31, encoded in the "immr" field. |
| `<shift>` | `shift` | `immr` | For the "64-bit" variant: is the shift amount, in the range 0 to 63, encoded in the "immr" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
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

- alias_mnemonic: `ASR`
- bitfield-fill: `signed-fill`
- isa: `A64`
- source: `asr_sbfm.xml`
</details>