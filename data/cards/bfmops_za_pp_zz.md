## BFMOPS
_ARM A64 Instruction_

**Title**: BFMOPS (non-widening) -- A64 | **Class**: `mortlach2` | **XML ID**: `bfmops_za_pp_zz`

**Architecture**: `FEAT_SME_B16B16` (ARMv9.4)

**Summary**: BFloat16 outer product and subtract

**Description**:
This instruction works with a 16-bit element ZA tile.

This instruction generates an outer product of the first source
vector and the second source vector.
The first source is SVLH×1
vector and the second source is 1×SVLH vector.

Each source vector is independently predicated by a corresponding governing predicate.
When either source vector element is Inactive
the corresponding destination tile element remains unmodified.

The resulting outer product, SVLH×SVLH, is then destructively
subtracted from the destination tile.
This is equivalent to performing a single multiply-subtract
from each of the destination tile elements.

This instruction follows SME2 ZA-targeting non-widening BFloat16
numerical behaviors.

ID_AA64SMFR0_EL1.B16B16 indicates whether this instruction is implemented.

**Attributes**: Predicated; SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `BFMOPS  <ZAda>.H, <Pn>/M, <Pm>/M, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4  3   1  0 |
|--------------------------------------------|
| 1   00  0000 1   10  1   Zm  Pm  Pn  Zn  1   10  0   ZAda |
```

#### Decode (A64.sme.mortlach2_misc_prod.mortlach_b16b16_prod.bfmops_za_pp_zz_16)

```
if !IsFeatureImplemented(FEAT_SME_B16B16) then EndOfDecode(Decode_UNDEF);
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(ZAda);
```

#### Execute (A64.sme.mortlach2_misc_prod.mortlach_b16b16_prod.bfmops_za_pp_zz_16)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer dim = VL DIV 16;
constant bits(PL) mask1 = P[a, PL];
constant bits(PL) mask2 = P[b, PL];
constant bits(VL) op1 = Z[n, VL];
constant bits(VL) op2 = Z[m, VL];
constant bits(dim*dim*16) op3 = ZAtile[da, 16, dim*dim*16];
bits(dim*dim*16) result;

for row = 0 to dim-1
    for col = 0 to dim-1
        constant bits(16) elem2 = Elem[op2, col, 16];
        constant bits(16) elem3 = Elem[op3, row*dim+col, 16];

        if ActivePredicateElement(mask1, row, 16) && ActivePredicateElement(mask2, col, 16) then
            constant bits(16) elem1 = BFNeg(Elem[op1, row, 16]);
            Elem[result, row*dim+col, 16] = BFMulAdd_ZA(elem3, elem1, elem2, FPCR);
        else
            Elem[result, row*dim+col, 16] = elem3;

ZAtile[da, 16, dim*dim*16] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_B16B16)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<ZAda>` | `register (128-bit)` | `ZAda` | Is the name of the ZA tile ZA0-ZA1, encoded in the "ZAda" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the first governing scalable predicate register P0-P7, encoded in the "Pn" field. |
| `<Pm>` | `unknown` | `Pm` | Is the name of the second governing scalable predicate register P0-P7, encoded in the "Pm" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfmops_za_pp_zz.xml`
</details>