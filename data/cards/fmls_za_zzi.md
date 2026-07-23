## FMLS
_ARM A64 Instruction_

**Title**: FMLS (multiple and indexed vector) -- A64 | **Class**: `mortlach2` | **XML ID**: `fmls_za_zzi`

**Architecture**: `FEAT_SME_F16F16` (ARMv9.4), `FEAT_SME2` (ARMv9.3), `FEAT_SME2 && FEAT_SME_F64F64` (FEAT_SME2 && FEAT_SME_F64F64)

**Summary**: Multi-vector floating-point fused multiply-subtract by indexed element

**Description**:
This instruction multiplies the indexed element of the
second source vector by the corresponding floating-point elements of the two or four first
source vectors and destructively subtracts these values without intermediate rounding from the corresponding elements of the ZA single-vector groups.

The elements within the second source vector are specified using an immediate element index
which selects the same element position within each 128-bit vector segment. The index
range is from 0 to one less than the number of elements per
128-bit segment.

The single-vector
group within each half of or each quarter of the ZA array is selected by the sum
of the vector select register and offset, modulo half or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA single-vector
groups
respectively. The vector group symbol is preferred
for disassembly, but optional in assembler source code.

This instruction follows SME ZA-targeting floating-point behaviors.

This instruction is unpredicated.

ID_AA64SMFR0_EL1.F64F64 indicates whether the double-precision variant is
implemented, and ID_AA64SMFR0_EL1.F16F16 indicates whether the half-precision variant is implemented.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two ZA single-vectors of half-precision elements`
- **Assembly**: `FMLS  ZA.H[<Wv>, <offs>{, VGx2}], { <Zn1>.H-<Zn2>.H }, <Zm>.H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   5  4  3  2  |
|--------------------------------------------------|
| 1   10  0000 1   00  01  Zm  0   Rv  1   i3h Zn  0   1   i3l off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_2.mortlach_multi2_zza_idx_h.fmls_za_zzi_h2xi)

```
if !IsFeatureImplemented(FEAT_SME_F16F16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 16;
constant integer n = UInt(Zn:'0');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i3h:i3l);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_indexed_2.mortlach_multi2_zza_idx_h.fmls_za_zzi_h2xi)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant integer eltspersegment = 128 DIV esize;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
bits(VL) result;

for r = 0 to nreg-1
    constant bits(VL) op1 = Z[n+r, VL];
    constant bits(VL) op2 = Z[m, VL];
    constant bits(VL) op3 = ZAvector[vec, VL];
    for e = 0 to elements-1
        constant bits(esize) elem1 = FPNeg(Elem[op1, e, esize], FPCR);
        constant integer segmentbase = e - (e MOD eltspersegment);
        constant integer s = segmentbase + index;
        constant bits(esize) elem2 = Elem[op2, s, esize];
        constant bits(esize) elem3 = Elem[op3, e, esize];
        Elem[result, e, esize] = FPMulAdd_ZA(elem3, elem1, elem2, FPCR);
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

### Variant: `Two ZA single-vectors of single-precision elements`
- **Assembly**: `FMLS  ZA.S[<Wv>, <offs>{, VGx2}], { <Zn1>.S-<Zn2>.S }, <Zm>.S[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   5  4  3  2  |
|--------------------------------------------------|
| 1   10  0000 1   01  01  Zm  0   Rv  0   i2  Zn  0   1   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_2.mortlach_multi2_zza_idx_s.fmls_za_zzi_s2xi)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 32;
constant integer n = UInt(Zn:'0');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i2);
constant integer nreg = 2;
```

### Variant: `Two ZA single-vectors of double-precision elements`
- **Assembly**: `FMLS  ZA.D[<Wv>, <offs>{, VGx2}], { <Zn1>.D-<Zn2>.D }, <Zm>.D[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12  10  9   5  4  3  2  |
|--------------------------------------------------|
| 1   10  0000 1   11  01  Zm  0   Rv  00  i1  Zn  0   1   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_2.mortlach_multi2_zza_idx_d.fmls_za_zzi_d2xi)

```
if !(IsFeatureImplemented(FEAT_SME2) && IsFeatureImplemented(FEAT_SME_F64F64)) then
    EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 64;
constant integer n = UInt(Zn:'0');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i1);
constant integer nreg = 2;
```

### Variant: `Four ZA single-vectors of half-precision elements`
- **Assembly**: `FMLS  ZA.H[<Wv>, <offs>{, VGx4}], { <Zn1>.H-<Zn4>.H }, <Zm>.H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   6  5  4  3  2  |
|-----------------------------------------------------|
| 1   10  0000 1   00  01  Zm  1   Rv  1   i3h Zn  0   0   1   i3l off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_3.mortlach_multi4_zza_idx_h.fmls_za_zzi_h4xi)

```
if !IsFeatureImplemented(FEAT_SME_F16F16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 16;
constant integer n = UInt(Zn:'00');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i3h:i3l);
constant integer nreg = 4;
```

### Variant: `Four ZA single-vectors of single-precision elements`
- **Assembly**: `FMLS  ZA.S[<Wv>, <offs>{, VGx4}], { <Zn1>.S-<Zn4>.S }, <Zm>.S[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   6  5  4  3  2  |
|-----------------------------------------------------|
| 1   10  0000 1   01  01  Zm  1   Rv  0   i2  Zn  0   0   1   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_3.mortlach_multi4_zza_idx_s.fmls_za_zzi_s4xi)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 32;
constant integer n = UInt(Zn:'00');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i2);
constant integer nreg = 4;
```

### Variant: `Four ZA single-vectors of double-precision elements`
- **Assembly**: `FMLS  ZA.D[<Wv>, <offs>{, VGx4}], { <Zn1>.D-<Zn4>.D }, <Zm>.D[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11 10  9   6   4  3  2  |
|-----------------------------------------------------|
| 1   10  0000 1   11  01  Zm  1   Rv  0   0   i1  Zn  00  1   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_3.mortlach_multi4_zza_idx_d.fmls_za_zzi_d4xi)

```
if !(IsFeatureImplemented(FEAT_SME2) && IsFeatureImplemented(FEAT_SME_F64F64)) then
    EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 64;
constant integer n = UInt(Zn:'00');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i1);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Two ZA single-vectors of double-precision elements", "Two ZA single-vectors of half-precision elements", and "Two ZA single-vectors of single |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Four ZA single-vectors of double-precision elements", "Four ZA single-vectors of half-precision elements", and "Four ZA single-vectors of sin |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<index>` | `unknown` | `i3h:i3l` | For the "Four ZA single-vectors of half-precision elements" and "Two ZA single-vectors of half-precision elements" variants: is the element index, in  |
| `<index>` | `unknown` | `i2` | For the "Four ZA single-vectors of single-precision elements" and "Two ZA single-vectors of single-precision elements" variants: is the element index, |
| `<index>` | `unknown` | `i1` | For the "Four ZA single-vectors of double-precision elements" and "Two ZA single-vectors of double-precision elements" variants: is the element index, |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" times 4 plus 3. |

### Encoding Constraints
_3× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F16F16)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |
| 🔒 FEATURE_GATE | `!IsFeatureImplemented(FEAT_SME2) \|\| !IsFeatureImplemented(FEAT_SME_F64F64)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmls_za_zzi.xml`
</details>