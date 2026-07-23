## FMLALB_advsimd_vec
_ARM A64 Instruction_

**Title**: FMLALB, FMLALT (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `FMLALB_advsimd_vec`

**Architecture**: `FEAT_FP8FMA` (ARMv9.5)

**Summary**: 8-bit floating-point multiply-add long to half-precision (vector)

**Description**:
This instruction widens the even-numbered (bottom) or odd-numbered (top)
8-bit elements in the first and second source vectors to half-precision
format and multiplies the corresponding elements. The intermediate products
are scaled by 2-UInt(FPMR.LSCALE[3:0]), before being destructively
added without intermediate rounding to the half-precision elements of the
destination vector that overlap with the corresponding 8-bit floating-point
elements in the source vectors.

The 8-bit floating-point encoding format for the elements of the first
source vector is selected by FPMR.F8S1.
The 8-bit floating-point encoding format for the elements of the second
source vector is selected by FPMR.F8S2.

### Variant: `Advanced SIMD (FMLALB_asimdsame2_J)` (FMLALB)
- **Condition**: `Q == 0`
- **Assembly**: `FMLALB  <Vd>.8H, <Vn>.16B, <Vm>.16B`
- **Fixed bits**: `Q`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15 14  10  9   4  |
|--------------------------------------|
| 0   Q   0   01110 11  0   Rm  1   1111 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame2.FMLALB_asimdsame2_J)

```
if !IsFeatureImplemented(FEAT_FP8FMA) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer elements = 128 DIV 16;
constant integer sel = UInt(Q);
```

#### Execute (A64.simd_dp.asimdsame2.FMLALB_asimdsame2_J)

```
CheckFPMREnabled(); CheckFPAdvSIMDEnabled64();
constant bits(128) operand1 = V[n, 128];
constant bits(128) operand2 = V[m, 128];
constant bits(128) operand3 = V[d, 128];
bits(128) result;

for e = 0 to elements-1
    constant bits(8)  element1 = Elem[operand1, 2 * e + sel, 8];
    constant bits(8)  element2 = Elem[operand2, 2 * e + sel, 8];
    constant bits(16) element3 = Elem[operand3, e, 16];
    Elem[result, e, 16] = FP8MulAddFP(element3, element1, element2, FPCR, FPMR);

V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP8FMA)` |

### Variant: `Advanced SIMD (FMLALT_asimdsame2_J)` (FMLALT)
- **Condition**: `Q == 1`
- **Assembly**: `FMLALT  <Vd>.8H, <Vn>.16B, <Vm>.16B`
- **Fixed bits**: `Q`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15 14  10  9   4  |
|--------------------------------------|
| 0   Q   0   01110 11  0   Rm  1   1111 1   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

---
<details><summary>Metadata</summary>

- advsimd-only: `simd-only`
- advsimd-type: `simd`
- isa: `A64`
- source: `fmlalb_advsimd_vec.xml`
</details>