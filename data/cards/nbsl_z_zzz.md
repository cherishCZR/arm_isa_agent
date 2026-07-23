## NBSL
_ARM A64 Instruction_

**Title**: NBSL -- A64 | **Class**: `sve2` | **XML ID**: `nbsl_z_zzz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Bitwise inverted select

**Description**:
Selects bits from the  first source vector where the
corresponding bit in the third source vector is '1', and from
the  second source vector where the corresponding bit in the
third source vector is '0'. The inverted result is placed
destructively in the destination and first source vector.
This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `NBSL  <Zdn>.D, <Zdn>.D, <Zm>.D, <Zk>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12  10  9   4  |
|-----------------------------------|
| 000 0010 0   11  1   Zm  001 11  1   Zk  Zdn |
```

#### Decode (A64.sve.sve_int_unpred_logical.sve_int_tern_log.nbsl_z_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer m = UInt(Zm);
constant integer k = UInt(Zk);
constant integer dn = UInt(Zdn);
```

#### Execute (A64.sve.sve_int_unpred_logical.sve_int_tern_log.nbsl_z_zzz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant bits(VL) operand1 = Z[dn, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[k, VL];

Z[dn, VL] = NOT((operand1 AND operand3) OR (operand2 AND NOT(operand3)));
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
- source: `nbsl_z_zzz.xml`
</details>