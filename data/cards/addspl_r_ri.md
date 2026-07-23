## ADDSPL
_ARM A64 Instruction_

**Title**: ADDSPL -- A64 | **Class**: `mortlach` | **XML ID**: `addspl_r_ri`

**Architecture**: `FEAT_SME` (PROFILE_A)

**Summary**: Add multiple of Streaming SVE predicate register size to scalar register

**Description**:
This instruction adds the Streaming SVE predicate register size in bytes multiplied
by an immediate in the range -32 to 31 to the
64-bit source general-purpose register or current stack
pointer and places the result in the 64-bit destination
general-purpose register or current stack pointer.

This instruction does not require the PE to be in Streaming SVE mode.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SME`
- **Assembly**: `ADDSPL  <Xd|SP>, <Xn|SP>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  15  11 10   4  |
|-----------------------------------|
| 000 0010 0   0   1   1   Rn  0101 1   imm6 Rd  |
```

#### Decode (A64.sve.sve_alloca.sve_int_arith_svl.addspl_r_ri_)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Rn);
constant integer d = UInt(Rd);
constant integer imm = SInt(imm6);
```

#### Execute (A64.sve.sve_alloca.sve_int_arith_svl.addspl_r_ri_)

```
CheckSMEEnabled();
constant integer SVL = CurrentSVL;
constant integer len = imm * (SVL DIV 64);
constant bits(64) operand1 = if n == 31 then SP[64] else X[n, 64];
constant bits(64) result = operand1 + len;

if d == 31 then
    SP[64] = result;
else
    X[d, 64] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd\|SP>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register or stack pointer, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the source general-purpose register or stack pointer, encoded in the "Rn" field. |
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
- source: `addspl_r_ri.xml`
</details>