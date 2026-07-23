## FCVTL
_ARM A64 Instruction_

**Title**: FCVTL, FCVTL2 -- A64 | **Class**: `advsimd` | **XML ID**: `FCVTL_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point convert to higher precision long (vector)

**Description**:
This instruction
reads each element in a vector
in the SIMD&FP source register, converts each value to double
the precision of the source element using the
rounding mode that is determined by the FPCR,
and writes each result to the equivalent element of the vector in the SIMD&FP
destination register.

Where the operation lengthens a 64-bit vector to a 128-bit vector,
the FCVTL2 variant operates on the elements in the top 64 bits of
the source register.

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
- **Assembly**: `FCVTL{2}  <Vd>.<Ta>, <Vn>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21  16  11   9   4  |
|-----------------------------------------|
| 0   Q   0   0   111 0   0   sz  10000 10111 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.FCVTL_asimdmisc_L)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 16 << UInt(sz);
constant integer datasize = 64;
constant integer part = UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimdmisc.FCVTL_asimdmisc_L)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = Vpart[n, part, datasize];
bits(2*datasize) result;

for e = 0 to elements-1
    Elem[result, e, 2*esize] = FPConvert(Elem[operand, e, esize], FPCR, 2 * esize);

V[d, 2*datasize] = result;
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
| `<Ta>` | `unknown` | `sz` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `sz:Q` | Is an arrangement specifier, |

**2 Value Table**:

| bitfield | symbol |
|---|---|
| 0 | [absent] |
| 1 | [present] |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4S |
| 1 | 2D |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |

---
<details><summary>Metadata</summary>

- advsimd-datatype: `simd-single-and-double`
- advsimd-type: `simd`
- datatype: `single-and-double`
- isa: `A64`
- source: `fcvtl_advsimd.xml`
</details>