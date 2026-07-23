## FADD
_ARM A64 Instruction_

**Title**: FADD -- A64 | **Class**: `mortlach2` | **XML ID**: `fadd_za_zw`

**Architecture**: `FEAT_SME2` (ARMv9.3), `FEAT_SME_F16F16 || FEAT_SME_F8F16` (FEAT_SME_F16F16 || FEAT_SME_F8F16)

**Summary**: Floating-point add multi-vector to ZA array vector accumulators

**Description**:
This instruction destructively adds all elements of the two or four source vectors to the corresponding elements of the ZA single-vector groups.

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
- **Assembly**: `FADD  ZA.<T>[<Wv>, <offs>{, VGx2}], { <Zm1>.<T>-<Zm2>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  18  16  14  12   9   5  4  3  2  |
|--------------------------------------------------|
| 1   10  0000 11  sz  1   00  00  00  Rv  111 Zm  0   0   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_2a.mortlach_multi2_z_za_float_mm.fadd_za_zw_2x2)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if sz == '1' && !IsFeatureImplemented(FEAT_SME_F64F64) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 32 << UInt(sz);
constant integer m = UInt(Zm:'0');
constant integer offset = UInt(off3);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_array_2a.mortlach_multi2_z_za_float_mm.fadd_za_zw_2x2)

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
    constant bits(VL) operand1 = ZAvector[vec, VL];
    constant bits(VL) operand2 = Z[m+r, VL];
    for e = 0 to elements-1
        constant bits(esize) element1 = Elem[operand1, e, esize];
        constant bits(esize) element2 = Elem[operand2, e, esize];
        Elem[result, e, esize] = FPAdd_ZA(element1, element2, FPCR);
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

### Variant: `Two ZA single-vectors of half-precision elements`
- **Assembly**: `FADD  ZA.H[<Wv>, <offs>{, VGx2}], { <Zm1>.H-<Zm2>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  18  16  14  12   9   5  4  3  2  |
|--------------------------------------------------|
| 1   10  0000 11  0   1   00  10  00  Rv  111 Zm  0   0   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_2a.mortlach_multi2_z_za_f16_mm.fadd_za_zw_2x2_16)

```
if !IsFeatureImplemented(FEAT_SME_F16F16) && !IsFeatureImplemented(FEAT_SME_F8F16) then
    EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 16;
constant integer m = UInt(Zm:'0');
constant integer offset = UInt(off3);
constant integer nreg = 2;
```

### Variant: `Four ZA single-vectors`
- **Assembly**: `FADD  ZA.<T>[<Wv>, <offs>{, VGx4}], { <Zm1>.<T>-<Zm4>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  18  16  14  12   9   6   4  3  2  |
|--------------------------------------------------|
| 1   10  0000 11  sz  1   00  00  10  Rv  111 Zm  00  0   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_2b.mortlach_multi4_z_za_float_mm.fadd_za_zw_4x4)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if sz == '1' && !IsFeatureImplemented(FEAT_SME_F64F64) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 32 << UInt(sz);
constant integer m = UInt(Zm:'00');
constant integer offset = UInt(off3);
constant integer nreg = 4;
```

### Variant: `Four ZA single-vectors of half-precision elements`
- **Assembly**: `FADD  ZA.H[<Wv>, <offs>{, VGx4}], { <Zm1>.H-<Zm4>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  18  16  14  12   9   6   4  3  2  |
|--------------------------------------------------|
| 1   10  0000 11  0   1   00  10  10  Rv  111 Zm  00  0   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_2b.mortlach_multi4_z_za_f16_mm.fadd_za_zw_4x4_16)

```
if !IsFeatureImplemented(FEAT_SME_F16F16) && !IsFeatureImplemented(FEAT_SME_F8F16) then
    EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 16;
constant integer m = UInt(Zm:'00');
constant integer offset = UInt(off3);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<T>` | `unknown` | `sz` | Is the size specifier, |
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Two ZA single-vectors of half-precision elements" and "Two ZA single-vectors" variants: is the name of the first scalable vector register of  |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Four ZA single-vectors of half-precision elements" and "Four ZA single-vectors" variants: is the name of the first scalable vector register o |
| `<Zm2>` | `register (128-bit)` | `Zm` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zm" times 2 plus 1. |
| `<Zm4>` | `register (128-bit)` | `Zm` | Is the name of the fourth scalable vector register of the source multi-vector group, encoded as "Zm" times 4 plus 3. |

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
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F16F16) \|\| IsFeatureImplemented(FEAT_SME_F8F16)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fadd_za_zw.xml`
</details>