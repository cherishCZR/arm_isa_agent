## SCVTF
_ARM A64 Instruction_

**Title**: SCVTF (scalar SIMD&FP) -- A64 | **Class**: `float` | **XML ID**: `SCVTF_sisd`

**Architecture**: `FEAT_FPRCVT` (ARMv9.6)

**Summary**: Signed integer convert to floating-point (scalar SIMD&FP)

**Description**:
This instruction converts the signed integer value in the
SIMD&FP source register to a floating-point value using the
rounding mode that is specified by the FPCR, and writes the result to the
SIMD&FP destination register.

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

### Variant: `Integer (SCVTF_sisd_32H)` (32-bit to half-precision)
- **Condition**: `sf == 0 && ftype == 11`
- **Assembly**: `SCVTF  <Hd>, <Sn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`11`
- **Bit Pattern**: `??????????????????????11???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  100 000000 Rn  Rd  |
```

#### Decode (A64.simd_dp.float2int.SCVTF_sisd_32H)

```
if !IsFeatureImplemented(FEAT_FPRCVT) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer intsize = 32 << UInt(sf);
constant integer fltsize = 8 << UInt(ftype EOR '10');
constant FPRounding rounding = FPRoundingMode(FPCR);
```

#### Execute (A64.simd_dp.float2int.SCVTF_sisd_32H)

```
CheckFPEnabled64();

bits(fltsize) fltval;
bits(intsize) intval;
constant boolean merge = IsMerging(FPCR);
bits(128) result = if merge then V[d, 128] else Zeros(128);

intval = V[n, intsize];
fltval = FixedToFP(intval, 0, FALSE, FPCR, rounding, fltsize);
Elem[result, 0, fltsize] = fltval;

V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FPRCVT)` |

### Variant: `Integer (SCVTF_sisd_32D)` (32-bit to double-precision)
- **Condition**: `sf == 0 && ftype == 01`
- **Assembly**: `SCVTF  <Dd>, <Sn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`01`
- **Bit Pattern**: `??????????????????????10???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  100 000000 Rn  Rd  |
```

### Variant: `Integer (SCVTF_sisd_64H)` (64-bit to half-precision)
- **Condition**: `sf == 1 && ftype == 11`
- **Assembly**: `SCVTF  <Hd>, <Dn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`11`
- **Bit Pattern**: `??????????????????????11???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  100 000000 Rn  Rd  |
```

### Variant: `Integer (SCVTF_sisd_64S)` (64-bit to single-precision)
- **Condition**: `sf == 1 && ftype == 00`
- **Assembly**: `SCVTF  <Sd>, <Dn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`00`
- **Bit Pattern**: `??????????????????????00???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  100 000000 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hd>` | `register (16-bit)` | `Rd` | Is the 16-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Dd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Sd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `scvtf_sisd.xml`
</details>