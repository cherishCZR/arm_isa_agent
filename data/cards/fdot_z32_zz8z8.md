## FDOT
_ARM A64 Instruction_

**Title**: FDOT (4-way, vectors) -- A64 | **Class**: `sve2` | **XML ID**: `fdot_z32_zz8z8`

**Architecture**: `(FEAT_SVE2 && FEAT_FP8DOT4) || FEAT_SSVE_FP8DOT4` ((FEAT_SVE2 && FEAT_FP8DOT4) || FEAT_SSVE_FP8DOT4)

**Summary**: 8-bit floating-point dot product to single-precision

**Description**:
This instruction computes the fused sum-of-products of a group of
four 8-bit floating-point values held in each 32-bit element
of the first source and second source vectors. The single-precision sum-of-products
are scaled by 2-UInt(FPMR.LSCALE),
before being destructively added without intermediate rounding to the corresponding
single-precision elements of the destination vector.

The 8-bit floating-point encoding format for the elements of the first source vector
and the second source vector is selected by FPMR.F8S1 and FPMR.F8S2
respectively.

This instruction is unpredicated.

### Variant: `SVE2`
- **Assembly**: `FDOT  <Zda>.S, <Zn>.B, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  15  13 12  10  9   4  |
|-----------------------------------------|
| 011 0010 0   0   1   1   Zm  10  0   00  1   Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fma_w.sve_fp_fdot.fdot_z32_zz8z8_)

```
if !HaveSVE2FP8DOT4() then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Execute (A64.sve.sve_fp_fma_w.sve_fp_fdot.fdot_z32_zz8z8_)

```
CheckFPMREnabled();
if IsFeatureImplemented(FEAT_SSVE_FP8DOT4) && IsFeatureImplemented(FEAT_FP8DOT4) then
    CheckSVEEnabled();
elsif IsFeatureImplemented(FEAT_FP8DOT4) then
    CheckNonStreamingSVEEnabled();
else
    CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 32;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(32) op1 = Elem[operand1, e, 32];
    constant bits(32) op2 = Elem[operand2, e, 32];
    bits(32) sum  = Elem[operand3, e, 32];

    sum = FP8DotAddFP(sum, op1, op2, FPCR, FPMR);
    Elem[result, e, 32] = sum;

Z[da, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `!HaveSVE2FP8DOT4()` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fdot_z32_zz8z8.xml`
</details>