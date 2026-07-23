## DUPM
_ARM A64 Instruction_

**Title**: DUPM -- A64 | **Class**: `sve` | **XML ID**: `dupm_z_i`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Broadcast logical bitmask immediate to vector (unpredicated)

**Description**:
Unconditionally broadcast the logical bitmask immediate into each element of the
destination vector. This instruction is unpredicated.
The immediate is a 64-bit value consisting of a single run of ones or zeros
repeating every 2, 4, 8, 16, 32 or 64 bits.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `DUPM  <Zd>.<T>, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  19  17   4  |
|--------------------------|
| 000 0010 1   11  00  00  imm13 Zd  |
```

#### Decode (A64.sve.sve_maskimm.sve_int_dup_mask_imm.dupm_z_i_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer d = UInt(Zd);
bits(esize) imm;
(imm, -) = DecodeBitMasks(imm13<12>, imm13<5:0>, imm13<11:6>, TRUE, esize);
```

#### Execute (A64.sve.sve_maskimm.sve_int_dup_mask_imm.dupm_z_i_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant bits(VL) result = Replicate(imm, VL DIV esize);
Z[d, VL] = result;
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
| `<T>` | `unknown` | `imm13` | Is the size specifier, |
| `<const>` | `unknown` | `imm13` | Is a 64, 32, 16 or 8-bit bitmask consisting of replicated 2, 4, 8, 16, 32 or 64 bit fields, each field containing a rotated run of non-zero bits, enco |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0xxxxxx0xxxxx | S |
| 0xxxxxx10xxxx | H |
| 0xxxxxx110xxx | B |
| 0xxxxxx1110xx | B |
| 0xxxxxx11110x | B |
| 0xxxxxx11111x | RESERVED |
| 1xxxxxxxxxxxx | D |

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
- source: `dupm_z_i.xml`
</details>