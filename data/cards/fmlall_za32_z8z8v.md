## FMLALL
_ARM A64 Instruction_

**Title**: FMLALL (multiple and single vector) -- A64 | **Class**: `mortlach2` | **XML ID**: `fmlall_za32_z8z8v`

**Architecture**: `FEAT_SME_F8F32` (ARMv9.5)

**Summary**: Multi-vector 8-bit floating-point multiply-add long-long by vector to single-precision

**Description**:
This instruction widens all 8-bit floating-point elements in the one, two, or four first source vectors and the second
source vector to
single-precision format and multiplies the corresponding elements. The intermediate products are scaled by
2-UInt(FPMR.LSCALE) before being destructively added
without intermediate rounding to the overlapping 32-bit
single-precision elements of the ZA quad-vector groups.

The quad-vector
group within all of, each half of,
or each quarter of the ZA array is selected by the sum
of the vector select register and offset range, modulo all, half, or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA quad-vector
groups
respectively. The vector group symbol is preferred
for disassembly, but optional in assembler source code.

The 8-bit floating-point encoding format for the elements of the first source vector
and the second source vector is selected by FPMR.F8S1 and FPMR.F8S2
respectively.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `One ZA quad-vector`
- **Assembly**: `FMLALL  ZA.S[<Wv>, <offs1>:<offs4>], <Zn>.B, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4   1  |
|-----------------------------------------|
| 1   10  0000 10  0   11  Zm  0   Rv  001 Zn  000 off2 |
```

#### Decode (A64.sme.mortlach_multi_array_1b.mortlach_multi1_zz_za_fp8_fma_long_long_sm.fmlall_za32_z8z8v_1)

```
if !IsFeatureImplemented(FEAT_SME_F8F32) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off2:'00');
constant integer nreg = 1;
```

#### Execute (A64.sme.mortlach_multi_array_1b.mortlach_multi1_zz_za_fp8_fma_long_long_sm.fmlall_za32_z8z8v_1)

```
CheckFPMREnabled();
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 32;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
bits(VL) result;
vec = vec - (vec MOD 4);

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[(n+r) MOD 32, VL];
    constant bits(VL) operand2 = Z[m, VL];
    for i = 0 to 3
        constant bits(VL) operand3 = ZAvector[vec + i, VL];
        for e = 0 to elements-1
            constant bits(8) element1 = Elem[operand1, 4 * e + i, 8];
            constant bits(8) element2 = Elem[operand2, 4 * e + i, 8];
            constant bits(32) element3 = Elem[operand3, e, 32];
            Elem[result, e, 32] = FP8MulAddFP(element3, element1, element2, FPCR, FPMR);
        ZAvector[vec + i, VL] = result;
    vec = vec + vstride;
```

### Variant: `Two ZA quad-vectors`
- **Assembly**: `FMLALL  ZA.S[<Wv>, <offs1>:<offs4>{, VGx2}], { <Zn1>.B-<Zn2>.B }, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4   1  0 |
|--------------------------------------------|
| 1   10  0000 10  0   10  Zm  0   Rv  000 Zn  000 1   o1  |
```

#### Decode (A64.sme.mortlach_multi_array_1a.mortlach_multi2_zz_za_fp8_fma_long_long_sm.fmlall_za32_z8z8v_2x1)

```
if !IsFeatureImplemented(FEAT_SME_F8F32) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(o1:'00');
constant integer nreg = 2;
```

### Variant: `Four ZA quad-vectors`
- **Assembly**: `FMLALL  ZA.S[<Wv>, <offs1>:<offs4>{, VGx4}], { <Zn1>.B-<Zn4>.B }, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4   1  0 |
|--------------------------------------------|
| 1   10  0000 10  0   11  Zm  0   Rv  000 Zn  000 1   o1  |
```

#### Decode (A64.sme.mortlach_multi_array_1b.mortlach_multi4_zz_za_fp8_fma_long_long_sm.fmlall_za32_z8z8v_4x1)

```
if !IsFeatureImplemented(FEAT_SME_F8F32) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(o1:'00');
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs1>` | `unknown` | `off2` | For the "One ZA quad-vector" variant: is the first vector select offset, encoded as "off2" field times 4. |
| `<offs1>` | `unknown` | `o1` | For the "Four ZA quad-vectors" and "Two ZA quad-vectors" variants: is the first vector select offset, encoded as "o1" field times 4. |
| `<offs4>` | `unknown` | `off2` | For the "One ZA quad-vector" variant: is the fourth vector select offset, encoded as "off2" field times 4 plus 3. |
| `<offs4>` | `unknown` | `o1` | For the "Four ZA quad-vectors" and "Two ZA quad-vectors" variants: is the fourth vector select offset, encoded as "o1" field times 4 plus 3. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn". |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" plus 1 modulo 32. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" plus 3 modulo 32. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F8F32)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmlall_za32_z8z8v.xml`
</details>