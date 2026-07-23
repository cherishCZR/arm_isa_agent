## BCAX
_ARM A64 Instruction_

**Title**: BCAX -- A64 | **Class**: `sve2` | **XML ID**: `bcax_z_zzz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Bitwise clear and exclusive-OR

**Description**:
Bitwise AND elements of the second source vector with the
corresponding inverted elements of the third source vector,
then exclusive-OR the results with corresponding elements of
the first source vector. The final results are destructively
placed in the corresponding elements of the destination and
first source vector. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `BCAX  <Zdn>.D, <Zdn>.D, <Zm>.D, <Zk>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12  10  9   4  |
|-----------------------------------|
| 000 0010 0   01  1   Zm  001 11  0   Zk  Zdn |
```

#### Decode (A64.sve.sve_int_unpred_logical.sve_int_tern_log.bcax_z_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer m = UInt(Zm);
constant integer k = UInt(Zk);
constant integer dn = UInt(Zdn);
```

#### Execute (A64.sve.sve_int_unpred_logical.sve_int_tern_log.bcax_z_zzz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant bits(VL) operand1 = Z[dn, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[k, VL];

Z[dn, VL] = operand1 EOR (operand2 AND NOT(operand3));
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the first source and destination scalable vector register, encoded in the "Zdn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<Zk>` | `register (128-bit)` | `Zk` | Is the name of the third source scalable vector register, encoded in the "Zk" field. |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bcax_z_zzz.xml`
</details>