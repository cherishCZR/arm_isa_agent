## UMULH
_ARM A64 Instruction_

**Title**: UMULH -- A64 | **Class**: `general` | **XML ID**: `UMULH`

**Summary**: Unsigned multiply high

**Description**:
This instruction multiplies two 64-bit register values, and writes
bits[127:64] of the 128-bit result to the 64-bit destination register.

### Variant: `64-bit`
- **Assembly**: `UMULH  <Xd>, <Xn>, <Xm>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28 27  24 23 22  20  15 14   9   4  |
|--------------------------------------|
| 1   00  1   101 1   1   10  Rm  0   (1)(1)(1)(1)(1) Rn  Rd  |
```

#### Decode (A64.dpreg.dp_3src.UMULH_64_dp_3src)

```
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.dpreg.dp_3src.UMULH_64_dp_3src)

```
constant bits(64) operand1 = X[n, 64];
constant bits(64) operand2 = X[m, 64];

constant integer result = UInt(operand1) * UInt(operand2);

X[d, 64] = result<127:64>;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register holding the multiplicand, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register holding the multiplier, encoded in the "Rm" field. |

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

- datatype: `64`
- isa: `A64`
- source: `umulh.xml`
</details>