## MADD
_ARM A64 Instruction_

**Title**: MADD -- A64 | **Class**: `general` | **XML ID**: `MADD`

**Summary**: Multiply-add

**Description**:
This instruction multiplies two register values, adds a third register value, and writes
the result to the destination register.

### Variant: `Integer (MADD_32A_dp_3src)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `MADD  <Wd>, <Wn>, <Wm>, <Wa>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  20  15 14   9   4  |
|-----------------------------|
| sf  00  11011 000 Rm  0   Ra  Rn  Rd  |
```

#### Decode (A64.dpreg.dp_3src.MADD_32A_dp_3src)

```
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer a = UInt(Ra);
constant integer datasize = 32 << UInt(sf);
```

#### Execute (A64.dpreg.dp_3src.MADD_32A_dp_3src)

```
constant bits(datasize) operand1 = X[n, datasize];
constant bits(datasize) operand2 = X[m, datasize];
constant bits(datasize) operand3 = X[a, datasize];

constant integer result = UInt(operand3) + (UInt(operand1) * UInt(operand2));

X[d, datasize] = result<datasize-1:0>;
```

### Variant: `Integer (MADD_64A_dp_3src)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `MADD  <Xd>, <Xn>, <Xm>, <Xa>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  20  15 14   9   4  |
|-----------------------------|
| sf  00  11011 000 Rm  0   Ra  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register holding the multiplicand, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register holding the multiplier, encoded in the "Rm" field. |
| `<Wa>` | `register (32-bit)` | `Ra` | Is the 32-bit name of the third general-purpose source register holding the addend, encoded in the "Ra" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register holding the multiplicand, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register holding the multiplier, encoded in the "Rm" field. |
| `<Xa>` | `register (64-bit)` | `Ra` | Is the 64-bit name of the third general-purpose source register holding the addend, encoded in the "Ra" field. |

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
- source: `madd.xml`
</details>