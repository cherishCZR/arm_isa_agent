## SMADDL
_ARM A64 Instruction_

**Title**: SMADDL -- A64 | **Class**: `general` | **XML ID**: `SMADDL`

**Summary**: Signed multiply-add long

**Description**:
This instruction multiplies two 32-bit register values, adds a 64-bit
register value, and writes the result to the 64-bit destination register.

### Variant: `64-bit`
- **Assembly**: `SMADDL  <Xd>, <Wn>, <Wm>, <Xa>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28 27  24 23 22  20  15 14   9   4  |
|--------------------------------------|
| 1   00  1   101 1   0   01  Rm  0   Ra  Rn  Rd  |
```

#### Decode (A64.dpreg.dp_3src.SMADDL_64WA_dp_3src)

```
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer a = UInt(Ra);
```

#### Execute (A64.dpreg.dp_3src.SMADDL_64WA_dp_3src)

```
constant bits(32) operand1 = X[n, 32];
constant bits(32) operand2 = X[m, 32];
constant bits(64) operand3 = X[a, 64];

constant integer result = SInt(operand3) + (SInt(operand1) * SInt(operand2));

X[d, 64] = result<63:0>;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register holding the multiplicand, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register holding the multiplier, encoded in the "Rm" field. |
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

- datatype: `64`
- isa: `A64`
- source: `smaddl.xml`
</details>