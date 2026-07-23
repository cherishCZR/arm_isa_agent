## CSNEG `[ALIAS]`
_ARM A64 Instruction_ (Alias of csneg.xml)

**Title**: CNEG -- A64 | **Class**: `general` | **XML ID**: `CNEG_CSNEG`

**Summary**: Conditional negate

**Description**:
This instruction returns, in the destination register,
the negated value of the source register if the condition is
TRUE, and otherwise returns the value of the source register.

### Variant: `Integer (CNEG_CSNEG_32_condsel)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `CNEG  <Wd>, <Wn>, <invcond>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `CSNEG  <Wd>, <Wn>, <Wm>, <cond>`
  Condition: Rn == Rm
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  |
|--------------------------------|
| sf  1   0   11010100 Rm  ?   0   1   Rn  Rd  |
```

### Variant: `Integer (CNEG_CSNEG_64_condsel)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `CNEG  <Xd>, <Xn>, <invcond>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `CSNEG  <Xd>, <Xn>, <Xm>, <cond>`
  Condition: Rn == Rm
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  |
|--------------------------------|
| sf  1   0   11010100 Rm  ?   0   1   Rn  Rd  |
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

- alias_mnemonic: `CNEG`
- isa: `A64`
- source: `cneg_csneg.xml`
</details>