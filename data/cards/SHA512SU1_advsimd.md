## SHA512SU1
_ARM A64 Instruction_

**Title**: SHA512SU1 -- A64 | **Class**: `advsimd` | **XML ID**: `SHA512SU1_advsimd`

**Architecture**: `FEAT_SHA512` (ARMv8.2)

**Summary**: SHA512 schedule update 1

**Description**:
This instruction takes the values from the three source SIMD&FP registers
and produces a 128-bit output value that combines the gamma1 functions of two
iterations of the SHA512 schedule update that are performed after the first 16
iterations within a block. It returns this value to the destination SIMD&FP
register.

### Variant: `Advanced SIMD`
- **Assembly**: `SHA512SU1  <Vd>.2D, <Vn>.2D, <Vm>.2D`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24  22  20  15 14 13  11   9   4  |
|-----------------------------------|
| 1100 111 00  11  Rm  1   0   00  10  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha512_3.SHA512SU1_VVV2_cryptosha512_3)

```
if !IsFeatureImplemented(FEAT_SHA512) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.simd_dp.cryptosha512_3.SHA512SU1_VVV2_cryptosha512_3)

```
AArch64.CheckFPAdvSIMDEnabled();

bits(64) sig1;
bits(128) Vtmp;
constant bits(128) x = V[n, 128];
constant bits(128) y = V[m, 128];
constant bits(128) w = V[d, 128];

sig1 = ROR(x<127:64>, 19) EOR ROR(x<127:64>, 61) EOR ('000000':x<127:70>);
Vtmp<127:64> = w<127:64> + sig1 + y<127:64>;
sig1 = ROR(x<63:0>, 19) EOR ROR(x<63:0>, 61) EOR ('000000':x<63:6>);
Vtmp<63:0> = w<63:0> + sig1 + y<63:0>;
V[d, 128] = Vtmp;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SHA512)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP source and destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the second SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the third SIMD&FP source register, encoded in the "Rm" field. |

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
- source: `sha512su1_advsimd.xml`
</details>