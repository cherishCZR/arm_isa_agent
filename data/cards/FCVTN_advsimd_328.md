## FCVTN
_ARM A64 Instruction_

**Title**: FCVTN, FCVTN2 (single-precision to 8-bit floating-point) -- A64 | **Class**: `advsimd` | **XML ID**: `FCVTN_advsimd_328`

**Architecture**: `FEAT_FP8` (ARMv9.5)

**Summary**: Single-precision to 8-bit floating-point convert and narrow (vector)

**Description**:
This instruction converts each single-precision element of the two
source vectors to 8-bit floating-point while scaling the value by
2SInt(FPMR.NSCALE), and places the in-order results in the
8-bit elements of the lower or upper half of the destination vector.
FCVTN writes the results to the lower half of the destination vector
and clears the upper half. FCVTN2 writes the results to the upper half
of the destination vector without affecting the other bits of the vector.

The 8-bit floating-point encoding format is selected by
FPMR.F8D.

### Variant: `Advanced SIMD`
- **Assembly**: `FCVTN{2}  <Vd>.<Ta>, <Vn>.4S, <Vm>.4S`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15 14  10  9   4  |
|--------------------------------------------|
| 0   Q   0   0   111 0   00  0   Rm  1   1110 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame2.FCVTN_asimdsame2_H)

```
if !IsFeatureImplemented(FEAT_FP8) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer part = UInt(Q);
constant integer elements = 128 DIV 32;
```

#### Execute (A64.simd_dp.asimdsame2.FCVTN_asimdsame2_H)

```
CheckFPMREnabled(); CheckFPAdvSIMDEnabled64();
constant bits(128) operand1 = V[n, 128];
constant bits(128) operand2 = V[m, 128];
bits(64) result;

for e = 0 to elements-1
    Elem[result, 0*elements + e, 8] = FPConvertFP8(Elem[operand1, e, 32], FPCR, FPMR, 8);
    Elem[result, 1*elements + e, 8] = FPConvertFP8(Elem[operand2, e, 32], FPCR, FPMR, 8);

Vpart[d, part, 64] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP8)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

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
- source: `fcvtn_advsimd_328.xml`
</details>