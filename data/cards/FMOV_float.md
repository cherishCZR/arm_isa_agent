## FMOV
_ARM A64 Instruction_

**Title**: FMOV (register) -- A64 | **Class**: `float` | **XML ID**: `FMOV_float`

**Summary**: Floating-point move register without conversion

**Description**:
This instruction copies the
floating-point value
in the SIMD&FP source register to
the SIMD&FP destination register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Floating-point (FMOV_H_floatdp1)` (Half-precision)
- **Condition**: `ftype == 11`
- **Assembly**: `FMOV  <Hd>, <Hn>`
- **Fixed bits**: `ftype`=`11`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  14   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 10000 00  10000 Rn  Rd  |
```

#### Decode (A64.simd_dp.floatdp1.FMOV_H_floatdp1)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if ftype == '10' then EndOfDecode(Decode_UNDEF);
if ftype == '11' && !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 8 << UInt(ftype EOR '10');
```

#### Execute (A64.simd_dp.floatdp1.FMOV_H_floatdp1)

```
CheckFPEnabled64();

constant bits(esize) operand = V[n, esize];
bits(128) result = Zeros(128);

Elem[result, 0, esize] = operand;

V[d, 128] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `ftype != '10'` |
| 🔒 FEATURE_GATE | `ftype != '11' \|\| IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Floating-point (FMOV_S_floatdp1)` (Single-precision)
- **Condition**: `ftype == 00`
- **Assembly**: `FMOV  <Sd>, <Sn>`
- **Fixed bits**: `ftype`=`00`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  14   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 10000 00  10000 Rn  Rd  |
```

### Variant: `Floating-point (FMOV_D_floatdp1)` (Double-precision)
- **Condition**: `ftype == 01`
- **Assembly**: `FMOV  <Dd>, <Dn>`
- **Fixed bits**: `ftype`=`01`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21  16  14   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 10000 00  10000 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hd>` | `register (16-bit)` | `Rd` | Is the 16-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Sd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Dd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the SIMD&FP source register, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmov_float.xml`
</details>