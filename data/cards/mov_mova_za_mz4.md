## MOVA `[ALIAS]`
_ARM A64 Instruction_ (Alias of mova_za_mz4.xml)

**Title**: MOV (vector to array, four registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `mov_mova_za_mz4`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Move four vector registers to four ZA single-vector groups

**Description**:
This instruction operates on four ZA single-vector groups.

The single-vector group within each quarter
of the ZA array is selected by the sum of the vector select register and offset, modulo
quarter the number of ZA array vectors.

The vector group symbol VGx4
indicates that the instruction operates on four ZA single-vector groups.

The preferred disassembly syntax uses a 64-bit element size, but an assembler should accept
any element size if it is used consistently for all operands. The vector group symbol is
preferred for disassembly, but optional in assembler source code.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `MOV  ZA.D[<Wv>, <offs>{, VGx4}], { <Zn1>.D-<Zn4>.D }`
- **Alias of**: `MOVA  ZA.D[<Wv>, <offs>{, VGx4}], { <Zn1>.D-<Zn4>.D }`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16  14  12   9   6   4  3  2  |
|--------------------------------------------------|
| 1   10  0000 0   00  000 1   0   00  Rv  011 Zn  00  0   0   off3 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 4. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the source multi-vector group, encoded as "Zn" times 4 plus 3. |

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
- source: `mov_mova_za_mz4.xml`
</details>