## EXTR `[ALIAS]`
_ARM A64 Instruction_ (Alias of extr.xml)

**Title**: ROR (immediate) -- A64 | **Class**: `general` | **XML ID**: `ROR_EXTR`

**Summary**: Rotate right (immediate)

**Description**:
This instruction provides the value of the contents of a
register rotated by a variable number of bits. The bits that are
rotated off the right end are inserted into the vacated bit
positions on the left.

### Variant: `Integer (ROR_EXTR_32_extract)` (32-bit)
- **Condition**: `sf == 0 && N == 0 && imms == 0xxxxx`
- **Assembly**: `ROR  <Wd>, <Ws>, #<shift>`
- **Fixed bits**: `sf`=`0`, `N`=`0`, `imms`=`0`
- **Bit Pattern**: `???????????????0??????0????????0`
- **Alias of**: `EXTR  <Wd>, <Ws>, <Ws>, #<shift>`
  Condition: Rn == Rm
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21 20  15   9   4  |
|-----------------------------|
| sf  00  100111 N   0   Rm  imms Rn  Rd  |
```

### Variant: `Integer (ROR_EXTR_64_extract)` (64-bit)
- **Condition**: `sf == 1 && N == 1`
- **Assembly**: `ROR  <Xd>, <Xs>, #<shift>`
- **Fixed bits**: `sf`=`1`, `N`=`1`
- **Bit Pattern**: `??????????????????????1????????1`
- **Alias of**: `EXTR  <Xd>, <Xs>, <Xs>, #<shift>`
  Condition: Rn == Rm
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21 20  15   9   4  |
|-----------------------------|
| sf  00  100111 N   0   Rm  imms Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Ws>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" and "Rm" fields. |
| `<shift>` | `shift` | `imms` | For the "32-bit" variant: is the amount by which to rotate, in the range 0 to 31, encoded in the "imms" field. |
| `<shift>` | `shift` | `imms` | For the "64-bit" variant: is the amount by which to rotate, in the range 0 to 63, encoded in the "imms" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xs>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register, encoded in the "Rn" and "Rm" fields. |

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

- alias_mnemonic: `ROR`
- isa: `A64`
- source: `ror_extr.xml`
</details>