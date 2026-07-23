## FMLA
_ARM A64 Instruction_

**Title**: FMLA (multiple and single vector) -- A64 | **Class**: `mortlach2` | **XML ID**: `fmla_za_zzv`

**Architecture**: `FEAT_SME2` (ARMv9.3), `FEAT_SME_F16F16` (ARMv9.4)

**Summary**: Multi-vector floating-point fused multiply-add by vector

**Description**:
This instruction multiplies the corresponding floating-point elements of the two or four first source vector
with corresponding elements of the second source vector and destructively adds these values without intermediate rounding to the corresponding elements of the ZA single-vector groups.

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

### Variant: `Two ZA single-vectors`
- **Assembly**: `FMLA  ZA.<T>[<Wv>, <offs>{, VGx2}], { <Zn1>.<T>-<Zn2>.<T> }, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4  3  2  |
|--------------------------------------------|
| 1   10  0000 10  sz  10  Zm  0   Rv  110 Zn  0   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_1a.mortlach_multi2_zz_za_float_sm.fmla_za_zzv_2x1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if sz == '1' && !IsFeatureImplemented(FEAT_SME_F64F64) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 32 << UInt(sz);
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_array_1a.mortlach_multi2_zz_za_float_sm.fmla_za_zzv_2x1)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
bits(VL) result;

for r = 0 to nreg-1
    constant bits(VL) op1 = Z[(n+r) MOD 32, VL];
    constant bits(VL) op2 = Z[m, VL];
    constant bits(VL) op3 = ZAvector[vec, VL];
    for e = 0 to elements-1
        constant bits(esize) elem1 = Elem[op1, e, esize];
        constant bits(esize) elem2 = Elem[op2, e, esize];
        constant bits(esize) elem3 = Elem[op3, e, esize];
        Elem[result, e, esize] = FPMulAdd_ZA(elem3, elem1, elem2, FPCR);
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

### Variant: `Two ZA single-vectors of half-precision elements`
- **Assembly**: `FMLA  ZA.H[<Wv>, <offs>{, VGx2}], { <Zn1>.H-<Zn2>.H }, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4  3  2  |
|--------------------------------------------|
| 1   10  0000 10  0   10  Zm  0   Rv  111 Zn  0   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_1a.mortlach_multi2_zz_za_f16_sm.fmla_za_zzv_2x1_16)

```
if !IsFeatureImplemented(FEAT_SME_F16F16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 16;
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer nreg = 2;
```

### Variant: `Four ZA single-vectors`
- **Assembly**: `FMLA  ZA.<T>[<Wv>, <offs>{, VGx4}], { <Zn1>.<T>-<Zn4>.<T> }, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4  3  2  |
|--------------------------------------------|
| 1   10  0000 10  sz  11  Zm  0   Rv  110 Zn  0   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_1b.mortlach_multi4_zz_za_float_sm.fmla_za_zzv_4x1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if sz == '1' && !IsFeatureImplemented(FEAT_SME_F64F64) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 32 << UInt(sz);
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer nreg = 4;
```

### Variant: `Four ZA single-vectors of half-precision elements`
- **Assembly**: `FMLA  ZA.H[<Wv>, <offs>{, VGx4}], { <Zn1>.H-<Zn4>.H }, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4  3  2  |
|--------------------------------------------|
| 1   10  0000 10  0   11  Zm  0   Rv  111 Zn  0   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_1b.mortlach_multi4_zz_za_f16_sm.fmla_za_zzv_4x1_16)

```
if !IsFeatureImplemented(FEAT_SME_F16F16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 16;
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<T>` | `unknown` | `sz` | Is the size specifier, |
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn". |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" plus 1 modulo 32. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" plus 3 modulo 32. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

### Encoding Constraints
_3× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |
| 🔒 FEATURE_GATE | `sz != '1' \|\| IsFeatureImplemented(FEAT_SME_F64F64)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F16F16)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmla_za_zzv.xml`
</details>