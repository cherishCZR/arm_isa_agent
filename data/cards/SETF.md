## SETF
_ARM A64 Instruction_

**Title**: SETF8, SETF16 -- A64 | **Class**: `general` | **XML ID**: `SETF`

**Architecture**: `FEAT_FlagM` (ARMv8.4)

**Summary**: Evaluation of 8-bit or 16-bit flag values

**Description**:
This instruction sets the PSTATE.NZV flags based on the value in the specified
general-purpose register. SETF8 treats the value as an 8-bit
value. SETF16 treats the value as a 16-bit value.

The PSTATE.C flag is not affected by these instructions.

### Variant: `Integer (SETF8_only_setf)` (SETF8)
- **Condition**: `sz == 0`
- **Assembly**: `SETF8  <Wn>`
- **Fixed bits**: `sz`=`0`
- **Bit Pattern**: `??????????????0?????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  14 13   9   4  3  |
|--------------------------------|
| 0   0   1   11010000 000000 sz  0010 Rn  0   1101 |
```

#### Decode (A64.dpreg.setf.SETF8_only_setf)

```
if !IsFeatureImplemented(FEAT_FlagM) then EndOfDecode(Decode_UNDEF);
constant integer size = 8 << UInt(sz);
constant integer n = UInt(Rn);
```

#### Execute (A64.dpreg.setf.SETF8_only_setf)

```
constant bits(32) reg = X[n, 32];
PSTATE.N = reg<size-1>;
PSTATE.Z = if (reg<size-1:0> == Zeros(size)) then '1' else '0';
PSTATE.V = reg<size> EOR reg<size-1>;
//PSTATE.C unchanged;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FlagM)` |

### Variant: `Integer (SETF16_only_setf)` (SETF16)
- **Condition**: `sz == 1`
- **Assembly**: `SETF16  <Wn>`
- **Fixed bits**: `sz`=`1`
- **Bit Pattern**: `??????????????1?????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  14 13   9   4  3  |
|--------------------------------|
| 0   0   1   11010000 000000 sz  0010 Rn  0   1101 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |

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
- source: `setf.xml`
</details>