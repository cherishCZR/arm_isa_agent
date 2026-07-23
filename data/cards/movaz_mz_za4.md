## MOVAZ
_ARM A64 Instruction_

**Title**: MOVAZ (array to vector, four registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `movaz_mz_za4`

**Architecture**: `FEAT_SME2p1` (ARMv9.4)

**Summary**: Move and zero four ZA single-vector groups to vector registers

**Description**:
This instruction operates on four ZA single-vector groups. The ZA single-vector groups are zeroed after moving their contents to the destination vectors.

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
- **Assembly**: `MOVAZ  { <Zd1>.D-<Zd4>.D }, ZA.D[<Wv>, <offs>{, VGx4}]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16  14  12   9   7   4   1  |
|-----------------------------------------------|
| 1   10  0000 0   00  000 1   1   00  Rv  011 10  off3 Zd  00  |
```

#### Decode (A64.sme.mortlach_ext.mortlach_multi4_za_extract_zero.movaz_mz_za4_1)

```
if !IsFeatureImplemented(FEAT_SME2p1) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer offset = UInt(off3);
constant integer d = UInt(Zd:'00');
constant integer nreg = 4;
```

#### Execute (A64.sme.mortlach_ext.mortlach_multi4_za_extract_zero.movaz_mz_za4_1)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;

for r = 0 to nreg-1
    constant bits(VL) result = ZAvector[vec, VL];
    ZAvector[vec, VL] = Zeros(VL);
    Z[d + r, VL] = result;
    vec = vec + vstride;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2p1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | Is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 4. |
| `<Zd4>` | `register (128-bit)` | `Zd` | Is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus 3. |
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |

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
- source: `movaz_mz_za4.xml`
</details>