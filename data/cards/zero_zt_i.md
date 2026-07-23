## ZERO
_ARM A64 Instruction_

**Title**: ZERO (table) -- A64 | **Class**: `mortlach2` | **XML ID**: `zero_zt_i`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Zero ZT0

**Description**:
This instruction zeroes all bytes of the ZT0 register.

This instruction does not require the PE to be in Streaming SVE mode,
and it is expected that this instruction will not experience a significant slowdown
due to contention with other PEs that are executing in Streaming SVE mode.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_or_1`

### Variant: `SME2`
- **Assembly**: `ZERO  { ZT0 }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  17   3  |
|--------------------|
| 1   10  0000 0010010 00000000000000 0001 |
```

#### Decode (A64.sme.mortlach_zero_zt.zero_zt_i_)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.sme.mortlach_zero_zt.zero_zt_i_)

```
CheckSMEEnabled();
CheckSMEZT0Enabled();

if IsFeatureImplemented(FEAT_TME) && TSTATE.depth > 0 then
    FailTransaction(TMFailure_ERR, FALSE);

ZT0[512] = Zeros(512);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

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
- source: `zero_zt_i.xml`
</details>