## CSINC
_ARM A64 Instruction_

**Title**: CSINC -- A64 | **Class**: `general` | **XML ID**: `CSINC`

**Summary**: Conditional select increment

**Description**:
This instruction returns, in the destination register,
the value of the first source register if the condition is TRUE, and
otherwise returns the value of the second source register incremented by 1.

### Variant: `Integer (CSINC_32_condsel)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `CSINC  <Wd>, <Wn>, <Wm>, <cond>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  |
|--------------------------------|
| sf  0   0   11010100 Rm  cond 0   1   Rn  Rd  |
```

#### Decode (A64.dpreg.condsel.CSINC_32_condsel)

```
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 32 << UInt(sf);
constant bits(4) condition = cond;
```

#### Execute (A64.dpreg.condsel.CSINC_32_condsel)

```
bits(datasize) result;
if ConditionHolds(condition) then
    result = X[n, datasize];
else
    result = X[m, datasize] + 1;

X[d, datasize] = result;
```

### Variant: `Integer (CSINC_64_condsel)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `CSINC  <Xd>, <Xn>, <Xm>, <cond>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  |
|--------------------------------|
| sf  0   0   11010100 Rm  cond 0   1   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<cond>` | `condition` | `cond` | Is one of the standard conditions, encoded in the standard way, and |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
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
- source: `csinc.xml`
</details>