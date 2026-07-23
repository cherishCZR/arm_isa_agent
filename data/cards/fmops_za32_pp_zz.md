## FMOPS
_ARM A64 Instruction_

**Title**: FMOPS (widening) -- A64 | **Class**: `mortlach` | **XML ID**: `fmops_za32_pp_zz`

**Architecture**: `FEAT_SME` (PROFILE_A)

**Summary**: Half-precision sum of outer products and subtract

**Description**:
This instruction works with a 32-bit element ZA tile.

This instruction widens the SVLS×2 sub-matrix of half-precision
values held in the first source vector to single-precision
values and multiplies it by the widened 2×SVLS
sub-matrix of half-precision values in the second source vector
to single-precision values.

Each source vector is independently predicated by a corresponding
governing predicate. When a 16-bit source element is Inactive it is treated
as having the value +0.0, but if both pairs of source vector elements
that correspond to a 32-bit destination element contain Inactive elements,
then the destination element remains unmodified.

The resulting SVLS×SVLS single-precision sum of outer
products is then destructively subtracted from the single-precision
destination tile.
This is equivalent to performing a 2-way dot product and subtract
from each of the destination tile elements.

Each 32-bit container of the first source vector holds 2 consecutive
column elements of each row of a SVLS×2 sub-matrix.
Similarly, each 32-bit container of the second source vector holds
2 consecutive row elements of each column of a 2×SVLS sub-matrix.

This instruction follows SME ZA-targeting floating-point behaviors.

**Attributes**: Predicated; SM Policy: `SM_1_only`

### Variant: `SME`
- **Assembly**: `FMOPS  <ZAda>.S, <Pn>/M, <Pm>/M, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4  3   1  |
|-----------------------------------------|
| 1   00  0000 1   10  1   Zm  Pm  Pn  Zn  1   00  ZAda |
```

#### Decode (A64.sme.mortlach_32bit_fp_prod.mortlach_f16f32_prod.fmops_za32_pp_zz_16)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(ZAda);
```

#### Execute (A64.sme.mortlach_32bit_fp_prod.mortlach_f16f32_prod.fmops_za32_pp_zz_16)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer dim = VL DIV 32;
constant bits(PL) mask1 = P[a, PL];
constant bits(PL) mask2 = P[b, PL];
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(dim*dim*32) operand3 = ZAtile[da, 32, dim*dim*32];
bits(dim*dim*32) result;

for row = 0 to dim-1
    for col = 0 to dim-1
        // determine row/col predicates
        constant boolean prow_0 = (ActivePredicateElement(mask1, 2*row + 0, 16));
        constant boolean prow_1 = (ActivePredicateElement(mask1, 2*row + 1, 16));
        constant boolean pcol_0 = (ActivePredicateElement(mask2, 2*col + 0, 16));
        constant boolean pcol_1 = (ActivePredicateElement(mask2, 2*col + 1, 16));

        bits(32) sum = Elem[operand3, row*dim+col, 32];
        if (prow_0 && pcol_0) || (prow_1 && pcol_1) then
            bits(16) erow_0 = (if prow_0 then Elem[operand1, 2*row + 0, 16] else FPZero('0', 16));
            bits(16) erow_1 = (if prow_1 then Elem[operand1, 2*row + 1, 16] else FPZero('0', 16));
            constant bits(16) ecol_0 = (if pcol_0 then Elem[operand2, 2*col + 0, 16]
                                        else FPZero('0', 16));
            constant bits(16) ecol_1 = (if pcol_1 then Elem[operand2, 2*col + 1, 16]
                                        else FPZero('0', 16));
            if prow_0 then erow_0 = FPNeg(erow_0, FPCR);
            if prow_1 then erow_1 = FPNeg(erow_1, FPCR);
            sum = FPDotAdd_ZA(sum, erow_0, erow_1, ecol_0, ecol_1, FPCR);

        Elem[result, row*dim+col, 32] = sum;

ZAtile[da, 32, dim*dim*32] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<ZAda>` | `register (128-bit)` | `ZAda` | Is the name of the ZA tile ZA0-ZA3, encoded in the "ZAda" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the first governing scalable predicate register P0-P7, encoded in the "Pn" field. |
| `<Pm>` | `unknown` | `Pm` | Is the name of the second governing scalable predicate register P0-P7, encoded in the "Pm" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmops_za32_pp_zz.xml`
</details>