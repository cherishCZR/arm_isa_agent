## FDOT
_ARM A64 Instruction_

**Title**: FDOT (4-way, multiple and single vector) -- A64 | **Class**: `mortlach2` | **XML ID**: `fdot_za32_z8z8v`

**Architecture**: `FEAT_SME_F8F32` (ARMv9.5)

**Summary**: Multi-vector 8-bit floating-point dot-product by vector to single-precision

**Description**:
This instruction computes the fused sum-of-products of a group of four 8-bit floating-point values
held in the corresponding 32-bit elements of the two or four first source vectors
and the second source vector.
The single-precision sum-of-products are scaled by 2-UInt(FPMR.LSCALE),
before being destructively added without intermediate rounding to the corresponding single-precision elements
of the ZA single-vector groups.
The 8-bit floating-point encoding format for the elements of the first source vector
and the second source vector is selected by FPMR.F8S1 and FPMR.F8S2
respectively.

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
- **Assembly**: `FDOT  ZA.S[<Wv>, <offs>{, VGx2}], { <Zn1>.B-<Zn2>.B }, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4   2  |
|-----------------------------------------|
| 1   10  0000 10  0   10  Zm  0   Rv  100 Zn  11  off3 |
```

#### Decode (A64.sme.mortlach_multi_array_1a.mortlach_multi2_z_za_fpdot_sm.fdot_za32_z8z8v_2x1)

```
if !IsFeatureImplemented(FEAT_SME_F8F32) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_array_1a.mortlach_multi2_z_za_fpdot_sm.fdot_za32_z8z8v_2x1)

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

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[(n+r) MOD 32, VL];
    constant bits(VL) operand2 = Z[m, VL];
    constant bits(VL) operand3 = ZAvector[vec, VL];
    for e = 0 to elements-1
        constant bits(32) op1 = Elem[operand1, e, 32];
        constant bits(32) op2 = Elem[operand2, e, 32];
        bits(32) sum = Elem[operand3, e, 32];
        sum = FP8DotAddFP(sum, op1, op2, FPCR, FPMR);
        Elem[result, e, 32] = sum;
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

### Variant: `Four ZA single-vectors`
- **Assembly**: `FDOT  ZA.S[<Wv>, <offs>{, VGx4}], { <Zn1>.B-<Zn4>.B }, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4   2  |
|-----------------------------------------|
| 1   10  0000 10  0   11  Zm  0   Rv  100 Zn  11  off3 |
```

#### Decode (A64.sme.mortlach_multi_array_1b.mortlach_multi4_z_za_fpdot_sm.fdot_za32_z8z8v_4x1)

```
if !IsFeatureImplemented(FEAT_SME_F8F32) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn". |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" plus 1 modulo 32. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" plus 3 modulo 32. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F8F32)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fdot_za32_z8z8v.xml`
</details>