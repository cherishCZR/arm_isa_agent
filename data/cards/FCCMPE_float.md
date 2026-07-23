## FCCMPE
_ARM A64 Instruction_

**Title**: FCCMPE -- A64 | **Class**: `float` | **XML ID**: `FCCMPE_float`

**Summary**: Floating-point conditional signaling compare (scalar)

**Description**:
This instruction compares the two SIMD&FP source register values
and writes the result to the
PSTATE.{N, Z, C, V} flags.
If the condition does not pass, then the PSTATE.{N, Z, C, V} flags
are set to the flag bit specifier.

This instruction raises an Invalid Operation floating-point exception if either or both of the operands
is any type of NaN.

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

### Variant: `Floating-point (FCCMPE_H_floatccmp)` (Half-precision)
- **Condition**: `ftype == 11`
- **Assembly**: `FCCMPE  <Hn>, <Hm>, #<nzcv>, <cond>`
- **Fixed bits**: `ftype`=`11`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  11   9   4  3  |
|--------------------------------------|
| 0   0   0   11110 ftype 1   Rm  cond 01  Rn  1   nzcv |
```

#### Decode (A64.simd_dp.floatccmp.FCCMPE_H_floatccmp)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if ftype == '10' then EndOfDecode(Decode_UNDEF);
if ftype == '11' && !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);

constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 8 << UInt(ftype EOR '10');
constant bits(4) condition = cond;
bits(4) flags = nzcv;
```

#### Execute (A64.simd_dp.floatccmp.FCCMPE_H_floatccmp)

```
CheckFPEnabled64();

constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];

if ConditionHolds(condition) then
    constant boolean signal_all_nans = TRUE;
    flags = FPCompare(operand1, operand2, signal_all_nans, FPCR);

PSTATE.<N,Z,C,V> = flags;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `ftype != '10'` |
| 🔒 FEATURE_GATE | `ftype != '11' \|\| IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Floating-point (FCCMPE_S_floatccmp)` (Single-precision)
- **Condition**: `ftype == 00`
- **Assembly**: `FCCMPE  <Sn>, <Sm>, #<nzcv>, <cond>`
- **Fixed bits**: `ftype`=`00`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  11   9   4  3  |
|--------------------------------------|
| 0   0   0   11110 ftype 1   Rm  cond 01  Rn  1   nzcv |
```

### Variant: `Floating-point (FCCMPE_D_floatccmp)` (Double-precision)
- **Condition**: `ftype == 01`
- **Assembly**: `FCCMPE  <Dn>, <Dm>, #<nzcv>, <cond>`
- **Fixed bits**: `ftype`=`01`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  11   9   4  3  |
|--------------------------------------|
| 0   0   0   11110 ftype 1   Rm  cond 01  Rn  1   nzcv |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Hm>` | `register (16-bit)` | `Rm` | Is the 16-bit name of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<nzcv>` | `unknown` | `nzcv` | Is the flag bit specifier, an immediate in the range 0 to 15, giving the alternative state for the 4-bit NZCV condition flags, encoded in the "nzcv" f |
| `<cond>` | `condition` | `cond` | Is one of the standard conditions, encoded in the standard way, and |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Sm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Dm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second SIMD&FP source register, encoded in the "Rm" field. |

**<cond> Value Table**:

| bitfield | symbol |
|---|---|
| 0000 | EQ |
| 0001 | NE |
| 0010 | CS |
| 0011 | CC |
| 0100 | MI |
| 0101 | PL |
| 0110 | VS |
| 0111 | VC |
| 1000 | HI |
| 1001 | LS |
| 1010 | GE |
| 1011 | LT |
| 1100 | GT |
| 1101 | LE |
| 1110 | AL |
| 1111 | NV |

### Operational Notes

The IEEE 754 standard specifies that the result of a comparison is precisely one of <, ==, > or unordered.  If either or both of the operands is a NaN, they are unordered, and all three of (Operand1 < Operand2), (Operand1 == Operand2) and (Operand1 > Operand2) are false. An unordered comparison sets the PSTATE condition flags to N=0, Z=0, C=1, and V=1.
        If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the NZCV condition flags written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fccmpe_float.xml`
</details>