## FMLALB_advsimd_elem
_ARM A64 Instruction_

**Title**: FMLALB, FMLALT (by element) -- A64 | **Class**: `advsimd` | **XML ID**: `FMLALB_advsimd_elem`

**Architecture**: `FEAT_FP8FMA` (ARMv9.5)

**Summary**: 8-bit floating-point multiply-add long to half-precision (vector, by element)

**Description**:
This instruction widens the even-numbered (bottom) or odd-numbered (top)
8-bit elements in the first source vector and the indexed element from the
second source vector to half-precision format and multiplies the corresponding
elements. The intermediate products are scaled by 2-UInt(FPMR.LSCALE[3:0]),
before being destructively added without intermediate rounding to the
half-precision elements of the destination vector that overlap with the
corresponding 8-bit floating-point elements in the first source vector.

The 8-bit floating-point encoding format for the elements of the first
source vector is selected by FPMR.F8S1.
The 8-bit floating-point encoding format for the elements of the second
source vector is selected by FPMR.F8S2.

### Variant: `Advanced SIMD (FMLALB_asimdelem_H)` (FMLALB)
- **Condition**: `Q == 0`
- **Assembly**: `FMLALB  <Vd>.8H, <Vn>.16B, <Vm>.B[<index>]`
- **Fixed bits**: `Q`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20 19  15  11 10  9   4  |
|-----------------------------------------|
| 0   Q   0   01111 11  L   M   Rm  0000 H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.FMLALB_asimdelem_H)

```
if !IsFeatureImplemented(FEAT_FP8FMA) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Rn);
constant integer m = UInt('00':Rm<2:0>);
constant integer d = UInt(Rd);
constant integer index = UInt(H:L:M:Rm<3>);
constant integer elements = 128 DIV 16;
constant integer sel = UInt(Q);
```

#### Execute (A64.simd_dp.asimdelem.FMLALB_asimdelem_H)

```
CheckFPMREnabled(); CheckFPAdvSIMDEnabled64();
constant bits(128) operand1 = V[n, 128];
constant bits(128) operand2 = V[m, 128];
constant bits(128) operand3 = V[d, 128];
bits(128) result;

for e = 0 to elements-1
    constant bits(8)  element1 = Elem[operand1, 2 * e + sel, 8];
    constant bits(8)  element2 = Elem[operand2, index, 8];
    constant bits(16) element3 = Elem[operand3, e, 16];
    Elem[result, e, 16] = FP8MulAddFP(element3, element1, element2, FPCR, FPMR);

V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP8FMA)` |

### Variant: `Advanced SIMD (FMLALT_asimdelem_H)` (FMLALT)
- **Condition**: `Q == 1`
- **Assembly**: `FMLALT  <Vd>.8H, <Vn>.16B, <Vm>.B[<index>]`
- **Fixed bits**: `Q`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20 19  15  11 10  9   4  |
|-----------------------------------------|
| 0   Q   0   01111 11  L   M   Rm  0000 H   0   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, in the range V0 to V7, encoded in the "Rm<2:0>" field. |
| `<index>` | `unknown` | `H:L:M:Rm` | Is the element index, in the range 0 to 15, encoded in the "H:L:M:Rm<3>" fields. |

---
<details><summary>Metadata</summary>

- advsimd-only: `simd-only`
- advsimd-reguse: `2reg-element`
- isa: `A64`
- source: `fmlalb_advsimd_elem.xml`
</details>