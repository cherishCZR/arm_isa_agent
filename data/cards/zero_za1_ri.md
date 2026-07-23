## ZERO
_ARM A64 Instruction_

**Title**: ZERO (single-vector) -- A64 | **Class**: `mortlach2` | **XML ID**: `zero_za1_ri`

**Architecture**: `FEAT_SME2p1` (ARMv9.4)

**Summary**: Zero ZA single-vector groups

**Description**:
This instruction zeroes two or four ZA single-vector groups.

The single-vector
group within each half of or each quarter of the ZA array is selected by the sum
of the vector select register and offset, modulo half or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA single-vector
groups
respectively.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `Two ZA single-vectors`
- **Assembly**: `ZERO  ZA.D[<Wv>, <offs>, VGx2]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  17  14  12   2  |
|--------------------------|
| 1   10  0000 0000011 000 Rv  0000000000 off3 |
```

#### Decode (A64.sme.mortlach_multizero.mortlach_multi_zero.zero_za1_ri_2)

```
if !IsFeatureImplemented(FEAT_SME2p1) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer offset = UInt(off3);
constant integer ngrp = 2;
```

#### Execute (A64.sme.mortlach_multizero.mortlach_multi_zero.zero_za1_ri_2)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV ngrp;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
for r = 0 to ngrp-1
    ZAvector[vec, VL] = Zeros(VL);
    vec = vec + vstride;
```

### Variant: `Four ZA single-vectors`
- **Assembly**: `ZERO  ZA.D[<Wv>, <offs>, VGx4]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  17  14  12   2  |
|--------------------------|
| 1   10  0000 0000011 100 Rv  0000000000 off3 |
```

#### Decode (A64.sme.mortlach_multizero.mortlach_multi_zero.zero_za1_ri_4)

```
if !IsFeatureImplemented(FEAT_SME2p1) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer offset = UInt(off3);
constant integer ngrp = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2p1)` |

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
- source: `zero_za1_ri.xml`
</details>