## MOVPRFX
_ARM A64 Instruction_

**Title**: MOVPRFX (unpredicated) -- A64 | **Class**: `sve` | **XML ID**: `movprfx_z_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move prefix (unpredicated)

**Description**:
The unpredicated MOVPRFX instruction is a hint to hardware that the instruction
may be combined with the destructive instruction which
follows it in program order to create a single constructive
operation.  Since it is a hint it is also
permitted to be implemented as a discrete vector copy, and
the result of executing the pair of instructions with or
without combining is identical. The choice of combined
versus discrete operation may vary dynamically.

Although the operation of the instruction is defined as a
simple unpredicated vector copy, it is required that the prefixed
instruction at PC+4 must be an SVE destructive
binary or ternary instruction encoding, or a unary operation with
merging predication, but excluding other MOVPRFX
instructions.
The prefixed instruction must specify
   the same destination vector as the MOVPRFX instruction.
The prefixed instruction must not use the
destination register in any other operand position,
even if they have different names but refer to the
same architectural register state.
Any other use is UNPREDICTABLE.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `MOVPRFX  <Zd>, <Zn>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  11   9   4  |
|--------------------------------|
| 000 0010 0   00  1   00000 1011 11  Zn  Zd  |
```

#### Decode (A64.sve.sve_int_unpred_misc.sve_int_bin_cons_misc_0_d.movprfx_z_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_int_unpred_misc.sve_int_bin_cons_misc_0_d.movprfx_z_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant bits(VL) result = Z[n, VL];
Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

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
- source: `movprfx_z_z.xml`
</details>