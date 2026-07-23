## SHA512H2
_ARM A64 Instruction_

**Title**: SHA512H2 -- A64 | **Class**: `advsimd` | **XML ID**: `SHA512H2_advsimd`

**Architecture**: `FEAT_SHA512` (ARMv8.2)

**Summary**: SHA512 hash update part 2

**Description**:
This instruction takes the values from the three 128-bit source SIMD&FP
registers and produces a 128-bit output value that combines the sigma0 and majority
functions of two iterations of the SHA512 computation. It returns this value to the
destination SIMD&FP register.

### Variant: `Advanced SIMD`
- **Assembly**: `SHA512H2  <Qd>, <Qn>, <Vm>.2D`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24  22  20  15 14 13  11   9   4  |
|-----------------------------------|
| 1100 111 00  11  Rm  1   0   00  01  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha512_3.SHA512H2_QQV_cryptosha512_3)

```
if !IsFeatureImplemented(FEAT_SHA512) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.simd_dp.cryptosha512_3.SHA512H2_QQV_cryptosha512_3)

```
AArch64.CheckFPAdvSIMDEnabled();

bits(128) Vtmp;
bits(64) NSigma0;
constant bits(128) x = V[n, 128];
constant bits(128) y = V[m, 128];
constant bits(128) w = V[d, 128];

NSigma0 =  ROR(y<63:0>, 28) EOR ROR(y<63:0>, 34) EOR ROR(y<63:0>, 39);
Vtmp<127:64> = SHAmajority(x<63:0>, y<127:64>, y<63:0>);
Vtmp<127:64> = (Vtmp<127:64> + NSigma0 +  w<127:64>);
NSigma0 =  ROR(Vtmp<127:64>, 28) EOR ROR(Vtmp<127:64>, 34) EOR ROR(Vtmp<127:64>, 39);
Vtmp<63:0> = SHAmajority(Vtmp<127:64>, y<63:0>, y<127:64>);
Vtmp<63:0> =   (Vtmp<63:0> + NSigma0 + w<63:0>);

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
- source: `sha512h2_advsimd.xml`
</details>