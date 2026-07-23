## FDOT
_ARM A64 Instruction_

**Title**: FDOT (8-bit floating-point to single-precision, by element) -- A64 | **Class**: `advsimd` | **XML ID**: `FDOT_advsimd_4wayelem`

**Architecture**: `FEAT_FP8DOT4` (ARMv9.5)

**Summary**: 8-bit floating-point dot product to single-precision (vector, by element)

**Description**:
This instruction computes the fused sum-of-products of a group of four 8-bit
floating-point values held in each 32-bit element of the first source
vector and a group of four 8-bit floating-point values in an indexed 32-bit
element of the second source vector. The single-precision sum-of-products
are scaled by 2-UInt(FPMR.LSCALE), before being destructively
added without intermediate rounding to the corresponding single-precision
elements of the destination vector.

The 8-bit floating-point groups within the second source vector are
specified using an immediate index.

The 8-bit floating-point encoding format for the elements of the first
source vector is selected by FPMR.F8S1.
The 8-bit floating-point encoding format for the elements of the second
source vector is selected by FPMR.F8S2.

### Variant: `Advanced SIMD`
- **Assembly**: `FDOT  <Vd>.<Ta>, <Vn>.<Tb>, <Vm>.4B[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20 19  15  11 10  9   4  |
|-----------------------------------------------|
| 0   Q   0   0   111 1   00  L   M   Rm  0000 H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.FDOT_asimdelem_D)

```
if !IsFeatureImplemented(FEAT_FP8DOT4) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Rn);
constant integer d = UInt(Rd);
constant integer m = UInt(M:Rm);
constant integer i = UInt(H:L);

constant integer datasize = if Q == '1' then 128 else 64;
constant integer esize = 32;
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimdelem.FDOT_asimdelem_D)

```
CheckFPMREnabled(); CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(128) operand2 = V[m, 128];
constant bits(datasize) operand3 = V[d, datasize];
bits(datasize) result;

for e = 0 to elements-1
    constant bits(esize) op1 = Elem[operand1, e, esize];
    constant bits(esize) op2 = Elem[operand2, i, esize];
    constant bits(esize) sum = Elem[operand3, e, esize];

    Elem[result, e, esize] = FP8DotAddFP(sum, op1, op2, FPCR, FPMR);

V[d, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP8DOT4)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vm>` | `register (128-bit)` | `M:Rm` | Is the name of the second SIMD&FP source register, encoded in the "M:Rm" fields. |
| `<index>` | `unknown` | `H:L` | Is the immediate index of a 32-bit group of four 8-bit values, in the range 0 to 3, encoded in the "H:L" fields. |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2S |
| 1 | 4S |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |

---
<details><summary>Metadata</summary>

- advsimd-only: `simd-only`
- advsimd-reguse: `2reg-element`
- isa: `A64`
- source: `fdot_advsimd_4wayelem.xml`
</details>