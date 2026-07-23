## SMIN
_ARM A64 Instruction_

**Title**: SMIN (immediate) -- A64 | **Class**: `general` | **XML ID**: `SMIN_imm`

**Architecture**: `FEAT_CSSC` (ARMv8.9)

**Summary**: Signed minimum (immediate)

**Description**:
This instruction determines the signed minimum of the source
register value and immediate, and writes the result to the destination
register.

### Variant: `Integer (SMIN_32_minmax_imm)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `SMIN  <Wd>, <Wn>, #<simm>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  21  17   9   4  |
|--------------------------|
| sf  0   0   1000111 0010 imm8 Rn  Rd  |
```

#### Decode (A64.dpimm.minmax_imm.SMIN_32_minmax_imm)

```
if !IsFeatureImplemented(FEAT_CSSC) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer datasize = 32 << UInt(sf);
constant integer imm = SInt(imm8);
```

#### Execute (A64.dpimm.minmax_imm.SMIN_32_minmax_imm)

```
constant bits(datasize) operand1 = X[n, datasize];
constant integer result = Min(SInt(operand1), imm);
X[d, datasize] = result<datasize-1:0>;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_CSSC)` |

### Variant: `Integer (SMIN_64_minmax_imm)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `SMIN  <Xd>, <Xn>, #<simm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  21  17   9   4  |
|--------------------------|
| sf  0   0   1000111 0010 imm8 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm8` | Is a signed immediate, in the range -128 to 127, encoded in the "imm8" field. |
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
- source: `smin_imm.xml`
</details>