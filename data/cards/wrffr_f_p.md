## WRFFR
_ARM A64 Instruction_

**Title**: WRFFR -- A64 | **Class**: `sve` | **XML ID**: `wrffr_f_p`

**Architecture**: `FEAT_SVE` (PROFILE_A)

**Summary**: Write the first-fault register

**Description**:
Read the source predicate register and place in the
first-fault register (FFR). This instruction is intended
to restore a saved FFR and is not recommended for general
use by applications.

This instruction requires that the source predicate contains a
monotonic predicate value, in which starting from bit 0
there are zero or more 1 bits, followed only by
0 bits in any remaining bit positions. If the source
is not a monotonic predicate value, then the resulting value
in the FFR will be UNPREDICTABLE. It is not possible to
generate a non-monotonic value in FFR when using
SETFFR followed by first-fault or non-fault loads.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_only`

### Variant: `SVE`
- **Assembly**: `WRFFR  <Pn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17  15  11   8   4  |
|-----------------------------------|
| 001 0010 1   00  101 0   00  1001 000 Pn  00000 |
```

#### Decode (A64.sve.sve_pred_wrffr.sve_int_wrffr.wrffr_f_p_)

```
if !IsFeatureImplemented(FEAT_SVE) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Pn);
```

#### Execute (A64.sve.sve_pred_wrffr.sve_int_wrffr.wrffr_f_p_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant bits(PL) operand = P[n, PL];

constant integer hsb = HighestSetBit(operand);
if hsb < 0 || IsOnes(operand<hsb:0>) then
    FFR[PL] = operand;
else // not a monotonic predicate
    FFR[PL] = bits(PL) UNKNOWN;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pn>` | `unknown` | `Pn` | Is the name of the source scalable predicate register, encoded in the "Pn" field. |

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
- source: `wrffr_f_p.xml`
</details>