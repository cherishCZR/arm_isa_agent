## FMLALLTT
_ARM A64 Instruction_

**Title**: FMLALLTT (vectors) -- A64 | **Class**: `sve2` | **XML ID**: `fmlalltt_z32_z8z8z8`

**Architecture**: `(FEAT_SVE2 && FEAT_FP8FMA) || FEAT_SSVE_FP8FMA` ((FEAT_SVE2 && FEAT_FP8FMA) || FEAT_SSVE_FP8FMA)

**Summary**: 8-bit floating-point multiply-add long long to single-precision (top top)

**Description**:
This 8-bit floating-point multiply-add long-long instruction widens the fourth 8-bit element of each 32-bit container
in the first and second source vectors
to single-precision format and
multiplies the corresponding elements. The intermediate products are scaled by
2-UInt(FPMR.LSCALE) before
being destructively added
without intermediate rounding to the single-precision elements of the destination vector
that overlap with the corresponding 8-bit floating-point elements in the
source vectors.
The 8-bit floating-point encoding format for the elements of the first source vector
and the second source vector is selected by FPMR.F8S1 and FPMR.F8S2
respectively.

This instruction is unpredicated.

### Variant: `SVE2`
- **Assembly**: `FMLALLTT  <Zda>.S, <Zn>.B, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22  20  15  13  11   9   4  |
|-----------------------------------|
| 011 0010 0   0   01  Zm  10  11  10  Zn  Zda |
```

#### Decode (A64.sve.sve_fp8_fma_w.sve_fp8_fma_long_long.fmlalltt_z32_z8z8z8_)

```
if !HaveSVE2FP8FMA() then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Execute (A64.sve.sve_fp8_fma_w.sve_fp8_fma_long_long.fmlalltt_z32_z8z8z8_)

```
CheckFPMREnabled();
if IsFeatureImplemented(FEAT_SSVE_FP8FMA) && IsFeatureImplemented(FEAT_FP8FMA) then
    CheckSVEEnabled();
elsif IsFeatureImplemented(FEAT_FP8FMA) then
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
    constant bits(8) element1 = Elem[operand1, 4 * e + 3, 8];
    constant bits(8) element2 = Elem[operand2, 4 * e + 3, 8];
    constant bits(32) element3 = Elem[operand3, e, 32];
    Elem[result, e, 32] = FP8MulAddFP(element3, element1, element2, FPCR, FPMR);

Z[da, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `!HaveSVE2FP8FMA()` |

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
- source: `fmlalltt_z32_z8z8z8.xml`
</details>