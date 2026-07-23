## EXT
_ARM A64 Instruction_

**Title**: EXT -- A64 | **Class**: `sve` | **XML ID**: `ext_z_zi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME), `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Extract vector from pair of vectors

**Description**:
Copy the indexed byte up to the last byte of the first source
vector to the bottom of the result vector, then fill the
remainder of the result starting from the first byte of the
second source vector.
The result is placed
destructively in the destination and first source vector,
   or constructively in the destination vector.
This instruction is unpredicated.

An index that is greater than or equal to the vector
length in bytes is treated as zero,
resulting in the first source vector being copied to the result unchanged.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `Constructive`
- **Assembly**: `EXT  <Zd>.B, { <Zn1>.B, <Zn2>.B }, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24  22 21 20  15  12   9   4  |
|--------------------------------|
| 000 0010 10  1   1   imm8h 000 imm8l Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_extract.sve_intx_perm_extract_i.ext_z_zi_con)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8;
constant integer dst = UInt(Zd);
constant integer s1 = UInt(Zn);
constant integer s2 = (s1 + 1) MOD 32;
constant integer position = UInt(imm8h:imm8l) * 8;
```

#### Execute (A64.sve.sve_perm_extract.sve_intx_perm_extract_i.ext_z_zi_con)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[s1, VL];
constant bits(VL) operand2 = Z[s2, VL];
bits(VL) result;

constant bits(VL*2) concat = operand2 : operand1;

if position >= VL then
    result = concat<VL-1:0>;
else
    result = concat<(position+VL)-1:position>;

Z[dst, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Variant: `Destructive`
- **Assembly**: `EXT  <Zdn>.B, <Zdn>.B, <Zm>.B, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24  22 21 20  15  12   9   4  |
|--------------------------------|
| 000 0010 10  0   1   imm8h 000 imm8l Zm  Zdn |
```

#### Decode (A64.sve.sve_perm_extract.sve_int_perm_extract_i.ext_z_zi_des)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8;
constant integer dst = UInt(Zdn);
constant integer s1 = dst;
constant integer s2 = UInt(Zm);
constant integer position = UInt(imm8h:imm8l) * 8;
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
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded in the "Zn" field. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded in the "Zn" field. |
| `<imm>` | `immediate` | `imm8h:imm8l` | Is the unsigned immediate operand, in the range 0 to 255, encoded in the "imm8h:imm8l" fields. |
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the first source and destination scalable vector register, encoded in the "Zdn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        The destructive variant of this instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must
conform to all of the following requirements, othe
... (truncated)

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ext_z_zi.xml`
</details>