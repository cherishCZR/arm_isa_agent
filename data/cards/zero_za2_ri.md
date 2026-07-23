## ZERO
_ARM A64 Instruction_

**Title**: ZERO (double-vector) -- A64 | **Class**: `mortlach2` | **XML ID**: `zero_za2_ri`

**Architecture**: `FEAT_SME2p1` (ARMv9.4)

**Summary**: Zero ZA double-vector groups

**Description**:
This instruction zeroes one, two, or four ZA double-vector groups.

The double-vector
group within all of, each half of,
or each quarter of the ZA array is selected by the sum
of the vector select register and offset range, modulo all, half, or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA double-vector
groups
respectively.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `One ZA double-vector`
- **Assembly**: `ZERO  ZA.D[<Wv>, <offs1>:<offs2>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  17  14  12   2  |
|--------------------------|
| 1   10  0000 0000011 001 Rv  0000000000 off3 |
```

#### Decode (A64.sme.mortlach_multizero.mortlach_multi_zero.zero_za2_ri_1)

```
if !IsFeatureImplemented(FEAT_SME2p1) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer offset = UInt(off3:'0');
constant integer ngrp = 1;
constant integer nvec = 2;
```

#### Execute (A64.sme.mortlach_multizero.mortlach_multi_zero.zero_za2_ri_1)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV ngrp;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
vec = vec - (vec MOD nvec);
for r = 0 to ngrp-1
    for i = 0 to nvec-1
        ZAvector[vec + i, VL] = Zeros(VL);
    vec = vec + vstride;
```

### Variant: `Two ZA double-vectors`
- **Assembly**: `ZERO  ZA.D[<Wv>, <offs1>:<offs2>, VGx2]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  17  14  12   2  1  |
|-----------------------------|
| 1   10  0000 0000011 010 Rv  0000000000 0   off2 |
```

#### Decode (A64.sme.mortlach_multizero.mortlach_multi_zero.zero_za2_ri_2)

```
if !IsFeatureImplemented(FEAT_SME2p1) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer offset = UInt(off2:'0');
constant integer ngrp = 2;
constant integer nvec = 2;
```

### Variant: `Four ZA double-vectors`
- **Assembly**: `ZERO  ZA.D[<Wv>, <offs1>:<offs2>, VGx4]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  17  14  12   2  1  |
|-----------------------------|
| 1   10  0000 0000011 011 Rv  0000000000 0   off2 |
```

#### Decode (A64.sme.mortlach_multizero.mortlach_multi_zero.zero_za2_ri_4)

```
if !IsFeatureImplemented(FEAT_SME2p1) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer offset = UInt(off2:'0');
constant integer ngrp = 4;
constant integer nvec = 2;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs1>` | `unknown` | `off3` | For the "One ZA double-vector" variant: is the first vector select offset, encoded as "off3" field times 2. |
| `<offs1>` | `unknown` | `off2` | For the "Four ZA double-vectors" and "Two ZA double-vectors" variants: is the first vector select offset, encoded as "off2" field times 2. |
| `<offs2>` | `unknown` | `off3` | For the "One ZA double-vector" variant: is the second vector select offset, encoded as "off3" field times 2 plus 1. |
| `<offs2>` | `unknown` | `off2` | For the "Four ZA double-vectors" and "Two ZA double-vectors" variants: is the second vector select offset, encoded as "off2" field times 2 plus 1. |

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
- source: `zero_za2_ri.xml`
</details>