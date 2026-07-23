## MOVI
_ARM A64 Instruction_

**Title**: MOVI -- A64 | **Class**: `advsimd` | **XML ID**: `MOVI_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Move immediate (vector)

**Description**:
This instruction places an immediate constant into every vector element of the destination
SIMD&FP register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD (MOVI_asimdimm_N_b)` (8-bit)
- **Condition**: `op == 0 && cmode == 1110`
- **Assembly**: `MOVI  <Vd>.<T>, #<imm8>{, LSL #0}`
- **Fixed bits**: `op`=`0`, `cmode`=`1110`
- **Bit Pattern**: `????????????0111?????????????0??`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  18 17 16 15  11 10  9  8  7  6  5  4  |
|--------------------------------------------------|
| 0   Q   op  0111100000 a   b   c   cmode 0   1   d   e   f   g   h   Rd  |
```

#### Decode (A64.simd_dp.asimdimm.MOVI_asimdimm_N_b)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer rd = UInt(Rd);
constant integer datasize = 64 << UInt(Q);
constant bits(64) imm64 = AdvSIMDExpandImm(op, cmode, a:b:c:d:e:f:g:h);
constant bits(datasize) imm = Replicate(imm64, datasize DIV 64);
```

#### Execute (A64.simd_dp.asimdimm.MOVI_asimdimm_N_b)

```
CheckFPAdvSIMDEnabled64();
V[rd, datasize] = imm;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

### Variant: `Advanced SIMD (MOVI_asimdimm_L_hl)` (16-bit shifted immediate)
- **Condition**: `op == 0 && cmode == 10x0`
- **Assembly**: `MOVI  <Vd>.<T>, #<imm8>{, LSL #<amount>}`
- **Fixed bits**: `op`=`0`, `cmode`=`10x0`
- **Bit Pattern**: `????????????0?01?????????????0??`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  18 17 16 15  11 10  9  8  7  6  5  4  |
|--------------------------------------------------|
| 0   Q   op  0111100000 a   b   c   cmode 0   1   d   e   f   g   h   Rd  |
```

### Variant: `Advanced SIMD (MOVI_asimdimm_L_sl)` (32-bit shifted immediate)
- **Condition**: `op == 0 && cmode == 0xx0`
- **Assembly**: `MOVI  <Vd>.<T>, #<imm8>{, LSL #<amount>}`
- **Fixed bits**: `op`=`0`, `cmode`=`0xx0`
- **Bit Pattern**: `????????????0??0?????????????0??`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  18 17 16 15  11 10  9  8  7  6  5  4  |
|--------------------------------------------------|
| 0   Q   op  0111100000 a   b   c   cmode 0   1   d   e   f   g   h   Rd  |
```

### Variant: `Advanced SIMD (MOVI_asimdimm_M_sm)` (32-bit shifting ones)
- **Condition**: `op == 0 && cmode == 110x`
- **Assembly**: `MOVI  <Vd>.<T>, #<imm8>, MSL #<amount>`
- **Fixed bits**: `op`=`0`, `cmode`=`110x`
- **Bit Pattern**: `?????????????011?????????????0??`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  18 17 16 15  11 10  9  8  7  6  5  4  |
|--------------------------------------------------|
| 0   Q   op  0111100000 a   b   c   cmode 0   1   d   e   f   g   h   Rd  |
```

### Variant: `Advanced SIMD (MOVI_asimdimm_D_ds)` (64-bit scalar)
- **Condition**: `Q == 0 && op == 1 && cmode == 1110`
- **Assembly**: `MOVI  <Dd>, #<imm>`
- **Fixed bits**: `Q`=`0`, `op`=`1`, `cmode`=`1110`
- **Bit Pattern**: `????????????0111?????????????10?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  18 17 16 15  11 10  9  8  7  6  5  4  |
|--------------------------------------------------|
| 0   Q   op  0111100000 a   b   c   cmode 0   1   d   e   f   g   h   Rd  |
```

### Variant: `Advanced SIMD (MOVI_asimdimm_D2_d)` (64-bit vector)
- **Condition**: `Q == 1 && op == 1 && cmode == 1110`
- **Assembly**: `MOVI  <Vd>.2D, #<imm>`
- **Fixed bits**: `Q`=`1`, `op`=`1`, `cmode`=`1110`
- **Bit Pattern**: `????????????0111?????????????11?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  18 17 16 15  11 10  9  8  7  6  5  4  |
|--------------------------------------------------|
| 0   Q   op  0111100000 a   b   c   cmode 0   1   d   e   f   g   h   Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | For the "8-bit" variant: is an arrangement specifier, |
| `<T>` | `unknown` | `Q` | For the "16-bit shifted immediate" variant: is an arrangement specifier, |
| `<T>` | `unknown` | `Q` | For the "32-bit shifted immediate" and "32-bit shifting ones" variants: is an arrangement specifier, |
| `<imm8>` | `immediate` | `a:b:c:d:e:f:g:h` | Is an 8-bit immediate encoded in "a:b:c:d:e:f:g:h". |
| `<amount>` | `unknown` | `cmode<1>` | For the "16-bit shifted immediate" variant: is the shift amount |
| `<amount>` | `unknown` | `cmode<2:1>` | For the "32-bit shifted immediate" variant: is the shift amount |
| `<amount>` | `unknown` | `cmode<0>` | For the "32-bit shifting ones" variant: is the shift amount |
| `<Dd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<imm>` | `immediate` | `a:b:c:d:e:f:g:h` | Is a 64-bit immediate 'aaaaaaaabbbbbbbbccccccccddddddddeeeeeeeeffffffffgggggggghhhhhhhh', encoded in "a:b:c:d:e:f:g:h". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |

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

**<amount> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 0 |
| 1 | 8 |

**<amount> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | 0 |
| 01 | 8 |
| 10 | 16 |
| 11 | 24 |

**<amount> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8 |
| 1 | 16 |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `movi_advsimd.xml`
</details>