## SETFFR
_ARM A64 Instruction_

**Title**: SETFFR -- A64 | **Class**: `sve` | **XML ID**: `setffr_f`

**Architecture**: `FEAT_SVE` (PROFILE_A)

**Summary**: Initialise the first-fault register to all true

**Description**:
Initialise the first-fault register (FFR) to all true
prior to a sequence of first-fault or non-fault loads.  This instruction is unpredicated.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_only`

### Variant: `SVE`
- **Assembly**: `SETFFR`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17  15  11   8   4  |
|-----------------------------------|
| 001 0010 1   00  101 1   00  1001 000 0000 00000 |
```

#### Decode (A64.sve.sve_pred_wrffr.sve_int_setffr.setffr_f_)

```
if !IsFeatureImplemented(FEAT_SVE) then EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.sve.sve_pred_wrffr.sve_int_setffr.setffr_f_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
FFR[PL] = Ones(PL);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE)` |

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
- source: `setffr_f.xml`
</details>