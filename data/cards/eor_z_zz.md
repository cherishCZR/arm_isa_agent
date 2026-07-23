## EOR
_ARM A64 Instruction_

**Title**: EOR (vectors, unpredicated) -- A64 | **Class**: `sve` | **XML ID**: `eor_z_zz`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Bitwise exclusive-OR vectors (unpredicated)

**Description**:
Bitwise exclusive-OR all elements of the second source vector with
corresponding elements of the first source vector
and place the results in the corresponding elements of the destination vector. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `EOR  <Zd>.D, <Zn>.D, <Zm>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   9   4  |
|--------------------------------|
| 000 0010 0   10  1   Zm  001 100 Zn  Zd  |
```

#### Decode (A64.sve.sve_int_unpred_logical.sve_int_bin_cons_log.eor_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_int_unpred_logical.sve_int_bin_cons_log.eor_z_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];

Z[d, VL] = operand1 EOR operand2;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

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
- source: `eor_z_zz.xml`
</details>