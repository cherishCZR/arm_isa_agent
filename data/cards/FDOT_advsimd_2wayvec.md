## FDOT
_ARM A64 Instruction_

**Title**: FDOT (8-bit floating-point to half-precision, vector) -- A64 | **Class**: `advsimd` | **XML ID**: `FDOT_advsimd_2wayvec`

**Architecture**: `FEAT_FP8DOT2` (ARMv9.5)

**Summary**: 8-bit floating-point dot product to half-precision (vector)

**Description**:
This instruction computes the fused sum-of-products of a group of two 8-bit
floating-point values held in each 16-bit element of the first and
second source vectors. The half-precision sum-of-products are scaled by
2-UInt(FPMR.LSCALE[3:0]), before being destructively added without
intermediate rounding to the corresponding half-precision elements
of the destination vector.

The 8-bit floating-point encoding format for the elements of the first
source vector is selected by FPMR.F8S1.
The 8-bit floating-point encoding format for the elements of the second
source vector is selected by FPMR.F8S2.

### Variant: `Advanced SIMD`
- **Assembly**: `FDOT  <Vd>.<Ta>, <Vn>.<Tb>, <Vm>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15 14  10  9   4  |
|--------------------------------------------|
| 0   Q   0   0   111 0   01  0   Rm  1   1111 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame2.FDOT_asimdsame2_D)

```
if !IsFeatureImplemented(FEAT_FP8DOT2) then
    EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = if Q == '1' then 128 else 64;
constant integer esize = 16;
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimdsame2.FDOT_asimdsame2_D)

```
CheckFPMREnabled(); CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];
constant bits(datasize) operand3 = V[d, datasize];
bits(datasize) result;

for e = 0 to elements-1
    constant bits(esize) op1 = Elem[operand1, e, esize];
    constant bits(esize) op2 = Elem[operand2, e, esize];
    bits(esize) sum = Elem[operand3, e, esize];

    sum = FP8DotAddFP(sum, op1, op2, FPCR, FPMR);
    Elem[result, e, esize] = sum;

V[d, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP8DOT2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4H |
| 1 | 8H |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |

---
<details><summary>Metadata</summary>

- advsimd-only: `simd-only`
- advsimd-type: `simd`
- isa: `A64`
- source: `fdot_advsimd_2wayvec.xml`
</details>