## BFDOT
_ARM A64 Instruction_

**Title**: BFDOT (multiple and indexed vector) -- A64 | **Class**: `mortlach2` | **XML ID**: `bfdot_za_zzi`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector BFloat16 dot-product by indexed element

**Description**:
This instruction computes the dot product of a pair of BF16 values held in the corresponding 32-bit
elements of the two or four first source
vectors and the indexed 32-bit element of the second source vector. The single-precision dot product
results are destructively added to the corresponding single-precision elements of the ZA
single-vector groups.

The BF16 pairs within the second source vector are specified using an immediate index
which selects the same BF16 pair position within each 128-bit vector segment. The
element index range is from 0 to 3.

The single-vector
group within each half of or each quarter of the ZA array is selected by the sum
of the vector select register and offset, modulo half or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA single-vector
groups
respectively. The vector group symbol is preferred
for disassembly, but optional in assembler source code.

This instruction follows SME2 ZA-targeting BFloat16 numerical behaviors.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two ZA single-vectors`
- **Assembly**: `BFDOT  ZA.S[<Wv>, <offs>{, VGx2}], { <Zn1>.H-<Zn2>.H }, <Zm>.H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   5   2  |
|--------------------------------------------|
| 1   10  0000 1   01  01  Zm  0   Rv  1   i2  Zn  011 off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_2.mortlach_multi2_zza_idx_s.bfdot_za_zzi_2xi)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'0');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i2);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_indexed_2.mortlach_multi2_zza_idx_s.bfdot_za_zzi_2xi)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 32;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant integer eltspersegment = 128 DIV 32;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
bits(VL) result;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[n+r, VL];
    constant bits(VL) operand2 = Z[m, VL];
    constant bits(VL) operand3 = ZAvector[vec, VL];
    for e = 0 to elements-1
        constant bits(16) elt1_a = Elem[operand1, 2 * e + 0, 16];
        constant bits(16) elt1_b = Elem[operand1, 2 * e + 1, 16];
        constant integer segmentbase = e - (e MOD eltspersegment);
        constant integer s = segmentbase + index;
        constant bits(16) elt2_a = Elem[operand2, 2 * s + 0, 16];
        constant bits(16) elt2_b = Elem[operand2, 2 * s + 1, 16];
        bits(32) sum = Elem[operand3, e, 32];
        sum = BFDotAdd(sum, elt1_a, elt1_b, elt2_a, elt2_b, FPCR);
        Elem[result, e, 32] = sum;
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

### Variant: `Four ZA single-vectors`
- **Assembly**: `BFDOT  ZA.S[<Wv>, <offs>{, VGx4}], { <Zn1>.H-<Zn4>.H }, <Zm>.H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   6  5   2  |
|-----------------------------------------------|
| 1   10  0000 1   01  01  Zm  1   Rv  1   i2  Zn  0   011 off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_3.mortlach_multi4_zza_idx_s.bfdot_za_zzi_4xi)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'00');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i2);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Two ZA single-vectors" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" tim |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Four ZA single-vectors" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" ti |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<index>` | `unknown` | `i2` | Is the immediate index of a group of two 16-bit elements within each 128-bit vector segment, in the range 0 to 3, encoded in the "i2" field. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" times 4 plus 3. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfdot_za_zzi.xml`
</details>