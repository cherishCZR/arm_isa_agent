## FCVTAU
_ARM A64 Instruction_

**Title**: FCVTAU (scalar SIMD&FP) -- A64 | **Class**: `float` | **XML ID**: `FCVTAU_sisd`

**Architecture**: `FEAT_FPRCVT` (ARMv9.6)

**Summary**: Floating-point convert to unsigned integer, rounding to nearest with ties to away (scalar SIMD&FP)

**Description**:
This instruction converts the floating-point value in the SIMD&FP source
register to a 32-bit or 64-bit unsigned integer using
the Round to Nearest with Ties to Away rounding mode, and writes the result to the
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

### Variant: `Floating-point (FCVTAU_sisd_32H)` (Half-precision to 32-bit)
- **Condition**: `sf == 0 && ftype == 11`
- **Assembly**: `FCVTAU  <Sd>, <Hn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`11`
- **Bit Pattern**: `??????????????????????11???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  011 000000 Rn  Rd  |
```

#### Decode (A64.simd_dp.float2int.FCVTAU_sisd_32H)

```
if !IsFeatureImplemented(FEAT_FPRCVT) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer intsize = 32 << UInt(sf);
constant integer fltsize = 8 << UInt(ftype EOR '10');
```

#### Execute (A64.simd_dp.float2int.FCVTAU_sisd_32H)

```
CheckFPEnabled64();

bits(fltsize) fltval;
bits(intsize) intval;
constant boolean merge = IsMerging(FPCR);
bits(128) result = if merge then V[d, 128] else Zeros(128);

fltval = V[n, fltsize];
intval = FPToFixed(fltval, 0, TRUE, FPCR, FPRounding_TIEAWAY, intsize);
Elem[result, 0, intsize] = intval;

V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FPRCVT)` |

### Variant: `Floating-point (FCVTAU_sisd_64H)` (Half-precision to 64-bit)
- **Condition**: `sf == 1 && ftype == 11`
- **Assembly**: `FCVTAU  <Dd>, <Hn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`11`
- **Bit Pattern**: `??????????????????????11???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  011 000000 Rn  Rd  |
```

### Variant: `Floating-point (FCVTAU_sisd_64S)` (Single-precision to 64-bit)
- **Condition**: `sf == 1 && ftype == 00`
- **Assembly**: `FCVTAU  <Dd>, <Sn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`00`
- **Bit Pattern**: `??????????????????????00???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  011 000000 Rn  Rd  |
```

### Variant: `Floating-point (FCVTAU_sisd_32D)` (Double-precision to 32-bit)
- **Condition**: `sf == 0 && ftype == 01`
- **Assembly**: `FCVTAU  <Sd>, <Dn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`01`
- **Bit Pattern**: `??????????????????????10???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   11  011 000000 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Sd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Dd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the SIMD&FP source register, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvtau_sisd.xml`
</details>