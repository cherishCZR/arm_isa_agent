## FMLAL
_ARM A64 Instruction_

**Title**: FMLAL (multiple vectors, FP8 to FP16) -- A64 | **Class**: `mortlach2` | **XML ID**: `fmlal_za_z8z8w`

**Architecture**: `FEAT_SME_F8F16` (ARMv9.5)

**Summary**: Multi-vector 8-bit floating-point multiply-add long to half-precision

**Description**:
This instruction widens all 8-bit floating-point elements in the two or four first and second source vectors to
half-precision format and multiplies the corresponding elements. The intermediate products are scaled by
2-UInt(FPMR.LSCALE[3:0]) before being destructively added
without intermediate rounding to the overlapping 16-bit
half-precision elements of the ZA double-vector groups.

The double-vector
group within each half of or each quarter of the ZA array is selected by the sum
of the vector select register and offset range, modulo half or quarter the number of ZA array vectors.

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

### Variant: `Two ZA double-vectors`
- **Assembly**: `FMLAL  ZA.H[<Wv>, <offs1>:<offs2>{, VGx2}], { <Zn1>.B-<Zn2>.B }, { <Zm1>.B-<Zm2>.B }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  16  14  12   9   5  4   1  |
|--------------------------------------------|
| 1   10  0000 11  0   1   Zm  00  Rv  010 Zn  1   000 off2 |
```

#### Decode (A64.sme.mortlach_multi_array_2a.mortlach_multi2_zz_za_fp8_fma_long_mm.fmlal_za_z8z8w_2x2)

```
if !IsFeatureImplemented(FEAT_SME_F8F16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'0');
constant integer m = UInt(Zm:'0');
constant integer offset = UInt(off2:'0');
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_array_2a.mortlach_multi2_zz_za_fp8_fma_long_mm.fmlal_za_z8z8w_2x2)

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
    constant bits(VL) op1 = Z[n+r, VL];
    constant bits(VL) op2 = Z[m+r, VL];
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

### Variant: `Four ZA double-vectors`
- **Assembly**: `FMLAL  ZA.H[<Wv>, <offs1>:<offs2>{, VGx4}], { <Zn1>.B-<Zn4>.B }, { <Zm1>.B-<Zm4>.B }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  17 16  14  12   9   6   4   1  |
|-----------------------------------------------|
| 1   10  0000 11  0   1   Zm  0   10  Rv  010 Zn  01  000 off2 |
```

#### Decode (A64.sme.mortlach_multi_array_2b.mortlach_multi4_zz_za_fp8_fma_long_mm.fmlal_za_z8z8w_4x4)

```
if !IsFeatureImplemented(FEAT_SME_F8F16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'00');
constant integer m = UInt(Zm:'00');
constant integer offset = UInt(off2:'0');
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs1>` | `unknown` | `off2` | Is the first vector select offset, encoded as "off2" field times 2. |
| `<offs2>` | `unknown` | `off2` | Is the second vector select offset, encoded as "off2" field times 2 plus 1. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Two ZA double-vectors" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" tim |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Four ZA double-vectors" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" ti |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Two ZA double-vectors" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" ti |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Four ZA double-vectors" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" t |
| `<Zm2>` | `register (128-bit)` | `Zm` | Is the name of the second scalable vector register of the second source multi-vector group, encoded as "Zm" times 2 plus 1. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" times 4 plus 3. |
| `<Zm4>` | `register (128-bit)` | `Zm` | Is the name of the fourth scalable vector register of the second source multi-vector group, encoded as "Zm" times 4 plus 3. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F8F16)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmlal_za_z8z8w.xml`
</details>