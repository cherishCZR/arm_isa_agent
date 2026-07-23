## BF12CVTL_advsimd
_ARM A64 Instruction_

**Title**: BF1CVTL, BF1CVTL2, BF2CVTL, BF2CVTL2 -- A64 | **Class**: `advsimd` | **XML ID**: `BF12CVTL_advsimd`

**Architecture**: `FEAT_FP8` (ARMv9.5)

**Summary**: 8-bit floating-point convert to BFloat16 (vector)

**Description**:
This instruction converts each 8-bit floating-point element from the lower
or upper half of the source vector to BFloat16 while downscaling the value,
and places the results in the 16-bit elements of the destination vector.
BF1CVTL and BF2CVTL convert the elements from the lower half
of the source vector while scaling the values by 2-UInt(FPMR.LSCALE[5:0])
and 2-UInt(FPMR.LSCALE2[5:0]), respectively.
BF1CVTL2 and BF2CVTL2 convert the elements from the upper half
of the source vector while scaling the values by 2-UInt(FPMR.LSCALE[5:0])
and 2-UInt(FPMR.LSCALE2[5:0]), respectively.

The 8-bit floating-point encoding format for BF1CVTL and BF1CVTL2
is selected by FPMR.F8S1. The 8-bit floating-point
encoding format for BF2CVTL and BF2CVTL2 is selected by
FPMR.F8S2.

### Variant: `Advanced SIMD (BF1CVTL_asimdmisc_V)` (BF1CVTL{2})
- **Condition**: `size == 10`
- **Assembly**: `BF1CVTL{2}  <Vd>.8H, <Vn>.<Ta>`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  11   9   4  |
|--------------------------------|
| 0   Q   1   01110 1x  10000 10111 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.BF1CVTL_asimdmisc_V)

```
if !IsFeatureImplemented(FEAT_FP8) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer part = UInt(Q);
constant integer elements = 64 DIV 8;
constant boolean issrc2 = size == '11';
```

#### Execute (A64.simd_dp.asimdmisc.BF1CVTL_asimdmisc_V)

```
CheckFPMREnabled(); CheckFPAdvSIMDEnabled64();
constant bits(64) operand = Vpart[n, part, 64];
bits(128) result;

for e = 0 to elements-1
    Elem[result, e, 16] = FP8ConvertBF(Elem[operand, e, 8], issrc2, FPCR, FPMR);

V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP8)` |

### Variant: `Advanced SIMD (BF2CVTL_asimdmisc_V)` (BF2CVTL{2})
- **Condition**: `size == 11`
- **Assembly**: `BF2CVTL{2}  <Vd>.8H, <Vn>.<Ta>`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  11   9   4  |
|--------------------------------|
| 0   Q   1   01110 1x  10000 10111 10  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Ta>` | `unknown` | `Q` | Is an arrangement specifier, |

**2 Value Table**:

| bitfield | symbol |
|---|---|
| 0 | [absent] |
| 1 | [present] |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |

---
<details><summary>Metadata</summary>

- advsimd-only: `simd-only`
- advsimd-type: `simd`
- isa: `A64`
- source: `bf12cvtl_advsimd.xml`
</details>