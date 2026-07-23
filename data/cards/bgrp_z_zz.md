## BGRP
_ARM A64 Instruction_

**Title**: BGRP -- A64 | **Class**: `sve2` | **XML ID**: `bgrp_z_zz`

**Architecture**: `FEAT_SVE_BitPerm` (ARMv9.0)

**Summary**: Group bits to right or left as selected by bitmask

**Description**:
This instruction separates bits in each element of the first source vector by
gathering from the bit positions indicated by non-zero bits
in the corresponding mask element of the second source
vector to the lowest-numbered contiguous bits of the
corresponding destination element, and from positions
indicated by zero bits to the highest-numbered bits of the
destination element, preserving the bit order within each group.
This instruction is unpredicated.

ID_AA64ZFR0_EL1.BitPerm indicates whether this instruction is implemented.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is
implemented and enabled, or FEAT_SSVE_BitPerm is implemented.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_or_SSVE_BitPerm`

### Variant: `SVE2`
- **Assembly**: `BGRP  <Zd>.<T>, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  13  11   9   4  |
|-----------------------------------|
| 010 0010 1   size 0   Zm  10  11  10  Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_constructive.sve_intx_perm_bit.bgrp_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE_BitPerm) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_intx_constructive.sve_intx_perm_bit.bgrp_z_zz_)

```
if IsFeatureImplemented(FEAT_SSVE_BitPerm) then
    CheckSVEEnabled();
else
    CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) data = Z[n, VL];
constant bits(VL) mask = Z[m, VL];
bits(VL) result;

for e = 0 to elements - 1
    Elem[result, e, esize] = BitGroup(Elem[data, e, esize], Elem[mask, e, esize]);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_BitPerm)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

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

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bgrp_z_zz.xml`
</details>