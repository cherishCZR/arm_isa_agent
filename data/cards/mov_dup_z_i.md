## DUP `[ALIAS]`
_ARM A64 Instruction_ (Alias of dup_z_i.xml)

**Title**: MOV (immediate, unpredicated) -- A64 | **Class**: `sve` | **XML ID**: `mov_dup_z_i`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move signed immediate to vector elements (unpredicated)

**Description**:
Unconditionally broadcast the signed integer immediate into each element of the
destination vector. This instruction is unpredicated.

The immediate operand is a signed value in the range -128 to
+127, and for element widths of 16 bits or higher it may also be
a signed multiple of 256 in the range -32768 to +32512 (excluding 0).

The immediate is encoded in 8 bits with an optional left shift
by 8. The preferred disassembly when the shift option is
specified is "#<simm8>, LSL #8".
However an assembler and
disassembler may also allow use of the shifted 16-bit value unless the
immediate is 0 and the shift amount is 8, which must be
unambiguously described as "#0, LSL #8".

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `MOV  <Zd>.<T>, #<imm>{, <shift>}`
- **Alias of**: `DUP  <Zd>.<T>, #<imm>{, <shift>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  16 15  13 12   4  |
|--------------------------------------|
| 001 0010 1   size 1   11  00  0   11  sh  imm8 Zd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<imm>` | `immediate` | `imm8` | Is a signed immediate in the range -128 to 127, encoded in the "imm8" field. |
| `<shift>` | `shift` | `sh` | Is the optional left shift to apply to the immediate, defaulting to LSL #0 and |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | LSL #0 |
| 1 | LSL #8 |

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

- alias_mnemonic: `MOV`
- isa: `A64`
- source: `mov_dup_z_i.xml`
</details>