## CFINV
_ARM A64 Instruction_

**Title**: CFINV -- A64 | **Class**: `system` | **XML ID**: `CFINV`

**Architecture**: `FEAT_FlagM` (ARMv8.4)

**Summary**: Invert carry flag

**Description**:
This instruction inverts the value of the PSTATE.C flag.

### Variant: `System`
- **Assembly**: `CFINV`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  18  15  11   7   4  |
|--------------------------|
| 110 101 0100000 000 0100 (0)(0)(0)(0) 000 11111 |
```

#### Decode (A64.control.pstate.CFINV_M_pstate)

```
if !IsFeatureImplemented(FEAT_FlagM) then EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.control.pstate.CFINV_M_pstate)

```
PSTATE.C = NOT(PSTATE.C);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FlagM)` |

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
- source: `cfinv.xml`
</details>