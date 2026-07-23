## UBFM `[ALIAS]`
_ARM A64 Instruction_ (Alias of ubfm.xml)

**Title**: LSL (immediate) -- A64 | **Class**: `general` | **XML ID**: `LSL_UBFM`

**Summary**: Logical shift left (immediate)

**Description**:
This instruction shifts a register value left by an immediate
number of bits, shifting in zeros, and writes the result to the destination
register.

### Variant: `With zeros to left and right (LSL_UBFM_32M_bitfield)` (32-bit)
- **Condition**: `sf == 0 && N == 0 && imms != 011111`
- **Assembly**: `LSL  <Wd>, <Wn>, #<shift>`
- **Fixed bits**: `sf`=`0`, `N`=`0`, `imms`=`ZNNNNN`
- **Bit Pattern**: `??????????????????????0????????0`
- **Alias of**: `UBFM  <Wd>, <Wn>, #(-<shift>  MOD  32), #(31-<shift>)`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  10  100110 N   immr imms Rn  Rd  |
```

### Variant: `With zeros to left and right (LSL_UBFM_64M_bitfield)` (64-bit)
- **Condition**: `sf == 1 && N == 1 && imms != 111111`
- **Assembly**: `LSL  <Xd>, <Xn>, #<shift>`
- **Fixed bits**: `sf`=`1`, `N`=`1`, `imms`=`NNNNNN`
- **Bit Pattern**: `??????????????????????1????????1`
- **Alias of**: `UBFM  <Xd>, <Xn>, #(-<shift>  MOD  64), #(63-<shift>)`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  10  100110 N   immr imms Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<shift>` | `shift` | `immr` | For the "32-bit" variant: is the shift amount, in the range 0 to 31. |
| `<shift>` | `shift` | `immr` | For the "64-bit" variant: is the shift amount, in the range 0 to 63. |
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

- alias_mnemonic: `LSL`
- bitfield-fill: `zero-fill`
- isa: `A64`
- source: `lsl_ubfm.xml`
</details>