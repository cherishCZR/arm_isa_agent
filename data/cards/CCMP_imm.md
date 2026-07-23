## CCMP
_ARM A64 Instruction_

**Title**: CCMP (immediate) -- A64 | **Class**: `general` | **XML ID**: `CCMP_imm`

**Summary**: Conditional compare (immediate)

**Description**:
This instruction sets the value of the condition flags to
the result of the comparison of a register value and an immediate value
if the condition is TRUE, and an immediate value otherwise.

### Variant: `5-bit unsigned immediate (CCMP_32_condcmp_imm)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `CCMP  <Wn>, #<imm>, #<nzcv>, <cond>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  3  |
|-----------------------------------|
| sf  1   1   11010010 imm5 cond 1   0   Rn  0   nzcv |
```

#### Decode (A64.dpreg.condcmp_imm.CCMP_32_condcmp_imm)

```
constant integer n = UInt(Rn);
constant integer datasize = 32 << UInt(sf);
constant bits(4) condition = cond;
bits(4) flags = nzcv;
constant bits(datasize) imm = ZeroExtend(imm5, datasize);
```

#### Execute (A64.dpreg.condcmp_imm.CCMP_32_condcmp_imm)

```
if ConditionHolds(condition) then
    constant bits(datasize) operand1 = X[n, datasize];
    constant bits(datasize) operand2 = imm;
    (-, flags) = AddWithCarry(operand1, NOT(operand2), '1');
PSTATE.<N,Z,C,V> = flags;
```

### Variant: `5-bit unsigned immediate (CCMP_64_condcmp_imm)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `CCMP  <Xn>, #<imm>, #<nzcv>, <cond>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  3  |
|-----------------------------------|
| sf  1   1   11010010 imm5 cond 1   0   Rn  0   nzcv |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm5` | Is a five bit unsigned (positive) immediate encoded in the "imm5" field. |
| `<nzcv>` | `unknown` | `nzcv` | Is the flag bit specifier, an immediate in the range 0 to 15, giving the alternative state for the 4-bit NZCV condition flags, encoded in the "nzcv" f |
| `<cond>` | `condition` | `cond` | Is one of the standard conditions, encoded in the standard way, and |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register, encoded in the "Rn" field. |

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

- immediate-type: `imm5u`
- isa: `A64`
- source: `ccmp_imm.xml`
</details>