## FMOV
_ARM A64 Instruction_

**Title**: FMOV (scalar, immediate) -- A64 | **Class**: `float` | **XML ID**: `FMOV_float_imm`

**Summary**: Floating-point move immediate (scalar)

**Description**:
This instruction copies a floating-point immediate
constant into the SIMD&FP destination register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Floating point constant in 8 bits (FMOV_H_floatimm)` (Half-precision)
- **Condition**: `ftype == 11`
- **Assembly**: `FMOV  <Hd>, #<imm>`
- **Fixed bits**: `ftype`=`11`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  12   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 1   imm8 100 00000 Rd  |
```

#### Decode (A64.simd_dp.floatimm.FMOV_H_floatimm)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if ftype == '10' then EndOfDecode(Decode_UNDEF);
if ftype == '11' && !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);

constant integer datasize = 8 << UInt(ftype EOR '10');
constant bits(datasize) imm = VFPExpandImm(imm8, datasize);
```

#### Execute (A64.simd_dp.floatimm.FMOV_H_floatimm)

```
CheckFPEnabled64();

V[d, datasize] = imm;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `ftype != '10'` |
| 🔒 FEATURE_GATE | `ftype != '11' \|\| IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Floating point constant in 8 bits (FMOV_S_floatimm)` (Single-precision)
- **Condition**: `ftype == 00`
- **Assembly**: `FMOV  <Sd>, #<imm>`
- **Fixed bits**: `ftype`=`00`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  12   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 1   imm8 100 00000 Rd  |
```

### Variant: `Floating point constant in 8 bits (FMOV_D_floatimm)` (Double-precision)
- **Condition**: `ftype == 01`
- **Assembly**: `FMOV  <Dd>, #<imm>`
- **Fixed bits**: `ftype`=`01`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  12   9   4  |
|--------------------------------|
| 0   0   0   11110 ftype 1   imm8 100 00000 Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hd>` | `register (16-bit)` | `Rd` | Is the 16-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<imm>` | `immediate` | `imm8` | Is a signed floating-point constant with 3-bit exponent and normalized 4 bits of precision, encoded in the "imm8" field. For details of the range of c |
| `<Sd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Dd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |

---
<details><summary>Metadata</summary>

- immediate-type: `imm8f`
- isa: `A64`
- source: `fmov_float_imm.xml`
</details>