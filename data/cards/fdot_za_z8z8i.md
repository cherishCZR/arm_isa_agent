## FDOT
_ARM A64 Instruction_

**Title**: FDOT (2-way, multiple and indexed vector, FP8 to FP16) -- A64 | **Class**: `mortlach2` | **XML ID**: `fdot_za_z8z8i`

**Architecture**: `FEAT_SME_F8F16` (ARMv9.5)

**Summary**: Multi-vector 8-bit floating-point dot-product by indexed element to half-precision

**Description**:
This instruction computes the fused sum-of-products of a group of two 8-bit floating-point values
held in the corresponding 16-bit elements of the two or four first source vectors and the indexed 16-bit element of the second source vector.
The half-precision sum-of-products are scaled by 2-UInt(FPMR.LSCALE[3:0]),
before being destructively added without intermediate rounding to the corresponding half-precision elements
of the ZA single-vector groups.
The 8-bit floating-point encoding format for the elements of the first source vector
and the second source vector is selected by FPMR.F8S1 and FPMR.F8S2
respectively.

The 8-bit floating-point pairs within the second source vector are specified
using an immediate index which selects the same pair position within each 128-bit vector segment.

The single-vector
group within each half of or each quarter of the ZA array is selected by the sum
of the vector select register and offset, modulo half or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA single-vector
groups
respectively. The vector group symbol is preferred
for disassembly, but optional in assembler source code.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two ZA single-vectors`
- **Assembly**: `FDOT  ZA.H[<Wv>, <offs>{, VGx2}], { <Zn1>.B-<Zn2>.B }, <Zm>.B[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   5  4  3  2  |
|--------------------------------------------------|
| 1   10  0000 1   11  01  Zm  0   Rv  0   i3h Zn  1   0   i3l off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_2.mortlach_multi2_fp8_fdot_idx.fdot_za_z8z8i_2xi)

```
if !IsFeatureImplemented(FEAT_SME_F8F16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'0');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i3h:i3l);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_indexed_2.mortlach_multi2_fp8_fdot_idx.fdot_za_z8z8i_2xi)

```
CheckFPMREnabled();
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant integer eltspersegment = 128 DIV 16;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
bits(VL) result;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[n+r, VL];
    constant bits(VL) operand2 = Z[m, VL];
    constant bits(VL) operand3 = ZAvector[vec, VL];
    for e = 0 to elements-1
        constant bits(16) op1 = Elem[operand1, e, 16];
        constant integer segmentbase = e - (e MOD eltspersegment);
        constant integer s = segmentbase + index;
        constant bits(16) op2 = Elem[operand2, s, 16];
        bits(16) sum = Elem[operand3, e, 16];
        sum = FP8DotAddFP(sum, op1, op2, FPCR, FPMR);
        Elem[result, e, 16] = sum;
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

### Variant: `Four ZA single-vectors`
- **Assembly**: `FDOT  ZA.H[<Wv>, <offs>{, VGx4}], { <Zn1>.B-<Zn4>.B }, <Zm>.B[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   6   3  2  |
|-----------------------------------------------|
| 1   10  0000 1   00  01  Zm  1   Rv  1   i3h Zn  100 i3l off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_3.mortlach_multi4_fp8_fdot_idx_h.fdot_za_z8z8i_4xi)

```
if !IsFeatureImplemented(FEAT_SME_F8F16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'00');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i3h:i3l);
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
| `<index>` | `unknown` | `i3h:i3l` | Is the immediate index of a group of two 8-bit elements within each 128-bit vector segment, in the range 0 to 7, encoded in the "i3h:i3l" fields. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" times 4 plus 3. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F8F16)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fdot_za_z8z8i.xml`
</details>