## BFADD
_ARM A64 Instruction_

**Title**: BFADD -- A64 | **Class**: `mortlach2` | **XML ID**: `bfadd_za_zw`

**Architecture**: `FEAT_SME_B16B16` (ARMv9.4)

**Summary**: BFloat16 add multi-vector to ZA array vector accumulators

**Description**:
This instruction destructively adds all elements of the two or four source vectors to the corresponding BFloat16 elements of the ZA single-vector groups.

The single-vector
group within each half of or each quarter of the ZA array is selected by the sum
of the vector select register and offset, modulo half or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA single-vector
groups
respectively. The vector group symbol is preferred
for disassembly, but optional in assembler source code.

This instruction follows SME2 ZA-targeting non-widening BFloat16
numerical behaviors.

This instruction is unpredicated.

ID_AA64SMFR0_EL1.B16B16 indicates whether this instruction is implemented.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Two ZA single-vectors`
- **Assembly**: `BFADD  ZA.H[<Wv>, <offs>{, VGx2}], { <Zm1>.H-<Zm2>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  18  16  14  12   9   5  4  3  2  |
|--------------------------------------------------|
| 1   10  0000 11  1   1   00  10  00  Rv  111 Zm  0   0   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_2a.mortlach_multi2_z_za_f16_mm.bfadd_za_zw_2x2_16)

```
if !IsFeatureImplemented(FEAT_SME_B16B16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer m = UInt(Zm:'0');
constant integer offset = UInt(off3);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_array_2a.mortlach_multi2_z_za_f16_mm.bfadd_za_zw_2x2_16)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
bits(VL) result;

for r = 0 to nreg-1
    constant bits(VL) operand1 = ZAvector[vec, VL];
    constant bits(VL) operand2 = Z[m+r, VL];
    for e = 0 to elements-1
        constant bits(16) element1 = Elem[operand1, e, 16];
        constant bits(16) element2 = Elem[operand2, e, 16];
        Elem[result, e, 16] = BFAdd_ZA(element1, element2, FPCR);
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

### Variant: `Four ZA single-vectors`
- **Assembly**: `BFADD  ZA.H[<Wv>, <offs>{, VGx4}], { <Zm1>.H-<Zm4>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  18  16  14  12   9   6   4  3  2  |
|--------------------------------------------------|
| 1   10  0000 11  1   1   00  10  10  Rv  111 Zm  00  0   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_2b.mortlach_multi4_z_za_f16_mm.bfadd_za_zw_4x4_16)

```
if !IsFeatureImplemented(FEAT_SME_B16B16) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer m = UInt(Zm:'00');
constant integer offset = UInt(off3);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Two ZA single-vectors" variant: is the name of the first scalable vector register of the source multi-vector group, encoded as "Zm" times 2. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Four ZA single-vectors" variant: is the name of the first scalable vector register of the source multi-vector group, encoded as "Zm" times 4. |
| `<Zm2>` | `register (128-bit)` | `Zm` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zm" times 2 plus 1. |
| `<Zm4>` | `register (128-bit)` | `Zm` | Is the name of the fourth scalable vector register of the source multi-vector group, encoded as "Zm" times 4 plus 3. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_B16B16)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfadd_za_zw.xml`
</details>