## ORR
_ARM A64 Instruction_

**Title**: ORR (immediate) -- A64 | **Class**: `sve` | **XML ID**: `orr_z_zi`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Bitwise inclusive OR with immediate (unpredicated)

**Description**:
Bitwise inclusive OR an immediate with
each 64-bit element of the source vector,
and destructively place the results in the corresponding elements of the  source vector. The immediate is a 64-bit value consisting of a single run of ones or zeros
repeating every 2, 4, 8, 16, 32 or 64 bits. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `ORR  <Zdn>.<T>, <Zdn>.<T>, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  19  17   4  |
|--------------------------|
| 000 0010 1   00  00  00  imm13 Zdn |
```

#### Decode (A64.sve.sve_maskimm.sve_int_log_imm.orr_z_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer dn = UInt(Zdn);
bits(64) imm;
(imm, -) = DecodeBitMasks(imm13<12>, imm13<5:0>, imm13<11:6>, TRUE, 64);
```

#### Execute (A64.sve.sve_maskimm.sve_int_log_imm.orr_z_zi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 64;
constant bits(VL) operand = Z[dn, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(64) element1 = Elem[operand, e, 64];
    Elem[result, e, 64] = element1 OR imm;

Z[dn, VL] = result;
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
                
              
            
          
        
        This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `orr_z_zi.xml`
</details>