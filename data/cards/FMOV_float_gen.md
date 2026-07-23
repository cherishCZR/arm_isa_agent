## FMOV
_ARM A64 Instruction_

**Title**: FMOV (general) -- A64 | **Class**: `float` | **XML ID**: `FMOV_float_gen`

**Summary**: Floating-point move to or from general-purpose register without conversion

**Description**:
This instruction transfers the contents of a SIMD&FP register
to a general-purpose register, or the contents of a general-purpose
register to a SIMD&FP register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Floating-point (FMOV_32H_float2int)` (Half-precision to 32-bit)
- **Condition**: `sf == 0 && ftype == 11 && rmode == 00 && opcode == 110`
- **Assembly**: `FMOV  <Wd>, <Hn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`11`, `rmode`=`0`, `opcode`=`0`
- **Bit Pattern**: `????????????????0??0??11???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   0x  11x 000000 Rn  Rd  |
```

#### Decode (A64.simd_dp.float2int.FMOV_32H_float2int)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if ftype == '10' && opcode<2:1>:rmode != '11 01' then EndOfDecode(Decode_UNDEF);
if ftype == '11' && !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer intsize = 32 << UInt(sf);
constant integer fltsize = if ftype == '10' then 64 else (8 << UInt(ftype EOR '10'));
constant integer part = UInt(rmode<0>);
FPConvOp op;

case opcode<2:1>:rmode of
    when '11 00'        // FMOV
        if fltsize != 16 && fltsize != intsize then EndOfDecode(Decode_UNDEF);
        op = if opcode<0> == '1' then FPConvOp_MOV_ItoF else FPConvOp_MOV_FtoI;
    when '11 01'        // FMOV D[1]
        if intsize != 64 || ftype != '10' then EndOfDecode(Decode_UNDEF);
        op = if opcode<0> == '1' then FPConvOp_MOV_ItoF else FPConvOp_MOV_FtoI;
    otherwise
        Unreachable();
```

#### Execute (A64.simd_dp.float2int.FMOV_32H_float2int)

```
CheckFPEnabled64();

bits(fltsize) fltval;
bits(intsize) intval;

case op of
    when FPConvOp_MOV_FtoI
        fltval = Vpart[n, part, fltsize];
        X[d, intsize] = ZeroExtend(fltval, intsize);
    when FPConvOp_MOV_ItoF
        intval = X[n, intsize];
        Vpart[d, part, fltsize] = intval<fltsize-1:0>;
    otherwise
        Unreachable();
```

#### Constraints
_3× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `ftype != '10' \|\| opcode<2:1>:rmode == '11 01'` |
| 🔒 FEATURE_GATE | `ftype != '11' \|\| IsFeatureImplemented(FEAT_FP16)` |
| 🚫 ENCODING_UNDEF | `fltsize == 16 \|\| fltsize == intsize` |
| 🚫 ENCODING_UNDEF | `intsize == 64 && ftype == '10'` |

### Variant: `Floating-point (FMOV_64H_float2int)` (Half-precision to 64-bit)
- **Condition**: `sf == 1 && ftype == 11 && rmode == 00 && opcode == 110`
- **Assembly**: `FMOV  <Xd>, <Hn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`11`, `rmode`=`0`, `opcode`=`0`
- **Bit Pattern**: `????????????????0??0??11???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   0x  11x 000000 Rn  Rd  |
```

### Variant: `Floating-point (FMOV_H32_float2int)` (32-bit to half-precision)
- **Condition**: `sf == 0 && ftype == 11 && rmode == 00 && opcode == 111`
- **Assembly**: `FMOV  <Hd>, <Wn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`11`, `rmode`=`0`, `opcode`=`1`
- **Bit Pattern**: `????????????????1??0??11???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   0x  11x 000000 Rn  Rd  |
```

### Variant: `Floating-point (FMOV_S32_float2int)` (32-bit to single-precision)
- **Condition**: `sf == 0 && ftype == 00 && rmode == 00 && opcode == 111`
- **Assembly**: `FMOV  <Sd>, <Wn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`00`, `rmode`=`0`, `opcode`=`1`
- **Bit Pattern**: `????????????????1??0??00???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   0x  11x 000000 Rn  Rd  |
```

### Variant: `Floating-point (FMOV_32S_float2int)` (Single-precision to 32-bit)
- **Condition**: `sf == 0 && ftype == 00 && rmode == 00 && opcode == 110`
- **Assembly**: `FMOV  <Wd>, <Sn>`
- **Fixed bits**: `sf`=`0`, `ftype`=`00`, `rmode`=`0`, `opcode`=`0`
- **Bit Pattern**: `????????????????0??0??00???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   0x  11x 000000 Rn  Rd  |
```

### Variant: `Floating-point (FMOV_H64_float2int)` (64-bit to half-precision)
- **Condition**: `sf == 1 && ftype == 11 && rmode == 00 && opcode == 111`
- **Assembly**: `FMOV  <Hd>, <Xn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`11`, `rmode`=`0`, `opcode`=`1`
- **Bit Pattern**: `????????????????1??0??11???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   0x  11x 000000 Rn  Rd  |
```

### Variant: `Floating-point (FMOV_D64_float2int)` (64-bit to double-precision)
- **Condition**: `sf == 1 && ftype == 01 && rmode == 00 && opcode == 111`
- **Assembly**: `FMOV  <Dd>, <Xn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`01`, `rmode`=`0`, `opcode`=`1`
- **Bit Pattern**: `????????????????1??0??10???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   0x  11x 000000 Rn  Rd  |
```

### Variant: `Floating-point (FMOV_V64I_float2int)` (64-bit to top half of 128-bit)
- **Condition**: `sf == 1 && ftype == 10 && rmode == 01 && opcode == 111`
- **Assembly**: `FMOV  <Vd>.D[1], <Xn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`10`, `rmode`=`1`, `opcode`=`1`
- **Bit Pattern**: `????????????????1??1??01???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   0x  11x 000000 Rn  Rd  |
```

### Variant: `Floating-point (FMOV_64D_float2int)` (Double-precision to 64-bit)
- **Condition**: `sf == 1 && ftype == 01 && rmode == 00 && opcode == 110`
- **Assembly**: `FMOV  <Xd>, <Dn>`
- **Fixed bits**: `sf`=`1`, `ftype`=`01`, `rmode`=`0`, `opcode`=`0`
- **Bit Pattern**: `????????????????0??0??10???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   0x  11x 000000 Rn  Rd  |
```

### Variant: `Floating-point (FMOV_64VX_float2int)` (Top half of 128-bit to 64-bit)
- **Condition**: `sf == 1 && ftype == 10 && rmode == 01 && opcode == 110`
- **Assembly**: `FMOV  <Xd>, <Vn>.D[1]`
- **Fixed bits**: `sf`=`1`, `ftype`=`10`, `rmode`=`1`, `opcode`=`0`
- **Bit Pattern**: `????????????????0??1??01???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  18  15   9   4  |
|-----------------------------------|
| sf  0   0   11110 ftype 1   0x  11x 000000 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Hd>` | `register (16-bit)` | `Rd` | Is the 16-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<Sd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<Dd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

### Operational Notes

If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the general-purpose register written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmov_float_gen.xml`
</details>