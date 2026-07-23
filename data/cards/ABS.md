## ABS
_ARM A64 Instruction_

**Title**: ABS -- A64 | **Class**: `general` | **XML ID**: `ABS`

**Architecture**: `FEAT_CSSC` (ARMv8.9)

**Summary**: Absolute value

**Description**:
This instruction computes the absolute value of the signed integer value
in the source register, and writes the result to the destination register.

### Variant: `Integer (ABS_32_dp_1src)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `ABS  <Wd>, <Wn>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15   9   4  |
|--------------------------|
| sf  1   0   11010110 00000 001000 Rn  Rd  |
```

#### Decode (A64.dpreg.dp_1src.ABS_32_dp_1src)

```
if !IsFeatureImplemented(FEAT_CSSC) then EndOfDecode(Decode_UNDEF);
constant integer datasize = 32 << UInt(sf);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
```

#### Execute (A64.dpreg.dp_1src.ABS_32_dp_1src)

```
constant bits(datasize) operand1 = X[n, datasize];
constant integer result = Abs(SInt(operand1));
X[d, datasize] = result<datasize-1:0>;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_CSSC)` |

### Variant: `Integer (ABS_64_dp_1src)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `ABS  <Xd>, <Xn>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15   9   4  |
|--------------------------|
| sf  1   0   11010110 00000 001000 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register, encoded in the "Rn" field. |

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
- source: `abs.xml`
</details>