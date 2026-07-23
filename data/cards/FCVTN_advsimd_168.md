## FCVTN
_ARM A64 Instruction_

**Title**: FCVTN (half-precision to 8-bit floating-point) -- A64 | **Class**: `advsimd` | **XML ID**: `FCVTN_advsimd_168`

**Architecture**: `FEAT_FP8` (ARMv9.5)

**Summary**: Half-precision to 8-bit floating-point convert and narrow (vector)

**Description**:
This instruction converts half-precision elements of the two
source vectors to 8-bit floating-point while scaling the values by
2SInt(FPMR.NSCALE[4:0]), and places the in-order results in the
8-bit elements of the destination vector.

The 8-bit floating-point encoding format is selected by
FPMR.F8D.

### Variant: `Advanced SIMD`
- **Assembly**: `FCVTN  <Vd>.<Ta>, <Vn>.<Tb>, <Vm>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15 14  10  9   4  |
|--------------------------------------------|
| 0   Q   0   0   111 0   01  0   Rm  1   1110 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame2.FCVTN_asimdsame2_D)

```
if !IsFeatureImplemented(FEAT_FP8) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = if Q == '1' then 128 else 64;
constant integer elements = datasize DIV 16;
```

#### Execute (A64.simd_dp.asimdsame2.FCVTN_asimdsame2_D)

```
CheckFPMREnabled(); CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];
bits(datasize) result;

for e = 0 to elements-1
    Elem[result, 0*elements + e, 8] = FPConvertFP8(Elem[operand1, e, 16], FPCR, FPMR, 8);
    Elem[result, 1*elements + e, 8] = FPConvertFP8(Elem[operand2, e, 16], FPCR, FPMR, 8);

V[d, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP8)` |

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
| 0 | 8B |
| 1 | 16B |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4H |
| 1 | 8H |

---
<details><summary>Metadata</summary>

- advsimd-only: `simd-only`
- advsimd-type: `simd`
- isa: `A64`
- source: `fcvtn_advsimd_168.xml`
</details>