## FRECPX
_ARM A64 Instruction_

**Title**: FRECPX -- A64 | **Class**: `advsimd` | **XML ID**: `FRECPX_advsimd`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point reciprocal exponent (scalar)

**Description**:
This instruction finds an approximate reciprocal exponent for the source
SIMD&FP register and writes the result to the destination SIMD&FP register.

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
- **Assembly**: `FRECPX  <Hd>, <Hn>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23 22  18  16  11   9   4  |
|--------------------------------------|
| 01  0   1   111 0   1   1111 00  11111 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdmiscfp16.FRECPX_asisdmiscfp16_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 16;
```

#### Execute (A64.simd_dp.asisdmiscfp16.FRECPX_asisdmiscfp16_R)

```
CheckFPEnabled64();
constant bits(esize) operand = V[n, esize];

constant boolean merge = IsMerging(FPCR);
bits(128) result = if merge then V[d, 128] else Zeros(128);

Elem[result, 0, esize] = FPRecpX(operand, FPCR);

V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Single-precision and double-precision`
- **Assembly**: `FRECPX  <V><d>, <V><n>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23 22 21  16  11   9   4  |
|--------------------------------------|
| 01  0   1   111 0   1   sz  10000 11111 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdmisc.FRECPX_asisdmisc_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 32 << UInt(sz);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hd>` | `register (16-bit)` | `Rd` | Is the 16-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<V>` | `register (128-bit)` | `sz` | Is a width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `unknown` | `Rn` | Is the number of the SIMD&FP source register, encoded in the "Rn" field. |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

---
<details><summary>Metadata</summary>

- advsimd-type: `sisd`
- isa: `A64`
- source: `frecpx_advsimd.xml`
</details>