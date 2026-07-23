## SHA512H
_ARM A64 Instruction_

**Title**: SHA512H -- A64 | **Class**: `advsimd` | **XML ID**: `SHA512H_advsimd`

**Architecture**: `FEAT_SHA512` (ARMv8.2)

**Summary**: SHA512 hash update part 1

**Description**:
This instruction takes the values from the three 128-bit source SIMD&FP
registers and produces a 128-bit output value that combines the sigma1 and chi
functions of two iterations of the SHA512 computation. It returns this value to the
destination SIMD&FP register.

### Variant: `Advanced SIMD`
- **Assembly**: `SHA512H  <Qd>, <Qn>, <Vm>.2D`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24  22  20  15 14 13  11   9   4  |
|-----------------------------------|
| 1100 111 00  11  Rm  1   0   00  00  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha512_3.SHA512H_QQV_cryptosha512_3)

```
if !IsFeatureImplemented(FEAT_SHA512) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.simd_dp.cryptosha512_3.SHA512H_QQV_cryptosha512_3)

```
AArch64.CheckFPAdvSIMDEnabled();

bits(128) Vtmp;
bits(64)  MSigma1;
bits(64)  tmp;
constant bits(128) x = V[n, 128];
constant bits(128) y = V[m, 128];
constant bits(128) w = V[d, 128];

MSigma1 =  ROR(y<127:64>, 14) EOR ROR(y<127:64>, 18) EOR ROR(y<127:64>, 41);
Vtmp<127:64> =  (y<127:64> AND x<63:0>) EOR (NOT(y<127:64>) AND x<127:64>);
Vtmp<127:64> = (Vtmp<127:64> + MSigma1 +  w<127:64>);
tmp = Vtmp<127:64> + y<63:0>;
MSigma1 = ROR(tmp, 14) EOR ROR(tmp, 18) EOR ROR(tmp, 41);
Vtmp<63:0> = (tmp AND y<127:64>) EOR (NOT(tmp) AND x<63:0>);
Vtmp<63:0> = (Vtmp<63:0> + MSigma1 + w<63:0>);
V[d, 128] =  Vtmp;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SHA512)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Qd>` | `register (128-bit)` | `Rd` | Is the 128-bit name of the SIMD&FP source and destination register, encoded in the "Rd" field. |
| `<Qn>` | `register (128-bit)` | `Rn` | Is the 128-bit name of the second SIMD&FP source register, encoded in the "Rn" field. |
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
- source: `sha512h_advsimd.xml`
</details>