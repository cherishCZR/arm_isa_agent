## ORR
_ARM A64 Instruction_

**Title**: ORR (vector, immediate) -- A64 | **Class**: `advsimd` | **XML ID**: `ORR_advsimd_imm`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Bitwise inclusive OR (vector, immediate)

**Description**:
This instruction reads each vector element from the destination
SIMD&FP register, performs a bitwise OR between each result
and an immediate constant, places the result into
a vector, and writes the vector to the
destination SIMD&FP register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Shifted immediate (ORR_asimdimm_L_hl)` (16-bit)
- **Condition**: `cmode == 10x1`
- **Assembly**: `ORR  <Vd>.<T>, #<imm8>{, LSL #<amount>}`
- **Fixed bits**: `cmode`=`10`
- **Bit Pattern**: `??????????????01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  18 17 16 15  11 10  9  8  7  6  5  4  |
|--------------------------------------------------|
| 0   Q   0   0111100000 a   b   c   xxx1 0   1   d   e   f   g   h   Rd  |
```

#### Decode (A64.simd_dp.asimdimm.ORR_asimdimm_L_hl)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer rd = UInt(Rd);
constant integer datasize = 64 << UInt(Q);
constant bits(64) imm64 = AdvSIMDExpandImm(op, cmode, a:b:c:d:e:f:g:h);
constant bits(datasize) imm = Replicate(imm64, datasize DIV 64);
```

#### Execute (A64.simd_dp.asimdimm.ORR_asimdimm_L_hl)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[rd, datasize];
V[rd, datasize] = operand OR imm;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

### Variant: `Shifted immediate (ORR_asimdimm_L_sl)` (32-bit)
- **Condition**: `cmode == 0xx1`
- **Assembly**: `ORR  <Vd>.<T>, #<imm8>{, LSL #<amount>}`
- **Fixed bits**: `cmode`=`0x`
- **Bit Pattern**: `???????????????0????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  18 17 16 15  11 10  9  8  7  6  5  4  |
|--------------------------------------------------|
| 0   Q   0   0111100000 a   b   c   xxx1 0   1   d   e   f   g   h   Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | For the "16-bit" variant: is an arrangement specifier, |
| `<T>` | `unknown` | `Q` | For the "32-bit" variant: is an arrangement specifier, |
| `<imm8>` | `immediate` | `a:b:c:d:e:f:g:h` | Is an 8-bit immediate encoded in "a:b:c:d:e:f:g:h". |
| `<amount>` | `unknown` | `cmode<1>` | For the "16-bit" variant: is the shift amount |
| `<amount>` | `unknown` | `cmode<2:1>` | For the "32-bit" variant: is the shift amount |

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

- asimdimm-immtype: `shifted-immediate`
- isa: `A64`
- source: `orr_advsimd_imm.xml`
</details>