## FNMADD
_ARM A64 Instruction_

**Title**: FNMADD -- A64 | **Class**: `float` | **XML ID**: `FNMADD_float`

**Summary**: Floating-point negated fused multiply-add (scalar)

**Description**:
This instruction multiplies the values of
the first two SIMD&FP source registers, negates the product,
subtracts the value of
the third SIMD&FP source register, and
writes the result to the destination SIMD&FP register.

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

### Variant: `Floating-point (FNMADD_H_floatdp3)` (Half-precision)
- **Condition**: `ftype == 11`
- **Assembly**: `FNMADD  <Hd>, <Hn>, <Hm>, <Ha>`
- **Fixed bits**: `ftype`=`11`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15 14   9   4  |
|-----------------------------------|
| 0   0   0   11111 ftype 1   Rm  0   Ra  Rn  Rd  |
```

#### Decode (A64.simd_dp.floatdp3.FNMADD_H_floatdp3)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if ftype == '10' then EndOfDecode(Decode_UNDEF);
if ftype == '11' && !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer a = UInt(Ra);

constant integer esize = 8 << UInt(ftype EOR '10');
```

#### Execute (A64.simd_dp.floatdp3.FNMADD_H_floatdp3)

```
CheckFPEnabled64();

constant bits(esize) addend   = FPNeg(V[a, esize], FPCR);
constant bits(esize) operand1 = FPNeg(V[n, esize], FPCR);
constant bits(esize) operand2 = V[m, esize];

bits(128) result = if IsMerging(FPCR) then V[a, 128] else Zeros(128);

Elem[result, 0, esize] = FPMulAdd(addend, operand1, operand2, FPCR);
V[d, 128] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `ftype != '10'` |
| 🔒 FEATURE_GATE | `ftype != '11' \|\| IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Floating-point (FNMADD_S_floatdp3)` (Single-precision)
- **Condition**: `ftype == 00`
- **Assembly**: `FNMADD  <Sd>, <Sn>, <Sm>, <Sa>`
- **Fixed bits**: `ftype`=`00`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15 14   9   4  |
|-----------------------------------|
| 0   0   0   11111 ftype 1   Rm  0   Ra  Rn  Rd  |
```

### Variant: `Floating-point (FNMADD_D_floatdp3)` (Double-precision)
- **Condition**: `ftype == 01`
- **Assembly**: `FNMADD  <Dd>, <Dn>, <Dm>, <Da>`
- **Fixed bits**: `ftype`=`01`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15 14   9   4  |
|-----------------------------------|
| 0   0   0   11111 ftype 1   Rm  0   Ra  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hd>` | `register (16-bit)` | `Rd` | Is the 16-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the first SIMD&FP source register holding the multiplicand, encoded in the "Rn" field. |
| `<Hm>` | `register (16-bit)` | `Rm` | Is the 16-bit name of the second SIMD&FP source register holding the multiplier, encoded in the "Rm" field. |
| `<Ha>` | `register (16-bit)` | `Ra` | Is the 16-bit name of the third SIMD&FP source register holding the addend, encoded in the "Ra" field. |
| `<Sd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first SIMD&FP source register holding the multiplicand, encoded in the "Rn" field. |
| `<Sm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second SIMD&FP source register holding the multiplier, encoded in the "Rm" field. |
| `<Sa>` | `register (32-bit)` | `Ra` | Is the 32-bit name of the third SIMD&FP source register holding the addend, encoded in the "Ra" field. |
| `<Dd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first SIMD&FP source register holding the multiplicand, encoded in the "Rn" field. |
| `<Dm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second SIMD&FP source register holding the multiplier, encoded in the "Rm" field. |
| `<Da>` | `register (64-bit)` | `Ra` | Is the 64-bit name of the third SIMD&FP source register holding the addend, encoded in the "Ra" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fnmadd_float.xml`
</details>