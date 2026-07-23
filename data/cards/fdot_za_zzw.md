## FDOT
_ARM A64 Instruction_

**Title**: FDOT (2-way, multiple vectors, FP16 to FP32) -- A64 | **Class**: `mortlach2` | **XML ID**: `fdot_za_zzw`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector half-precision dot-product

**Description**:
This instruction computes the fused sum-of-products of a pair of half-precision values
held in the corresponding 32-bit elements of the two or four first and second source vectors,
without intermediate rounding. The single-precision sum-of-products are destructively added
to the corresponding single-precision elements of the ZA single-vector groups.

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

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two ZA single-vectors`
- **Assembly**: `FDOT  ZA.S[<Wv>, <offs>{, VGx2}], { <Zn1>.H-<Zn2>.H }, { <Zm1>.H-<Zm2>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  16  14  12   9   5   3  2  |
|--------------------------------------------|
| 1   10  0000 11  0   1   Zm  00  Rv  100 Zn  00  0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_2a.mortlach_multi2_z_za_fpdot_mm.fdot_za_zzw_2x2)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'0');
constant integer m = UInt(Zm:'0');
constant integer offset = UInt(off3);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_array_2a.mortlach_multi2_z_za_fpdot_mm.fdot_za_zzw_2x2)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 32;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
bits(VL) result;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[n+r, VL];
    constant bits(VL) operand2 = Z[m+r, VL];
    constant bits(VL) operand3 = ZAvector[vec, VL];
    for e = 0 to elements-1
        constant bits(16) elt1_a = Elem[operand1, 2 * e + 0, 16];
        constant bits(16) elt1_b = Elem[operand1, 2 * e + 1, 16];
        constant bits(16) elt2_a = Elem[operand2, 2 * e + 0, 16];
        constant bits(16) elt2_b = Elem[operand2, 2 * e + 1, 16];
        bits(32) sum = Elem[operand3, e, 32];
        sum = FPDotAdd_ZA(sum, elt1_a, elt1_b, elt2_a, elt2_b, FPCR);
        Elem[result, e, 32] = sum;
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

### Variant: `Four ZA single-vectors`
- **Assembly**: `FDOT  ZA.S[<Wv>, <offs>{, VGx4}], { <Zn1>.H-<Zn4>.H }, { <Zm1>.H-<Zm4>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  17 16  14  12   9   6  5   3  2  |
|--------------------------------------------------|
| 1   10  0000 11  0   1   Zm  0   10  Rv  100 Zn  0   00  0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_2b.mortlach_multi4_z_za_fpdot_mm.fdot_za_zzw_4x4)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'00');
constant integer m = UInt(Zm:'00');
constant integer offset = UInt(off3);
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
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Two ZA single-vectors" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" ti |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Four ZA single-vectors" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" t |
| `<Zm2>` | `register (128-bit)` | `Zm` | Is the name of the second scalable vector register of the second source multi-vector group, encoded as "Zm" times 2 plus 1. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" times 4 plus 3. |
| `<Zm4>` | `register (128-bit)` | `Zm` | Is the name of the fourth scalable vector register of the second source multi-vector group, encoded as "Zm" times 4 plus 3. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fdot_za_zzw.xml`
</details>