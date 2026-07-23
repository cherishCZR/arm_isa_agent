## MOVA
_ARM A64 Instruction_

**Title**: MOVA (vector to array, two registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `mova_za_mz2`

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
- **Assembly**: `MOVA  ZA.D[<Wv>, <offs>{, VGx2}], { <Zn1>.D-<Zn2>.D }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16  14  12   9   5  4  3  2  |
|--------------------------------------------------|
| 1   10  0000 0   00  000 1   0   00  Rv  010 Zn  0   0   0   off3 |
```

#### Decode (A64.sme.mortlach_ins.mortlach_multi2_za_insert_ctg.mova_za_mz2_1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer offset = UInt(off3);
constant integer n = UInt(Zn:'0');
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_ins.mortlach_multi2_za_insert_ctg.mova_za_mz2_1)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;

for r = 0 to nreg-1
    constant bits(VL) result = Z[n + r, VL];
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

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

- isa: `A64`
- source: `mova_za_mz2.xml`
</details>