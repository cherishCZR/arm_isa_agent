## FCVTXN
_ARM A64 Instruction_

**Title**: FCVTXN, FCVTXN2 -- A64 | **Class**: `advsimd` | **XML ID**: `FCVTXN_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point convert to lower precision narrow, rounding to odd (vector)

**Description**:
This instruction reads each vector element
in the source SIMD&FP register, narrows each value to half
the precision of the source element using the Round to Odd rounding mode, writes
the result to a vector, and writes the vector to the destination SIMD&FP
register.

The FCVTXN instruction writes the vector
to the lower half of the
destination register and clears the upper half.
The FCVTXN2 instruction writes the vector
to the upper half of the
destination register without affecting the other bits of the register.

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

### Variant: `Scalar`
- **Assembly**: `FCVTXN  S<d>, D<n>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23  21  16  11   9   4  |
|-----------------------------------|
| 01  1   1   111 0   01  10000 10110 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdmisc.FCVTXN_asisdmisc_N)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 32;
constant integer datasize = esize;
constant integer elements = 1;
constant integer part = 0;
```

#### Execute (A64.simd_dp.asisdmisc.FCVTXN_asisdmisc_N)

```
CheckFPAdvSIMDEnabled64();

constant bits(2*datasize) operand = V[n, 2*datasize];
constant boolean merge = elements == 1 && IsMerging(FPCR);
bits(128) result = if merge then V[d, 128] else Zeros(128);

for e = 0 to elements-1
    Elem[result, e, esize] = FPConvert(Elem[operand, e, 2*esize], FPCR, FPRounding_ODD, esize);

if merge then
    V[d, 128] = result;
else
    Vpart[d, part, datasize] = Elem[result, 0, datasize];
```

### Variant: `Vector`
- **Assembly**: `FCVTXN{2}  <Vd>.<Tb>, <Vn>.2D`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21  16  11   9   4  |
|--------------------------------------|
| 0   Q   1   0   111 0   01  10000 10110 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.FCVTXN_asimdmisc_N)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 32;
constant integer datasize = 64;
constant integer elements = 2;
constant integer part = UInt(Q);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<d>` | `register (32-bit)` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `register (64-bit)` | `Rn` | Is the number of the SIMD&FP source register, encoded in the "Rn" field. |
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Tb>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

**2 Value Table**:

| bitfield | symbol |
|---|---|
| 0 | [absent] |
| 1 | [present] |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2S |
| 1 | 4S |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvtxn_advsimd.xml`
</details>