## AESIMC
_ARM A64 Instruction_

**Title**: AESIMC -- A64 | **Class**: `advsimd` | **XML ID**: `AESIMC_advsimd`

**Architecture**: `FEAT_AES` (ARMv8.0)

**Summary**: AES inverse mix columns

**Description**:
AES inverse mix columns.

### Variant: `Advanced SIMD`
- **Assembly**: `AESIMC  <Vd>.16B, <Vn>.16B`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24 23  21  16  12 11   9   4  |
|--------------------------------|
| 0100 111 0   00  10100 0011 1   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptoaes.AESIMC_B_cryptoaes)

```
if !IsFeatureImplemented(FEAT_AES) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
```

#### Execute (A64.simd_dp.cryptoaes.AESIMC_B_cryptoaes)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) operand = V[n, 128];
V[d, 128] = AESInvMixColumns(operand);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AES)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

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
- source: `aesimc_advsimd.xml`
</details>