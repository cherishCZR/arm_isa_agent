## BFMLAL
_ARM A64 Instruction_

**Title**: BFMLALB, BFMLALT (by element) -- A64 | **Class**: `advsimd` | **XML ID**: `BFMLAL_advsimd_elt`

**Architecture**: `FEAT_BF16` (ARMv8.6)

**Summary**: BFloat16 floating-point widening multiply-add long (by element)

**Description**:
This instruction widens the even-numbered (bottom)
or odd-numbered (top) 16-bit elements in the first source vector, and the indexed element in
the second source vector from Bfloat16 to single-precision format. The instruction then multiplies and adds these values
without intermediate rounding to single-precision elements of the destination vector that overlap with the
corresponding BFloat16 elements in the first source vector.

ID_AA64ISAR1_EL1.BF16 indicates whether this instruction is supported.

### Variant: `Vector`
- **Assembly**: `BFMLAL<bt>  <Vd>.4S, <Vn>.8H, <Vm>.H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20 19  15  11 10  9   4  |
|-----------------------------------------------|
| 0   Q   0   0   111 1   11  L   M   Rm  1111 H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.BFMLAL_asimdelem_F)

```
if !IsFeatureImplemented(FEAT_BF16) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Rn);
constant integer m = UInt('0':Rm);
constant integer d = UInt(Rd);
constant integer index = UInt(H:L:M);

constant integer elements = 128 DIV 32;
constant integer sel = UInt(Q);
```

#### Execute (A64.simd_dp.asimdelem.BFMLAL_asimdelem_F)

```
CheckFPAdvSIMDEnabled64();
bits(128) result;
constant bits(128) operand1 = V[n, 128];
constant bits(128) operand2 = V[m, 128];
constant bits(128) operand3 = V[d, 128];
constant bits(16) element2  = Elem[operand2, index, 16];

for e = 0 to elements-1
    constant bits(16) element1   = Elem[operand1, 2 * e + sel, 16];
    constant bits(32) addend     = Elem[operand3, e, 32];
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
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, in the range V0 to V15, encoded in the "Rm" field. |
| `<index>` | `unknown` | `H:L:M` | Is the element index, in the range 0 to 7, encoded in the "H:L:M" fields. |

**<bt> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | B |
| 1 | T |

---
<details><summary>Metadata</summary>

- advsimd-reguse: `2reg-element`
- datatype: `half`
- isa: `A64`
- reguse-datatype: `2reg-element-half`
- source: `bfmlal_advsimd_elt.xml`
</details>