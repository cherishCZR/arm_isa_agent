## SBFM `[ALIAS]`
_ARM A64 Instruction_ (Alias of sbfm.xml)

**Title**: SBFIZ -- A64 | **Class**: `general` | **XML ID**: `SBFIZ_SBFM`

**Summary**: Signed bitfield insert in zeros

**Description**:
This instruction copies a bitfield of
<width> bits from the least significant bits of the source
register to bit position <lsb> of the destination
register, setting the destination bits below the bitfield to zero,
and the bits above the bitfield to a copy of the most significant
bit of the bitfield.

### Variant: `With sign replication to left and zeros to right (SBFIZ_SBFM_32M_bitfield)` (32-bit)
- **Condition**: `sf == 0 && N == 0`
- **Assembly**: `SBFIZ  <Wd>, <Wn>, #<lsb>, #<width>`
- **Fixed bits**: `sf`=`0`, `N`=`0`
- **Bit Pattern**: `??????????????????????0????????0`
- **Alias of**: `SBFM  <Wd>, <Wn>, #(-<lsb>  MOD  32), #(<width>-1)`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  00  100110 N   immr imms Rn  Rd  |
```

### Variant: `With sign replication to left and zeros to right (SBFIZ_SBFM_64M_bitfield)` (64-bit)
- **Condition**: `sf == 1 && N == 1`
- **Assembly**: `SBFIZ  <Xd>, <Xn>, #<lsb>, #<width>`
- **Fixed bits**: `sf`=`1`, `N`=`1`
- **Bit Pattern**: `??????????????????????1????????1`
- **Alias of**: `SBFM  <Xd>, <Xn>, #(-<lsb>  MOD  64), #(<width>-1)`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  00  100110 N   immr imms Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<lsb>` | `unknown` | `immr` | For the "32-bit" variant: is the bit number of the lsb of the destination bitfield, in the range 0 to 31. |
| `<lsb>` | `unknown` | `immr` | For the "64-bit" variant: is the bit number of the lsb of the destination bitfield, in the range 0 to 63. |
| `<width>` | `unknown` | `imms:immr` | For the "32-bit" variant: is the width of the bitfield, in the range 1 to 32-<lsb>. |
| `<width>` | `unknown` | `imms:immr` | For the "64-bit" variant: is the width of the bitfield, in the range 1 to 64-<lsb>. |
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

- alias_mnemonic: `SBFIZ`
- bitfield-fill: `signed-fill`
- isa: `A64`
- source: `sbfiz_sbfm.xml`
</details>