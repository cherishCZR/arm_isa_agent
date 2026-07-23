## RDSVL
_ARM A64 Instruction_

**Title**: RDSVL -- A64 | **Class**: `mortlach` | **XML ID**: `rdsvl_r_i`

**Architecture**: `FEAT_SME` (PROFILE_A)

**Summary**: Read multiple of Streaming SVE vector register size to scalar register

**Description**:
This instruction multiplies the Streaming SVE vector register size in bytes by an
immediate in the range -32 to 31 and places the
result in the 64-bit destination general-purpose register.

This instruction does not require the PE to be in Streaming SVE mode.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SME`
- **Assembly**: `RDSVL  <Xd>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  15  11 10   4  |
|-----------------------------------|
| 000 0010 0   1   0   1   11111 0101 1   imm6 Rd  |
```

#### Decode (A64.sve.sve_alloca.sve_int_read_svl_a.rdsvl_r_i_)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer imm = SInt(imm6);
```

#### Execute (A64.sve.sve_alloca.sve_int_read_svl_a.rdsvl_r_i_)

```
CheckSMEEnabled();
constant integer SVL = CurrentSVL;
constant integer len = imm * (SVL DIV 8);
X[d, 64] = len<63:0>;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register, encoded in the "Rd" field. |
| `<imm>` | `immediate` | `imm6` | Is the signed immediate operand, in the range -32 to 31, encoded in the "imm6" field. |

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
- source: `rdsvl_r_i.xml`
</details>