## RMIF
_ARM A64 Instruction_

**Title**: RMIF -- A64 | **Class**: `general` | **XML ID**: `RMIF`

**Architecture**: `FEAT_FlagM` (ARMv8.4)

**Summary**: Rotate, mask insert flags

**Description**:
This instruction performs a rotation right of a value held in a
general-purpose register by an immediate value, and then inserts a
selection of the bottom four bits of the result of the rotation
into the PSTATE flags, under the control of a second immediate mask.

### Variant: `Integer`
- **Assembly**: `RMIF  <Xn>, #<shift>, #<mask>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  14   9   4  3  |
|-----------------------------------|
| 1   0   1   1   101 0000 imm6 00001 Rn  0   mask |
```

#### Decode (A64.dpreg.rmif.RMIF_only_rmif)

```
if !IsFeatureImplemented(FEAT_FlagM) then EndOfDecode(Decode_UNDEF);
constant integer imm = UInt(imm6);
constant bits(4) flagmask = mask;
constant integer n = UInt(Rn);
```

#### Execute (A64.dpreg.rmif.RMIF_only_rmif)

```
constant bits(64) reg = X[n, 64];
constant bits(4) flags = (reg:reg)<imm+3:imm>;
if flagmask<3> == '1' then PSTATE.N = flags<3>;
if flagmask<2> == '1' then PSTATE.Z = flags<2>;
if flagmask<1> == '1' then PSTATE.C = flags<1>;
if flagmask<0> == '1' then PSTATE.V = flags<0>;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FlagM)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<shift>` | `shift` | `imm6` | Is the shift amount, in the range 0 to 63, defaulting to 0 and encoded in the "imm6" field. |
| `<mask>` | `unknown` | `mask` | Is the flag bit mask, an immediate in the range 0 to 15, which selects the bits that are inserted into the NZCV condition flags, encoded in the "mask" |

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
- source: `rmif.xml`
</details>