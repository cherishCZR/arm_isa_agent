## FVDOTB
_ARM A64 Instruction_

**Title**: FVDOTB -- A64 | **Class**: `mortlach2` | **XML ID**: `fvdotb_za32_z8z8i`

**Architecture**: `FEAT_SME_F8F32` (ARMv9.5)

**Summary**: Multi-vector 8-bit floating-point vertical dot-product by indexed element to single-precision (bottom)

**Description**:
This instruction computes the fused sum-of-products of each vertical group of
two 8-bit floating-point values held in the corresponding elements of the two
first source vectors with the lower-numbered horizontal group of two 8-bit
floating-point values in the indexed 32-bit group of the corresponding 128-bit segment of the second source vector.
The single-precision sum-of-products are scaled by 2-UInt(FPMR.LSCALE),
before being destructively added without intermediate rounding to the corresponding single-precision elements
of the four ZA single-vector groups.
The 8-bit floating-point encoding format for the elements of the first source vector
and the second source vector is selected by FPMR.F8S1 and FPMR.F8S2
respectively.

The 8-bit floating-point groups within the second source vector are specified
using an immediate index which selects the same group position within each 128-bit vector segment.

The single-vector group within each quarter
of the ZA array is selected by the sum of the vector select register and offset, modulo
quarter the number of ZA array vectors.

The vector group symbol VGx4 indicates that the ZA operand consists
of four ZA single-vector groups.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `FVDOTB  ZA.S[<Wv>, <offs>, VGx4], { <Zn1>.B-<Zn2>.B }, <Zm>.B[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12  10  9   5  4  3  2  |
|--------------------------------------------------|
| 1   10  0000 1   11  01  Zm  0   Rv  01  i2h Zn  0   0   i2l off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_2.mortlach_multi2_fp8_fvdot_idx_s.fvdotb_za32_z8z8i_2xi)

```
if !IsFeatureImplemented(FEAT_SME_F8F32) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'0');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i2h:i2l);
```

#### Execute (A64.sme.mortlach_multi_indexed_2.mortlach_multi2_fp8_fvdot_idx_s.fvdotb_za32_z8z8i_2xi)

```
CheckFPMREnabled();
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 32;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV 4;
constant integer eltspersegment = 128 DIV 32;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
bits(VL) result;

for r = 0 to 3
    constant bits(VL) operand1a = Z[n+0, VL];
    constant bits(VL) operand1b = Z[n+1, VL];
    constant bits(VL) operand2 = Z[m, VL];
    constant bits(VL) operand3 = ZAvector[vec, VL];
    for e = 0 to elements-1
        bits(16) op1;
        Elem[op1, 0, 8] = Elem[operand1a, 4 * e + r, 8];
        Elem[op1, 1, 8] = Elem[operand1b, 4 * e + r, 8];
        constant integer segmentbase = e - (e MOD eltspersegment);
        constant integer s = 2*(segmentbase + index);
        constant bits(16) op2 = Elem[operand2, s, 16];
        bits(32) sum  = Elem[operand3, e, 32];
        sum = FP8DotAddFP(sum, op1, op2, FPCR, FPMR);
        Elem[result, e, 32] = sum;

    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F8F32)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" times 2. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<index>` | `unknown` | `i2h:i2l` | Is the immediate index of a 32-bit group of four 8-bit values within each 128-bit vector segment, in the range 0 to 3, encoded in the "i2h:i2l" fields |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fvdotb_za32_z8z8i.xml`
</details>