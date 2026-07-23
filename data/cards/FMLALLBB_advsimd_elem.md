## FMLALLBB_advsimd_elem
_ARM A64 Instruction_

**Title**: FMLALLBB, FMLALLBT, FMLALLTB, FMLALLTT (by element) -- A64 | **Class**: `advsimd` | **XML ID**: `FMLALLBB_advsimd_elem`

**Architecture**: `FEAT_FP8FMA` (ARMv9.5)

**Summary**: 8-bit floating-point multiply-add long-long to single-precision (vector, by element)

**Description**:
This instruction widens the first (bottom bottom), second (bottom top),
third (top bottom), or fourth (top top) 8-bit element of each 32-bit
container in the first source vector and the indexed element from the
second source vector to single-precision format and multiplies the corresponding
elements. The intermediate products are scaled by 2-UInt(FPMR.LSCALE),
before being destructively added without intermediate rounding to the
single-precision elements of the destination vector that overlap with the
corresponding 8-bit floating-point elements in the first source vector.

The 8-bit floating-point encoding format for the elements of the first
source vector is selected by FPMR.F8S1.
The 8-bit floating-point encoding format for the elements of the second
source vector is selected by FPMR.F8S2.

### Variant: `Advanced SIMD (FMLALLBB_asimdelem_J)` (FMLALLBB)
- **Condition**: `Q == 0 && size == 00`
- **Assembly**: `FMLALLBB  <Vd>.4S, <Vn>.16B, <Vm>.B[<index>]`
- **Fixed bits**: `Q`=`0`, `size`=`0`
- **Bit Pattern**: `??????????????????????0???????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20 19  15  11 10  9   4  |
|-----------------------------------------|
| 0   Q   1   01111 0x  L   M   Rm  1000 H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.FMLALLBB_asimdelem_J)

```
if !IsFeatureImplemented(FEAT_FP8FMA) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Rn);
constant integer m = UInt('00':Rm<2:0>);
constant integer d = UInt(Rd);
constant integer index = UInt(H:L:M:Rm<3>);
constant integer elements = 128 DIV 32;
constant integer sel = UInt(Q:size<0>);
```

#### Execute (A64.simd_dp.asimdelem.FMLALLBB_asimdelem_J)

```
CheckFPMREnabled(); CheckFPAdvSIMDEnabled64();
constant bits(128) operand1 = V[n, 128];
constant bits(128) operand2 = V[m, 128];
constant bits(128) operand3 = V[d, 128];
bits(128) result;

for e = 0 to elements-1
    constant bits(8) element1  = Elem[operand1, 4 * e + sel, 8];
    constant bits(8) element2  = Elem[operand2, index, 8];
    constant bits(32) element3 = Elem[operand3, e, 32];
    Elem[result, e, 32] = FP8MulAddFP(element3, element1, element2, FPCR, FPMR);

V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP8FMA)` |

### Variant: `Advanced SIMD (FMLALLBT_asimdelem_J)` (FMLALLBT)
- **Condition**: `Q == 0 && size == 01`
- **Assembly**: `FMLALLBT  <Vd>.4S, <Vn>.16B, <Vm>.B[<index>]`
- **Fixed bits**: `Q`=`0`, `size`=`1`
- **Bit Pattern**: `??????????????????????1???????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20 19  15  11 10  9   4  |
|-----------------------------------------|
| 0   Q   1   01111 0x  L   M   Rm  1000 H   0   Rn  Rd  |
```

### Variant: `Advanced SIMD (FMLALLTB_asimdelem_J)` (FMLALLTB)
- **Condition**: `Q == 1 && size == 00`
- **Assembly**: `FMLALLTB  <Vd>.4S, <Vn>.16B, <Vm>.B[<index>]`
- **Fixed bits**: `Q`=`1`, `size`=`0`
- **Bit Pattern**: `??????????????????????0???????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20 19  15  11 10  9   4  |
|-----------------------------------------|
| 0   Q   1   01111 0x  L   M   Rm  1000 H   0   Rn  Rd  |
```

### Variant: `Advanced SIMD (FMLALLTT_asimdelem_J)` (FMLALLTT)
- **Condition**: `Q == 1 && size == 01`
- **Assembly**: `FMLALLTT  <Vd>.4S, <Vn>.16B, <Vm>.B[<index>]`
- **Fixed bits**: `Q`=`1`, `size`=`1`
- **Bit Pattern**: `??????????????????????1???????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20 19  15  11 10  9   4  |
|-----------------------------------------|
| 0   Q   1   01111 0x  L   M   Rm  1000 H   0   Rn  Rd  |
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
- source: `fmlallbb_advsimd_elem.xml`
</details>