## FMOV
_ARM A64 Instruction_

**Title**: FMOV (vector, immediate) -- A64 | **Class**: `advsimd` | **XML ID**: `FMOV_advsimd`

**Architecture**: `FEAT_AdvSIMD && FEAT_FP16` (FEAT_AdvSIMD && FEAT_FP16), `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Floating-point move immediate (vector)

**Description**:
This instruction copies an immediate
floating-point constant into every element of the SIMD&FP destination register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Half-precision`
- **Assembly**: `FMOV  <Vd>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  18 17 16 15  11 10  9  8  7  6  5  4  |
|-----------------------------------------------------------|
| 0   Q   0   0   111 10  0000 a   b   c   1111 1   1   d   e   f   g   h   Rd  |
```

#### Decode (A64.simd_dp.asimdimm.FMOV_asimdimm_H_h)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_FP16) then
    EndOfDecode(Decode_UNDEF);

constant integer rd = UInt(Rd);

constant integer datasize = 64 << UInt(Q);
constant bits(8) imm8 = a:b:c:d:e:f:g:h;
constant bits(16) imm16 = imm8<7>:NOT(imm8<6>):Replicate(imm8<6>, 2):imm8<5:0>:Zeros(6);
constant bits(datasize) imm = Replicate(imm16, datasize DIV 16);
```

#### Execute (A64.simd_dp.asimdimm.FMOV_asimdimm_H_h)

```
CheckFPAdvSIMDEnabled64();
V[rd, datasize] = imm;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Single-precision and double-precision (FMOV_asimdimm_S_s)` (Single-precision)
- **Condition**: `op == 0`
- **Assembly**: `FMOV  <Vd>.<T>, #<imm>`
- **Fixed bits**: `op`=`0`
- **Bit Pattern**: `?????????????????????????????0??`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  18 17 16 15  11 10  9  8  7  6  5  4  |
|--------------------------------------------------|
| 0   Q   op  0111100000 a   b   c   1111 0   1   d   e   f   g   h   Rd  |
```

#### Decode (A64.simd_dp.asimdimm.FMOV_asimdimm_S_s)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if cmode:op == '11111' then
    // FMOV Dn,#imm is in main FP instruction set
    if Q == '0' then EndOfDecode(Decode_UNDEF);

constant integer rd = UInt(Rd);
constant integer datasize = 64 << UInt(Q);
constant bits(64) imm64 = AdvSIMDExpandImm(op, cmode, a:b:c:d:e:f:g:h);
constant bits(datasize) imm = Replicate(imm64, datasize DIV 64);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `Q != '0'` |

### Variant: `Single-precision and double-precision (FMOV_asimdimm_D2_d)` (Double-precision)
- **Condition**: `Q == 1 && op == 1`
- **Assembly**: `FMOV  <Vd>.2D, #<imm>`
- **Fixed bits**: `Q`=`1`, `op`=`1`
- **Bit Pattern**: `?????????????????????????????11?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  18 17 16 15  11 10  9  8  7  6  5  4  |
|--------------------------------------------------|
| 0   Q   op  0111100000 a   b   c   1111 0   1   d   e   f   g   h   Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | For the "Half-precision" variant: is an arrangement specifier, |
| `<T>` | `unknown` | `Q` | For the "Single-precision" variant: is an arrangement specifier, |
| `<imm>` | `immediate` | `a:b:c:d:e:f:g:h` | Is a signed floating-point constant with 3-bit exponent and normalized 4 bits of precision, encoded in "a:b:c:d:e:f:g:h". For details of the range of  |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4H |
| 1 | 8H |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2S |
| 1 | 4S |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmov_advsimd.xml`
</details>