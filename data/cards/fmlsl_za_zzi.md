## FMLSL
_ARM A64 Instruction_

**Title**: FMLSL (multiple and indexed vector) -- A64 | **Class**: `mortlach2` | **XML ID**: `fmlsl_za_zzi`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector floating-point multiply-subtract long by indexed element

**Description**:
This instruction widens all 16-bit half-precision elements in the
one, two, or four first source vectors and the indexed element of the second source vector to
single-precision format, then multiplies the corresponding elements and destructively subtracts these
values without intermediate rounding from the overlapping 32-bit
single-precision elements of the ZA double-vector groups.

The half-precision elements within the second source vector are specified using a
3-bit immediate index which selects the same element position within each 128-bit
vector segment.

The double-vector
group within all of, each half of,
or each quarter of the ZA array is selected by the sum
of the vector select register and offset range, modulo all, half, or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA double-vector
groups
respectively. The vector group symbol is preferred
for disassembly, but optional in assembler source code.

This instruction follows SME ZA-targeting floating-point behaviors.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `One ZA double-vector`
- **Assembly**: `FMLSL  ZA.S[<Wv>, <offs1>:<offs2>], <Zn>.H, <Zm>.H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   4  3  2  |
|-----------------------------------------------|
| 1   10  0000 1   10  00  Zm  i3h Rv  1   i3l Zn  0   1   off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_1.mortlach_multi1_fma_long_idx.fmlsl_za_zzi_1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3:'0');
constant integer index = UInt(i3h:i3l);
constant integer nreg = 1;
```

#### Execute (A64.sme.mortlach_multi_indexed_1.mortlach_multi1_fma_long_idx.fmlsl_za_zzi_1)

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
vec = vec - (vec MOD 2);

for r = 0 to nreg-1
    constant bits(VL) op1 = Z[n+r, VL];
    constant bits(VL) op2 = Z[m, VL];
    for i = 0 to 1
        constant bits(VL) op3 = ZAvector[vec + i, VL];
        for e = 0 to elements-1
            constant integer segmentbase = e - (e MOD eltspersegment);
            constant integer s = 2 * segmentbase + index;
            constant bits(16) elem1 = FPNeg(Elem[op1, 2 * e + i, 16], FPCR);
            constant bits(16) elem2 = Elem[op2, s, 16];
            constant bits(32) elem3 = Elem[op3, e, 32];
            Elem[result, e, 32] = FPMulAddH_ZA(elem3, elem1, elem2,
                                                    FPCR);
        ZAvector[vec + i, VL] = result;
    vec = vec + vstride;
```

### Variant: `Two ZA double-vectors`
- **Assembly**: `FMLSL  ZA.S[<Wv>, <offs1>:<offs2>{, VGx2}], { <Zn1>.H-<Zn2>.H }, <Zm>.H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   5  4  3  2  1  |
|-----------------------------------------------------|
| 1   10  0000 1   10  01  Zm  0   Rv  1   i3h Zn  0   0   1   i3l off2 |
```

#### Decode (A64.sme.mortlach_multi_indexed_2.mortlach_multi2_fma_long_idx.fmlsl_za_zzi_2xi)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'0');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off2:'0');
constant integer index = UInt(i3h:i3l);
constant integer nreg = 2;
```

### Variant: `Four ZA double-vectors`
- **Assembly**: `FMLSL  ZA.S[<Wv>, <offs1>:<offs2>{, VGx4}], { <Zn1>.H-<Zn4>.H }, <Zm>.H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   6   4  3  2  1  |
|-----------------------------------------------------|
| 1   10  0000 1   10  01  Zm  1   Rv  1   i3h Zn  00  0   1   i3l off2 |
```

#### Decode (A64.sme.mortlach_multi_indexed_3.mortlach_multi4_fma_long_idx.fmlsl_za_zzi_4xi)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'00');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off2:'0');
constant integer index = UInt(i3h:i3l);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs1>` | `unknown` | `off3` | For the "One ZA double-vector" variant: is the first vector select offset, encoded as "off3" field times 2. |
| `<offs1>` | `unknown` | `off2` | For the "Four ZA double-vectors" and "Two ZA double-vectors" variants: is the first vector select offset, encoded as "off2" field times 2. |
| `<offs2>` | `unknown` | `off3` | For the "One ZA double-vector" variant: is the second vector select offset, encoded as "off3" field times 2 plus 1. |
| `<offs2>` | `unknown` | `off2` | For the "Four ZA double-vectors" and "Two ZA double-vectors" variants: is the second vector select offset, encoded as "off2" field times 2 plus 1. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<index>` | `unknown` | `i3h:i3l` | Is the element index, in the range 0 to 7, encoded in the "i3h:i3l" fields. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Two ZA double-vectors" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" tim |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Four ZA double-vectors" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" ti |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" times 4 plus 3. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmlsl_za_zzi.xml`
</details>