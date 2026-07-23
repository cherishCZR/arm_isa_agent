## FCVTN
_ARM A64 Instruction_

**Title**: FCVTN, FCVTN2 (double to single-precision, single to half-precision) -- A64 | **Class**: `advsimd` | **XML ID**: `FCVTN_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point convert to lower precision narrow (vector)

**Description**:
This instruction reads each vector element
in the SIMD&FP source register, converts each result to half
the precision of the source element, writes
the final result to a vector, and writes the vector
to the lower or upper half of the destination SIMD&FP register.
The destination vector elements are half as long as the source vector elements.
The rounding mode is determined by the FPCR.

FCVTN writes the vector to the lower half of the
destination register and clears the upper half.
FCVTN2 writes the vector to the upper half of the
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

### Variant: `Vector single-precision and double-precision`
- **Assembly**: `FCVTN{2}  <Vd>.<Tb>, <Vn>.<Ta>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21  16  11   9   4  |
|-----------------------------------------|
| 0   Q   0   0   111 0   0   sz  10000 10110 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.FCVTN_asimdmisc_N)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 16 << UInt(sz);
constant integer datasize = 64;
constant integer part = UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimdmisc.FCVTN_asimdmisc_N)

```
CheckFPAdvSIMDEnabled64();
constant bits(2*datasize) operand = V[n, 2*datasize];
bits(datasize) result;

for e = 0 to elements-1
    Elem[result, e, esize] = FPConvert(Elem[operand, e, 2*esize], FPCR, esize);

Vpart[d, part, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Tb>` | `unknown` | `sz:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Ta>` | `unknown` | `sz` | Is an arrangement specifier, |

**2 Value Table**:

| bitfield | symbol |
|---|---|
| 0 | [absent] |
| 1 | [present] |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4S |
| 1 | 2D |

---
<details><summary>Metadata</summary>

- advsimd-datatype: `simd-single-and-double`
- advsimd-type: `simd`
- datatype: `single-and-double`
- isa: `A64`
- source: `fcvtn_advsimd.xml`
</details>