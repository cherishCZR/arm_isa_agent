## F12CVTL_advsimd
_ARM A64 Instruction_

**Title**: F1CVTL, F1CVTL2, F2CVTL, F2CVTL2 -- A64 | **Class**: `advsimd` | **XML ID**: `F12CVTL_advsimd`

**Architecture**: `FEAT_FP8` (ARMv9.5)

**Summary**: 8-bit floating-point convert to half-precision (vector)

**Description**:
This instruction converts each 8-bit floating-point element from the lower
or upper half of the source vector to half-precision while downscaling the value,
and places the results in the 16-bit elements of the destination vector.
F1CVTL and F2CVTL convert the elements from the lower half
of the source vector while scaling the values by 2-UInt(FPMR.LSCALE[3:0])
and 2-UInt(FPMR.LSCALE2[3:0]), respectively.
F1CVTL2 and F2CVTL2 convert the elements from the upper half
of the source vector while scaling the values by 2-UInt(FPMR.LSCALE[3:0])
and 2-UInt(FPMR.LSCALE2[3:0]), respectively.

The 8-bit floating-point encoding format for F1CVTL and F1CVTL2
is selected by FPMR.F8S1. The 8-bit floating-point
encoding format for F2CVTL and F2CVTL2 is selected by
FPMR.F8S2.

### Variant: `Advanced SIMD (F1CVTL_asimdmisc_V)` (F1CVTL{2})
- **Condition**: `size == 00`
- **Assembly**: `F1CVTL{2}  <Vd>.8H, <Vn>.<Ta>`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  11   9   4  |
|--------------------------------|
| 0   Q   1   01110 0x  10000 10111 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.F1CVTL_asimdmisc_V)

```
if !IsFeatureImplemented(FEAT_FP8) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Rn);
constant integer d = UInt(Rd);
constant integer part = UInt(Q);
constant integer elements = 64 DIV 8;
constant boolean issrc2 = size == '01';
```

#### Execute (A64.simd_dp.asimdmisc.F1CVTL_asimdmisc_V)

```
CheckFPMREnabled(); CheckFPAdvSIMDEnabled64();
constant bits(64) operand = Vpart[n, part, 64];
bits(128) result;

for e = 0 to elements-1
    Elem[result, e, 16] = FP8ConvertFP(Elem[operand, e, 8], issrc2, FPCR, FPMR);

V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP8)` |

### Variant: `Advanced SIMD (F2CVTL_asimdmisc_V)` (F2CVTL{2})
- **Condition**: `size == 01`
- **Assembly**: `F2CVTL{2}  <Vd>.8H, <Vn>.<Ta>`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  11   9   4  |
|--------------------------------|
| 0   Q   1   01110 0x  10000 10111 10  Rn  Rd  |
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
- source: `f12cvtl_advsimd.xml`
</details>