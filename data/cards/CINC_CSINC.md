## CSINC `[ALIAS]`
_ARM A64 Instruction_ (Alias of csinc.xml)

**Title**: CINC -- A64 | **Class**: `general` | **XML ID**: `CINC_CSINC`

**Summary**: Conditional increment

**Description**:
This instruction returns, in the destination register,
the value of the source register incremented by 1 if the
condition is TRUE, and otherwise returns the value of the
source register.

### Variant: `Integer (CINC_CSINC_32_condsel)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `CINC  <Wd>, <Wn>, <invcond>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `CSINC  <Wd>, <Wn>, <Wm>, <cond>`
  Condition: Rn == Rm
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  |
|--------------------------------|
| sf  0   0   11010100 ?   ?   0   1   ?   Rd  |
```

### Variant: `Integer (CINC_CSINC_64_condsel)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `CINC  <Xd>, <Xn>, <invcond>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `CSINC  <Xd>, <Xn>, <Xm>, <cond>`
  Condition: Rn == Rm
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  |
|--------------------------------|
| sf  0   0   11010100 ?   ?   0   1   ?   Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" and "Rm" fields. |
| `<invcond>` | `unknown` | `cond` | Is one of the standard conditions, excluding AL and NV, encoded with its least significant bit inverted, and |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register, encoded in the "Rn" and "Rm" fields. |

**<invcond> Value Table**:

| bitfield | symbol |
|---|---|
| 0000 |  |
| 0001 |  |
| 0010 |  |
| 0011 |  |
| 0100 |  |
| 0101 |  |
| 0110 |  |
| 0111 |  |
| 1000 |  |
| 1001 |  |
| 1010 |  |
| 1011 |  |
| 1100 |  |
| 1101 |  |

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

- alias_mnemonic: `CINC`
- isa: `A64`
- source: `cinc_csinc.xml`
</details>