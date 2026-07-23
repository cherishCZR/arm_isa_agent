## FMLAL
_ARM A64 Instruction_

**Title**: FMLAL (multiple and single vector, FP8 to FP16) -- A64 | **Class**: `mortlach2` | **XML ID**: `fmlal_za_z8z8v`

**Architecture**: `FEAT_SME_F8F16` (ARMv9.5)

**Summary**: Multi-vector 8-bit floating-point multiply-add long by vector to half-precision

**Description**:
This instruction widens all 8-bit floating-point elements in the one, two, or four first source vectors and the second
source vector to
half-precision format and multiplies the corresponding elements. The intermediate products are scaled by
2-UInt(FPMR.LSCALE[3:0]) before being destructively added
without intermediate rounding to the overlapping 16-bit
half-precision elements of the ZA double-vector groups.

The double-vector
group within all of, each half of,
or each quarter of the ZA array is selected by the sum
of the vector select register and offset range, modulo all, half, or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA double-vector
groups
respectively. The vector group symbol is preferred
for disassembly, but optional in assembler source code.

The 8-bit floating-point encoding format for the elements of the first source vector
and the second source vector is selected by FPMR.F8S1 and FPMR.F8S2
respectively.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `One ZA double-vector`
- **Assembly**: `FMLAL  ZA.H[<Wv>, <offs1>:<offs2>], <Zn>.B, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4   2  |
|-----------------------------------------|
| 1   10  0000 10  0   11  Zm  0   Rv  011 Zn  00  off3 |
```

#### Decode (A64.sme.mortlach_multi_array_1b.mortlach_multi1_zz_za_fp8_fma_long_sm.fmlal_za_z8z8v_1)

```
if !IsFeatureImplemented(FEAT_SME_F8F16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3:'0');
constant integer nreg = 1;
```

#### Execute (A64.sme.mortlach_multi_array_1b.mortlach_multi1_zz_za_fp8_fma_long_sm.fmlal_za_z8z8v_1)

```
CheckFPMREnabled();
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
bits(VL) result;
vec = vec - (vec MOD 2);

for r = 0 to nreg-1
    constant bits(VL) op1 = Z[(n+r) MOD 32, VL];
    constant bits(VL) op2 = Z[m, VL];
    for i = 0 to 1
        constant bits(VL) op3 = ZAvector[vec + i, VL];
        for e = 0 to elements-1
            constant bits(8) elem1 = Elem[op1, 2 * e + i, 8];
            constant bits(8) elem2 = Elem[op2, 2 * e + i, 8];
            constant bits(16) elem3 = Elem[op3, e, 16];
            Elem[result, e, 16] = FP8MulAddFP(elem3, elem1, elem2,
                                                    FPCR, FPMR);
        ZAvector[vec + i, VL] = result;
    vec = vec + vstride;
```

### Variant: `Two ZA double-vectors`
- **Assembly**: `FMLAL  ZA.H[<Wv>, <offs1>:<offs2>{, VGx2}], { <Zn1>.B-<Zn2>.B }, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4  3  2  1  |
|-----------------------------------------------|
| 1   10  0000 10  0   10  Zm  0   Rv  010 Zn  0   0   1   off2 |
```

#### Decode (A64.sme.mortlach_multi_array_1a.mortlach_multi2_zz_za_fma_long_sm.fmlal_za_z8z8v_2x1)

```
if !IsFeatureImplemented(FEAT_SME_F8F16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off2:'0');
constant integer nreg = 2;
```

### Variant: `Four ZA double-vectors`
- **Assembly**: `FMLAL  ZA.H[<Wv>, <offs1>:<offs2>{, VGx4}], { <Zn1>.B-<Zn4>.B }, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4  3  2  1  |
|-----------------------------------------------|
| 1   10  0000 10  0   11  Zm  0   Rv  010 Zn  0   0   1   off2 |
```

#### Decode (A64.sme.mortlach_multi_array_1b.mortlach_multi4_zz_za_fma_long_sm.fmlal_za_z8z8v_4x1)

```
if !IsFeatureImplemented(FEAT_SME_F8F16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off2:'0');
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
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn". |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" plus 1 modulo 32. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" plus 3 modulo 32. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F8F16)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmlal_za_z8z8v.xml`
</details>