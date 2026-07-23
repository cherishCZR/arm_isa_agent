## BFCVTN
_ARM A64 Instruction_

**Title**: BFCVTN, BFCVTN2 -- A64 | **Class**: `advsimd` | **XML ID**: `BFCVTN_advsimd`

**Architecture**: `FEAT_BF16` (ARMv8.6)

**Summary**: Floating-point convert from single-precision to BFloat16 format (vector)

**Description**:
This instruction reads
each single-precision element in the SIMD&FP source vector, converts each value to BFloat16
format, and writes the results in the lower or upper half of the SIMD&FP destination vector.
The result elements are half the width of the source elements.

The BFCVTN instruction writes the half-width results to the lower half
of the destination vector and clears the upper half to zero.
The BFCVTN2 instruction writes the results to the upper half
of the destination vector without affecting the other bits in the register.

### Variant: `Vector single-precision to BFloat16`
- **Assembly**: `BFCVTN{2}  <Vd>.<Ta>, <Vn>.4S`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21  16  11   9   4  |
|--------------------------------------|
| 0   Q   0   0   111 0   10  10000 10110 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.BFCVTN_asimdmisc_4S)

```
if !IsFeatureImplemented(FEAT_BF16) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer part = UInt(Q);
constant integer elements = 64 DIV 16;
```

#### Execute (A64.simd_dp.asimdmisc.BFCVTN_asimdmisc_4S)

```
CheckFPAdvSIMDEnabled64();
constant bits(128) operand = V[n, 128];
bits(64) result;

for e = 0 to elements-1
    Elem[result, e, 16] = FPConvertBF(Elem[operand, e, 32], FPCR);

Vpart[d, part, 64] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_BF16)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

**2 Value Table**:

| bitfield | symbol |
|---|---|
| 0 | [absent] |
| 1 | [present] |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4H |
| 1 | 8H |

---
<details><summary>Metadata</summary>

- advsimd-datatype: `simd-single-and-bf16`
- advsimd-type: `simd`
- datatype: `single-and-bf16`
- isa: `A64`
- source: `bfcvtn_advsimd.xml`
</details>