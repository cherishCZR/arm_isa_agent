## EXTQ
_ARM A64 Instruction_

**Title**: EXTQ -- A64 | **Class**: `sve2` | **XML ID**: `extq_z_zi`

**Architecture**: `FEAT_SVE2p1 || FEAT_SME2p1` (FEAT_SVE2p1 || FEAT_SME2p1)

**Summary**: Extract vector segment from each pair of quadword vector segments

**Description**:
For each 128-bit vector segment of the result, copy the indexed byte
up to and including the last byte of the corresponding first source
vector segment to the bottom of the result segment,
then fill the remainder of the result segment starting from the first byte
of the corresponding second source vector segment.
The result segments are destructively placed in the corresponding
first source vector segment.
This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `EXTQ  <Zdn>.B, <Zdn>.B, <Zm>.B, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15   9   4  |
|--------------------------------|
| 000 0010 1   01  1   0   imm4 001001 Zm  Zdn |
```

#### Decode (A64.sve.sve_perm_quads_a.sve_int_perm_extq.extq_z_zi_des)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer dn = UInt(Zdn);
constant integer m = UInt(Zm);
constant integer position = UInt(imm4) << 3;
```

#### Execute (A64.sve.sve_perm_quads_a.sve_int_perm_extq.extq_z_zi_des)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments = VL DIV 128;
constant bits(VL) operand1 = Z[dn, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for s = 0 to segments-1
    constant bits(256) concat = Elem[operand2, s, 128] : Elem[operand1, s, 128];
    Elem[result, s, 128] = concat<position+127:position>;

Z[dn, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p1) \|\| IsFeatureImplemented(FEAT_SME2p1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the first source and destination scalable vector register, encoded in the "Zdn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `imm4` | Is the unsigned immediate operand, in the range 0 to 15, encoded in the "imm4" field. |

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
- source: `extq_z_zi.xml`
</details>