## UMAX
_ARM A64 Instruction_

**Title**: UMAX (register) -- A64 | **Class**: `general` | **XML ID**: `UMAX_reg`

**Architecture**: `FEAT_CSSC` (ARMv8.9)

**Summary**: Unsigned maximum (register)

**Description**:
This instruction determines the unsigned maximum of the two source
register values and writes the result to the destination register.

### Variant: `Integer (UMAX_32_dp_2src)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `UMAX  <Wd>, <Wn>, <Wm>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15   9   4  |
|--------------------------|
| sf  0   0   11010110 Rm  011001 Rn  Rd  |
```

#### Decode (A64.dpreg.dp_2src.UMAX_32_dp_2src)

```
if !IsFeatureImplemented(FEAT_CSSC) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 32 << UInt(sf);
```

#### Execute (A64.dpreg.dp_2src.UMAX_32_dp_2src)

```
constant bits(datasize) operand1 = X[n, datasize];
constant bits(datasize) operand2 = X[m, datasize];
constant integer result = Max(UInt(operand1), UInt(operand2));
X[d, datasize] = result<datasize-1:0>;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_CSSC)` |

### Variant: `Integer (UMAX_64_dp_2src)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `UMAX  <Xd>, <Xn>, <Xm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15   9   4  |
|--------------------------|
| sf  0   0   11010110 Rm  011001 Rn  Rd  |
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

- isa: `A64`
- source: `umax_reg.xml`
</details>