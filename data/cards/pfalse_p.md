## PFALSE
_ARM A64 Instruction_

**Title**: PFALSE -- A64 | **Class**: `sve` | **XML ID**: `pfalse_p`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Set all predicate elements to false

**Description**:
Set all elements in the destination predicate to false.

For programmer convenience, an assembler
      must also accept predicate-as-counter register name for the
      destination predicate register.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `PFALSE  <Pd>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21  19  15  13  10   8   4  3  |
|-----------------------------------------|
| 001 0010 1   0   0   01  1000 11  100 10  0000 0   Pd  |
```

#### Decode (A64.sve.sve_pred_gen_d.sve_int_pfalse.pfalse_p_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Pd);
```

#### Execute (A64.sve.sve_pred_gen_d.sve_int_pfalse.pfalse_p_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
P[d, PL] = Zeros(PL);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

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
- source: `pfalse_p.xml`
</details>