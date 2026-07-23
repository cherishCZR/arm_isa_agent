## FJCVTZS
_ARM A64 Instruction_

**Title**: FJCVTZS -- A64 | **Class**: `float` | **XML ID**: `FJCVTZS`

**Architecture**: `FEAT_JSCVT` (ARMv8.3)

**Summary**: Floating-point Javascript convert to signed fixed-point, rounding toward zero

**Description**:
This instruction converts the double-precision floating-point value
in the SIMD&FP source register to a 32-bit signed integer using
the Round towards Zero rounding mode, and writes the result to the
general-purpose destination register.
If the result is too large to be represented as a signed 32-bit
integer, then the result is the integer modulo 232, as held in
a 32-bit signed integer.

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

### Variant: `Double-precision to 32-bit`
- **Assembly**: `FJCVTZS  <Wd>, <Dn>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  18  15   9   4  |
|-----------------------------------------|
| 0   0   0   1   111 0   01  1   11  110 000000 Rn  Rd  |
```

#### Decode (A64.simd_dp.float2int.FJCVTZS_32D_float2int)

```
if !IsFeatureImplemented(FEAT_JSCVT) then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer intsize = 32;
constant integer fltsize = 64;
```

#### Execute (A64.simd_dp.float2int.FJCVTZS_32D_float2int)

```
CheckFPAdvSIMDEnabled64();
constant bits(fltsize) fltval = V[n, fltsize];

bits(intsize) intval;
bit z;
(intval, z) = FPToFixedJS(fltval, FPCR, intsize);

X[d, intsize] = intval;
PSTATE.<N,Z,C,V> = '0':z:'00';
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_JSCVT)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the SIMD&FP source register, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- convert-type: `double-to-32`
- isa: `A64`
- source: `fjcvtzs.xml`
</details>