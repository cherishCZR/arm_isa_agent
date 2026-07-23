## RDFFR
_ARM A64 Instruction_

**Title**: RDFFR (predicated) -- A64 | **Class**: `sve` | **XML ID**: `rdffr_p_p_f`

**Architecture**: `FEAT_SVE` (PROFILE_A)

**Summary**: Return predicate of succesfully loaded elements

**Description**:
Read the first-fault register (FFR) and place active
elements in the corresponding elements of the destination
predicate. Inactive elements in the destination predicate register are set to zero. Does not set the condition flags.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_only`

### Variant: `Not setting the condition flags`
- **Assembly**: `RDFFR  <Pd>.B, <Pg>/Z`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21  19  15  13  10   8   4  3  |
|-----------------------------------------|
| 001 0010 1   0   0   01  1000 11  110 00  Pg  0   Pd  |
```

#### Decode (A64.sve.sve_pred_gen_d.sve_int_rdffr.rdffr_p_p_f_)

```
if !IsFeatureImplemented(FEAT_SVE) then EndOfDecode(Decode_UNDEF);
constant integer g = UInt(Pg);
constant integer d = UInt(Pd);
constant boolean setflags = FALSE;
```

#### Execute (A64.sve.sve_pred_gen_d.sve_int_rdffr.rdffr_p_p_f_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant bits(PL) mask = P[g, PL];
constant bits(PL) ffr = FFR[PL];
constant bits(PL) result = ffr AND mask;

if setflags then
    PSTATE.<N,Z,C,V> = PredTest(mask, result, 8);
P[d, PL] = result;
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
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register, encoded in the "Pg" field. |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- cond-setting: `no-s`
- isa: `A64`
- source: `rdffr_p_p_f.xml`
</details>