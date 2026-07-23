## BFM `[ALIAS]`
_ARM A64 Instruction_ (Alias of bfm.xml)

**Title**: BFC -- A64 | **Class**: `general` | **XML ID**: `BFC_BFM`

**Architecture**: `FEAT_ASMv8p2` (ARMv8.2)

**Summary**: Bitfield clear

**Description**:
This instruction sets a bitfield of <width> bits at bit
position <lsb> of the destination register to zero,
leaving the other destination bits unchanged.

### Variant: `Leaving other bits unchanged (BFC_BFM_32M_bitfield)` (32-bit)
- **Condition**: `sf == 0 && N == 0`
- **Assembly**: `BFC  <Wd>, #<lsb>, #<width>`
- **Fixed bits**: `sf`=`0`, `N`=`0`
- **Bit Pattern**: `??????????????????????0????????0`
- **Alias of**: `BFM  <Wd>, WZR, #(-<lsb>  MOD  32), #(<width>-1)`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  01  100110 N   immr imms 11111 Rd  |
```

### Variant: `Leaving other bits unchanged (BFC_BFM_64M_bitfield)` (64-bit)
- **Condition**: `sf == 1 && N == 1`
- **Assembly**: `BFC  <Xd>, #<lsb>, #<width>`
- **Fixed bits**: `sf`=`1`, `N`=`1`
- **Bit Pattern**: `??????????????????????1????????1`
- **Alias of**: `BFM  <Xd>, XZR, #(-<lsb>  MOD  64), #(<width>-1)`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  01  100110 N   immr imms 11111 Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<lsb>` | `unknown` | `immr` | For the "32-bit" variant: is the bit number of the lsb of the destination bitfield, in the range 0 to 31. |
| `<lsb>` | `unknown` | `immr` | For the "64-bit" variant: is the bit number of the lsb of the destination bitfield, in the range 0 to 63. |
| `<width>` | `unknown` | `imms:immr` | For the "32-bit" variant: is the width of the bitfield, in the range 1 to 32-<lsb>. |
| `<width>` | `unknown` | `imms:immr` | For the "64-bit" variant: is the width of the bitfield, in the range 1 to 64-<lsb>. |
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

- alias_mnemonic: `BFC`
- bitfield-fill: `nofill`
- isa: `A64`
- source: `bfc_bfm.xml`
</details>