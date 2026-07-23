## CCMN
_ARM A64 Instruction_

**Title**: CCMN (register) -- A64 | **Class**: `general` | **XML ID**: `CCMN_reg`

**Summary**: Conditional compare negative (register)

**Description**:
This instruction sets the value of the condition flags to
the result of the comparison of a register value and the inverse of another
register value if the condition is TRUE, and an immediate value otherwise.

### Variant: `Integer (CCMN_32_condcmp_reg)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `CCMN  <Wn>, <Wm>, #<nzcv>, <cond>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  3  |
|-----------------------------------|
| sf  0   1   11010010 Rm  cond 0   0   Rn  0   nzcv |
```

#### Decode (A64.dpreg.condcmp_reg.CCMN_32_condcmp_reg)

```
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 32 << UInt(sf);
constant bits(4) condition = cond;
bits(4) flags = nzcv;
```

#### Execute (A64.dpreg.condcmp_reg.CCMN_32_condcmp_reg)

```
if ConditionHolds(condition) then
    constant bits(datasize) operand1 = X[n, datasize];
    constant bits(datasize) operand2 = X[m, datasize];
    (-, flags) = AddWithCarry(operand1, operand2, '0');
PSTATE.<N,Z,C,V> = flags;
```

### Variant: `Integer (CCMN_64_condcmp_reg)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `CCMN  <Xn>, <Xm>, #<nzcv>, <cond>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  3  |
|-----------------------------------|
| sf  0   1   11010010 Rm  cond 0   0   Rn  0   nzcv |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<nzcv>` | `unknown` | `nzcv` | Is the flag bit specifier, an immediate in the range 0 to 15, giving the alternative state for the 4-bit NZCV condition flags, encoded in the "nzcv" f |
| `<cond>` | `condition` | `cond` | Is one of the standard conditions, encoded in the standard way, and |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register, encoded in the "Rm" field. |

**<cond> Value Table**:

| bitfield | symbol |
|---|---|
| 0000 | EQ |
| 0001 | NE |
| 0010 | CS |
| 0011 | CC |
| 0100 | MI |
| 0101 | PL |
| 0110 | VS |
| 0111 | VC |
| 1000 | HI |
| 1001 | LS |
| 1010 | GE |
| 1011 | LT |
| 1100 | GT |
| 1101 | LE |
| 1110 | AL |
| 1111 | NV |

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

- isa: `A64`
- source: `ccmn_reg.xml`
</details>