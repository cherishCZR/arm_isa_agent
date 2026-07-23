## INSR
_ARM A64 Instruction_

**Title**: INSR (SIMD&FP scalar) -- A64 | **Class**: `sve` | **XML ID**: `insr_z_v`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Insert SIMD&FP scalar register in shifted vector

**Description**:
Shift the destination vector left by one element,
and then place a copy of the SIMD&FP scalar
register in element 0 of the destination vector.
This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `INSR  <Zdn>.<T>, <V><m>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15   9   4  |
|--------------------------------|
| 000 0010 1   size 1   10  100 001110 Vm  Zdn |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_perm_insrv.insr_z_v_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer dn = UInt(Zdn);
constant integer m = UInt(Vm);
```

#### Execute (A64.sve.sve_perm_unpred_d.sve_int_perm_insrv.insr_z_v_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant bits(VL) dest = Z[dn, VL];
constant bits(esize) src = V[m, esize];
Z[dn, VL] = dest<(VL-esize)-1:0> : src;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the source and destination scalable vector register, encoded in the "Zdn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<V>` | `register (128-bit)` | `size` | Is a width specifier, |
| `<m>` | `unknown` | `Vm` | Is the number [0-31] of the source SIMD&FP register, encoded in the "Vm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

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
- source: `insr_z_v.xml`
</details>