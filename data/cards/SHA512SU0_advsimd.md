## SHA512SU0
_ARM A64 Instruction_

**Title**: SHA512SU0 -- A64 | **Class**: `advsimd` | **XML ID**: `SHA512SU0_advsimd`

**Architecture**: `FEAT_SHA512` (ARMv8.2)

**Summary**: SHA512 schedule update 0

**Description**:
This instruction takes the values from the two 128-bit source SIMD&FP
registers and produces a 128-bit output value that combines the gamma0 functions
of two iterations of the SHA512 schedule update that are performed after the first
16 iterations within a block. It returns this value to the destination SIMD&FP register.

### Variant: `Advanced SIMD`
- **Assembly**: `SHA512SU0  <Vd>.2D, <Vn>.2D`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24  22  18  11   9   4  |
|--------------------------|
| 1100 111 01  1000 0001000 00  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha512_2.SHA512SU0_VV2_cryptosha512_2)

```
if !IsFeatureImplemented(FEAT_SHA512) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
```

#### Execute (A64.simd_dp.cryptosha512_2.SHA512SU0_VV2_cryptosha512_2)

```
AArch64.CheckFPAdvSIMDEnabled();

bits(64) sig0;
bits(128) Vtmp;
constant bits(128) x = V[n, 128];
constant bits(128) w = V[d, 128];
sig0 = ROR(w<127:64>, 1) EOR ROR(w<127:64>, 8) EOR ('0000000':w<127:71>);
Vtmp<63:0> = w<63:0> + sig0;
sig0 = ROR(x<63:0>, 1) EOR ROR(x<63:0>, 8) EOR ('0000000':x<63:7>);
Vtmp<127:64> = w<127:64> + sig0;
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
- source: `sha512su0_advsimd.xml`
</details>