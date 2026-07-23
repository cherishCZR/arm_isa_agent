## INSR
_ARM A64 Instruction_

**Title**: INSR (scalar) -- A64 | **Class**: `sve` | **XML ID**: `insr_z_r`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Insert general-purpose register in shifted vector

**Description**:
Shift the destination vector left by one element,
and then place a copy of the least-significant
bits of the general-purpose register in element 0 of the
destination vector.  This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `INSR  <Zdn>.<T>, <R><m>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15   9   4  |
|--------------------------------|
| 000 0010 1   size 1   00  100 001110 Rm  Zdn |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_perm_insrs.insr_z_r_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer dn = UInt(Zdn);
constant integer m = UInt(Rm);
```

#### Execute (A64.sve.sve_perm_unpred_d.sve_int_perm_insrs.insr_z_r_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant bits(VL) dest = Z[dn, VL];
constant bits(esize) src = X[m, esize];
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
| `<R>` | `unknown` | `size` | Is a width specifier, |
| `<m>` | `unknown` | `Rm` | Is the number [0-30] of the source general-purpose register or the name ZR (31), encoded in the "Rm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | W |
| 01 | W |
| 10 | W |
| 11 | X |

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
- source: `insr_z_r.xml`
</details>