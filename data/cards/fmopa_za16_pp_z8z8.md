## FMOPA
_ARM A64 Instruction_

**Title**: FMOPA (widening, 2-way, FP8 to FP16) -- A64 | **Class**: `mortlach2` | **XML ID**: `fmopa_za16_pp_z8z8`

**Architecture**: `FEAT_SME_F8F16` (ARMv9.5)

**Summary**: 8-bit floating-point sum of outer products and accumulate

**Description**:
This instruction works with a 16-bit element ZA tile.

This instruction widens the SVLH×2 sub-matrix of 8-bit
floating-point values held in the first source vector to half-precision
values and multiplies it by the widened 2×SVLH
sub-matrix of 8-bit floating-point values in the second source vector
to half-precision values.

Each source vector is independently predicated by a corresponding
governing predicate. When a 8-bit source element is Inactive it is treated
as having the value +0.0, but if both groups of source vector elements
that correspond to a 16-bit destination element contain Inactive elements,
then the destination element remains unmodified.

The resulting SVLH×SVLH
half-precision sum of outer products are scaled by
2-UInt(FPMR.LSCALE[3:0]),
before being destructively added to
the half-precision destination tile.
This is equivalent to performing a downscaled 2-way dot product and accumulate
to each of the destination tile elements.

Each 16-bit container of the first source vector holds 2 consecutive
column elements of each row of a SVLH×2 sub-matrix.
Similarly, each 16-bit container of the second source vector holds
2 consecutive row elements of each column of a 2×SVLH sub-matrix.

The 8-bit floating-point encoding format for the elements of the first source vector
and the second source vector is selected by FPMR.F8S1 and FPMR.F8S2
respectively.

**Attributes**: Predicated; SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `FMOPA  <ZAda>.H, <Pn>/M, <Pm>/M, <Zn>.B, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4  3   1  0 |
|--------------------------------------------|
| 1   00  0000 0   10  1   Zm  Pm  Pn  Zn  0   10  0   ZAda |
```

#### Decode (A64.sme.mortlach2_misc_prod.mortlach_f8f16_prod.fmopa_za16_pp_z8z8_8)

```
if !IsFeatureImplemented(FEAT_SME_F8F16) then EndOfDecode(Decode_UNDEF);
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(ZAda);
```

#### Execute (A64.sme.mortlach2_misc_prod.mortlach_f8f16_prod.fmopa_za16_pp_z8z8_8)

```
CheckFPMREnabled();
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer dim = VL DIV 16;
constant bits(PL) mask1 = P[a, PL];
constant bits(PL) mask2 = P[b, PL];
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(dim*dim*16) operand3 = ZAtile[da, 16, dim*dim*16];
bits(dim*dim*16) result;

for row = 0 to dim-1
    for col = 0 to dim-1
        array [0..1] of boolean prow;
        array [0..1] of boolean pcol;
        boolean any_active = FALSE;
        for i = 0 to 1
            prow[i] = ActivePredicateElement(mask1, 2*row + i, 8);
            pcol[i] = ActivePredicateElement(mask2, 2*col + i, 8);
            any_active = any_active || (prow[i] && pcol[i]);

        if any_active then
            bits(16) sum = Elem[operand3, row*dim+col, 16];
            bits(16) rowop = Zeros(16);
            bits(16) colop = Zeros(16);
            for i = 0 to 1
                if prow[i] then
                    Elem[rowop, i, 8] = Elem[operand1, 2*row + i, 8];
                if pcol[i] then
                    Elem[colop, i, 8] = Elem[operand2, 2*col + i, 8];

            sum = FP8DotAddFP(sum, rowop, colop, FPCR, FPMR);
            Elem[result, row*dim+col, 16] = sum;
        else
            Elem[result, row*dim+col, 16] = Elem[operand3, row*dim+col, 16];

ZAtile[da, 16, dim*dim*16] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F8F16)` |

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
- source: `fmopa_za16_pp_z8z8.xml`
</details>