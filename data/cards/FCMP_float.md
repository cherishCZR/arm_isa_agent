## FCMP
_ARM A64 Instruction_

**Title**: FCMP -- A64 | **Class**: `float` | **XML ID**: `FCMP_float`

**Summary**: Floating-point quiet compare (scalar)

**Description**:
This instruction compares the two SIMD&FP source register values,
or the first SIMD&FP source register value and zero. It writes the result to the
PSTATE.{N, Z, C, V} flags.

This instruction raises an Invalid Operation floating-point exception if either or both of the operands
is a signaling NaN.

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

### Variant: `Floating-point (FCMP_H_floatcmp)` (Half-precision)
- **Condition**: `ftype == 11 && opc == 00`
- **Assembly**: `FCMP  <Hn>, <Hm>`
- **Fixed bits**: `ftype`=`11`, `opc`=`0`
- **Bit Pattern**: `???0??????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  13   9   4   2  |
|--------------------------------------|
| 0   0   0   11110 ftype 1   Rm  00  1000 Rn  0x  000 |
```

#### Decode (A64.simd_dp.floatcmp.FCMP_H_floatcmp)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if ftype == '10' then EndOfDecode(Decode_UNDEF);
if ftype == '11' && !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);

constant integer n = UInt(Rn);
constant integer m = UInt(Rm);   // ignored when opc<0> == '1'

constant integer datasize = 8 << UInt(ftype EOR '10');
constant boolean signal_all_nans = FALSE;
constant boolean cmp_with_zero = (opc<0> == '1');
```

#### Execute (A64.simd_dp.floatcmp.FCMP_H_floatcmp)

```
CheckFPEnabled64();

constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = if cmp_with_zero then FPZero('0', datasize) else V[m, datasize];

PSTATE.<N,Z,C,V> = FPCompare(operand1, operand2, signal_all_nans, FPCR);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `ftype != '10'` |
| 🔒 FEATURE_GATE | `ftype != '11' \|\| IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Floating-point (FCMP_HZ_floatcmp)` (Half-precision, zero)
- **Condition**: `ftype == 11 && Rm == (00000) && opc == 01`
- **Assembly**: `FCMP  <Hn>, #0.0`
- **Fixed bits**: `ftype`=`11`, `Rm`=`(0)(0)(0)(0)(0)`, `opc`=`1`
- **Bit Pattern**: `???1??????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  13   9   4   2  |
|--------------------------------------|
| 0   0   0   11110 ftype 1   Rm  00  1000 Rn  0x  000 |
```

### Variant: `Floating-point (FCMP_S_floatcmp)` (Single-precision)
- **Condition**: `ftype == 00 && opc == 00`
- **Assembly**: `FCMP  <Sn>, <Sm>`
- **Fixed bits**: `ftype`=`00`, `opc`=`0`
- **Bit Pattern**: `???0??????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  13   9   4   2  |
|--------------------------------------|
| 0   0   0   11110 ftype 1   Rm  00  1000 Rn  0x  000 |
```

### Variant: `Floating-point (FCMP_SZ_floatcmp)` (Single-precision, zero)
- **Condition**: `ftype == 00 && Rm == (00000) && opc == 01`
- **Assembly**: `FCMP  <Sn>, #0.0`
- **Fixed bits**: `ftype`=`00`, `Rm`=`(0)(0)(0)(0)(0)`, `opc`=`1`
- **Bit Pattern**: `???1??????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  13   9   4   2  |
|--------------------------------------|
| 0   0   0   11110 ftype 1   Rm  00  1000 Rn  0x  000 |
```

### Variant: `Floating-point (FCMP_D_floatcmp)` (Double-precision)
- **Condition**: `ftype == 01 && opc == 00`
- **Assembly**: `FCMP  <Dn>, <Dm>`
- **Fixed bits**: `ftype`=`01`, `opc`=`0`
- **Bit Pattern**: `???0??????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  13   9   4   2  |
|--------------------------------------|
| 0   0   0   11110 ftype 1   Rm  00  1000 Rn  0x  000 |
```

### Variant: `Floating-point (FCMP_DZ_floatcmp)` (Double-precision, zero)
- **Condition**: `ftype == 01 && Rm == (00000) && opc == 01`
- **Assembly**: `FCMP  <Dn>, #0.0`
- **Fixed bits**: `ftype`=`01`, `Rm`=`(0)(0)(0)(0)(0)`, `opc`=`1`
- **Bit Pattern**: `???1??????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  13   9   4   2  |
|--------------------------------------|
| 0   0   0   11110 ftype 1   Rm  00  1000 Rn  0x  000 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hn>` | `register (16-bit)` | `Rn` | For the "Half-precision" variant: is the 16-bit name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Hn>` | `register (16-bit)` | `Rn` | For the "Half-precision, zero" variant: is the 16-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Hm>` | `register (16-bit)` | `Rm` | Is the 16-bit name of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | For the "Single-precision" variant: is the 32-bit name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | For the "Single-precision, zero" variant: is the 32-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Sm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | For the "Double-precision" variant: is the 64-bit name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | For the "Double-precision, zero" variant: is the 64-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Dm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second SIMD&FP source register, encoded in the "Rm" field. |

### Operational Notes

The IEEE 754 standard specifies that the result of a comparison is precisely one of <, ==, > or unordered.  If either or both of the operands is a NaN, they are unordered, and all three of (Operand1 < Operand2), (Operand1 == Operand2) and (Operand1 > Operand2) are false. An unordered comparison sets the PSTATE condition flags to N=0, Z=0, C=1, and V=1.
        If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the NZCV condition flags written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcmp_float.xml`
</details>