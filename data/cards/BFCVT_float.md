## BFCVT
_ARM A64 Instruction_

**Title**: BFCVT -- A64 | **Class**: `float` | **XML ID**: `BFCVT_float`

**Architecture**: `FEAT_BF16` (ARMv8.6)

**Summary**: Floating-point convert from single-precision to BFloat16 format (scalar)

**Description**:
This instruction converts the single-precision floating-point value
in the 32-bit SIMD&FP source register to BFloat16 format and writes
the result in the 16-bit SIMD&FP destination register.

ID_AA64ISAR1_EL1.BF16 indicates whether this instruction is supported.

### Variant: `Single-precision to BFloat16`
- **Assembly**: `BFCVT  <Hd>, <Sn>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  14   9   4  |
|--------------------------------------|
| 0   0   0   1   111 0   01  1   000110 10000 Rn  Rd  |
```

#### Decode (A64.simd_dp.floatdp1.BFCVT_BS_floatdp1)

```
if !IsFeatureImplemented(FEAT_BF16) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
```

#### Execute (A64.simd_dp.floatdp1.BFCVT_BS_floatdp1)

```
CheckFPEnabled64();

constant bits(32) operand = V[n, 32];
constant boolean merge = IsMerging(FPCR);
bits(128) result = if merge then V[d, 128] else Zeros(128);

Elem[result, 0, 16] = FPConvertBF(operand, FPCR);
V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_BF16)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hd>` | `register (16-bit)` | `Rd` | Is the 16-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the SIMD&FP source register, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- convert-type: `single-to-bf16`
- isa: `A64`
- source: `bfcvt_float.xml`
</details>