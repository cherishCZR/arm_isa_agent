## MOVA `[ALIAS]`
_ARM A64 Instruction_ (Alias of mova_za_mz2.xml)

**Title**: MOV (vector to array, two registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `mov_mova_za_mz2`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Move two vector registers to two ZA single-vector groups

**Description**:
This instruction operates on two ZA single-vector groups.

The single-vector group within each half
of the ZA array is selected by the sum of the vector select register and offset, modulo
half the number of ZA array vectors.

The vector group symbol VGx2
indicates that the instruction operates on two ZA single-vector groups.

The preferred disassembly syntax uses a 64-bit element size, but an assembler should accept
any element size if it is used consistently for all operands. The vector group symbol is
preferred for disassembly, but optional in assembler source code.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `MOV  ZA.D[<Wv>, <offs>{, VGx2}], { <Zn1>.D-<Zn2>.D }`
- **Alias of**: `MOVA  ZA.D[<Wv>, <offs>{, VGx2}], { <Zn1>.D-<Zn2>.D }`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16  14  12   9   5  4  3  2  |
|--------------------------------------------------|
| 1   10  0000 0   00  000 1   0   00  Rv  010 Zn  0   0   0   off3 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 2. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zn" times 2 plus 1. |

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
- source: `mov_mova_za_mz2.xml`
</details>