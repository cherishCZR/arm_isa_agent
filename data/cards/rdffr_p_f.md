## RDFFR
_ARM A64 Instruction_

**Title**: RDFFR (unpredicated) -- A64 | **Class**: `sve` | **XML ID**: `rdffr_p_f`

**Architecture**: `FEAT_SVE` (PROFILE_A)

**Summary**: Read the first-fault register

**Description**:
Read the first-fault register (FFR) and place in the
destination predicate without predication.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_only`

### Variant: `SVE`
- **Assembly**: `RDFFR  <Pd>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21  19  15  13  10   8   4  3  |
|-----------------------------------------|
| 001 0010 1   0   0   01  1001 11  110 00  0000 0   Pd  |
```

#### Decode (A64.sve.sve_pred_gen_d.sve_int_rdffr_2.rdffr_p_f_)

```
if !IsFeatureImplemented(FEAT_SVE) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Pd);
```

#### Execute (A64.sve.sve_pred_gen_d.sve_int_rdffr_2.rdffr_p_f_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant bits(PL) ffr = FFR[PL];
P[d, PL] = ffr;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |

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
- source: `rdffr_p_f.xml`
</details>