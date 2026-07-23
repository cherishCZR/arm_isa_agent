## BFMLAL
_ARM A64 Instruction_

**Title**: BFMLALB, BFMLALT (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `BFMLAL_advsimd_vec`

**Architecture**: `FEAT_BF16` (ARMv8.6)

**Summary**: BFloat16 floating-point widening multiply-add long (vector)

**Description**:
This instruction widens the even-numbered (bottom) or
odd-numbered (top) 16-bit elements in the first and second source vectors from Bfloat16 to single-precision format.
The instruction then multiplies and adds these values without intermediate rounding to the
single-precision elements of the destination vector that overlap with the corresponding BFloat16
elements in the source vectors.

ID_AA64ISAR1_EL1.BF16 indicates whether this instruction is supported.

### Variant: `Vector`
- **Assembly**: `BFMLAL<bt>  <Vd>.4S, <Vn>.8H, <Vm>.8H`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15 14  10  9   4  |
|--------------------------------------------|
| 0   Q   1   0   111 0   11  0   Rm  1   1111 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame2.BFMLAL_asimdsame2_F_)

```
if !IsFeatureImplemented(FEAT_BF16) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);

constant integer elements = 128 DIV 32;
constant integer sel = UInt(Q);
```

#### Execute (A64.simd_dp.asimdsame2.BFMLAL_asimdsame2_F_)

```
CheckFPAdvSIMDEnabled64();
constant bits(128) operand1 = V[n, 128];
constant bits(128) operand2 = V[m, 128];
constant bits(128) operand3 = V[d, 128];
bits(128) result;

for e = 0 to elements-1
    constant bits(16) element1 = Elem[operand1, 2 * e + sel, 16];
    constant bits(16) element2 = Elem[operand2, 2 * e + sel, 16];
    constant bits(32) addend   = Elem[operand3, e, 32];
    Elem[result, e, 32] = BFMulAddH(addend, element1, element2, FPCR);

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
| `<bt>` | `unknown` | `Q` | Is the bottom or top element specifier, |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

**<bt> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | B |
| 1 | T |

---
<details><summary>Metadata</summary>

- advsimd-type: `simd`
- isa: `A64`
- source: `bfmlal_advsimd_vec.xml`
</details>