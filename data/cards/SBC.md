## SBC
_ARM A64 Instruction_

**Title**: SBC -- A64 | **Class**: `general` | **XML ID**: `SBC`

**Summary**: Subtract with carry

**Description**:
This instruction subtracts a register value
and the value of NOT (Carry flag) from a register value,
and writes the result to the destination register.

### Variant: `Not setting the condition flags (SBC_32_addsub_carry)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `SBC  <Wd>, <Wn>, <Wm>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15   9   4  |
|--------------------------|
| sf  1   0   11010000 Rm  000000 Rn  Rd  |
```

#### Decode (A64.dpreg.addsub_carry.SBC_32_addsub_carry)

```
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 32 << UInt(sf);
```

#### Execute (A64.dpreg.addsub_carry.SBC_32_addsub_carry)

```
constant bits(datasize) operand1 = X[n, datasize];
constant bits(datasize) operand2 = NOT(X[m, datasize]);
bits(datasize) result;

(result, -) = AddWithCarry(operand1, operand2, PSTATE.C);

X[d, datasize] = result;
```

### Variant: `Not setting the condition flags (SBC_64_addsub_carry)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `SBC  <Xd>, <Xn>, <Xm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15   9   4  |
|--------------------------|
| sf  1   0   11010000 Rm  000000 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register, encoded in the "Rm" field. |

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

- cond-setting: `no-s`
- isa: `A64`
- source: `sbc.xml`
</details>