## EOR `[ALIAS]`
_ARM A64 Instruction_ (Alias of eor_z_zi.xml)

**Title**: EON -- A64 | **Class**: `sve` | **XML ID**: `eon_eor_z_zi`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Bitwise exclusive-OR with inverted immediate (unpredicated)

**Description**:
Bitwise exclusive-OR an inverted immediate with
each 64-bit element of the source vector,
and destructively place the results in the corresponding elements of the  source vector. The immediate is a 64-bit value consisting of a single run of ones or zeros
repeating every 2, 4, 8, 16, 32 or 64 bits. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `EON  <Zdn>.<T>, <Zdn>.<T>, #<const>`
- **Alias of**: `EOR  <Zdn>.<T>, <Zdn>.<T>, #(-<const> - 1)`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  19  17   4  |
|--------------------------|
| 000 0010 1   01  00  00  imm13 Zdn |
```

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

- alias_mnemonic: `EON`
- isa: `A64`
- source: `eon_eor_z_zi.xml`
</details>