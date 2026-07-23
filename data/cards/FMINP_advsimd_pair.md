## FMINP
_ARM A64 Instruction_

**Title**: FMINP (scalar) -- A64 | **Class**: `advsimd` | **XML ID**: `FMINP_advsimd_pair`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point minimum of pair of elements (scalar)

**Description**:
This instruction compares two vector elements in the source SIMD&FP register
and writes the smallest of the floating-point values
as a scalar to the destination SIMD&FP register.

When FPCR.AH is 0,
the behavior is as follows for each pairwise operation:

When FPCR.AH is 1,
the behavior is as follows for each pairwise operation:

This instruction can generate a floating-point exception.
  Depending on the settings in FPCR,
  the exception results in either a flag being set in FPSR
  or a synchronous exception being generated.
  For more information, see
  Floating-point exceptions and exception traps.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Half-precision`
- **Assembly**: `FMINP  H<d>, <Vn>.2H`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23 22 21  16  11   9   4  |
|--------------------------------------|
| 01  0   1   111 0   1   0   11000 01111 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdpair.FMINP_asisdpair_only_H)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);
if sz == '1' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 16;
constant integer datasize = 32;
```

#### Execute (A64.simd_dp.asisdpair.FMINP_asisdpair_only_H)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[n, datasize];
V[d, esize] = FPReduce(ReduceOp_FMIN, operand, esize, FPCR);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_FP16)` |
| 🚫 ENCODING_UNDEF | `sz != '1'` |

### Variant: `Single-precision and double-precision`
- **Assembly**: `FMINP  <V><d>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23 22 21  16  11   9   4  |
|--------------------------------------|
| 01  1   1   111 0   1   sz  11000 01111 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdpair.FMINP_asisdpair_only_SD)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 32 << UInt(sz);
constant integer datasize = esize * 2;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<d>` | `register (16-bit)` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<V>` | `register (128-bit)` | `sz` | Is the destination width specifier, |
| `<T>` | `unknown` | `sz` | Is the source arrangement specifier, |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2S |
| 1 | 2D |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fminp_advsimd_pair.xml`
</details>