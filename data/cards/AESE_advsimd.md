## AESE
_ARM A64 Instruction_

**Title**: AESE -- A64 | **Class**: `advsimd` | **XML ID**: `AESE_advsimd`

**Architecture**: `FEAT_AES` (ARMv8.0)

**Summary**: AES single round encryption

**Description**:
AES single round encryption.

### Variant: `Advanced SIMD`
- **Assembly**: `AESE  <Vd>.16B, <Vn>.16B`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24 23  21  16  12 11   9   4  |
|--------------------------------|
| 0100 111 0   00  10100 0010 0   10  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptoaes.AESE_B_cryptoaes)

```
if !IsFeatureImplemented(FEAT_AES) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
```

#### Execute (A64.simd_dp.cryptoaes.AESE_B_cryptoaes)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) operand1 = V[d, 128];
constant bits(128) operand2 = V[n, 128];
bits(128) result = operand1 EOR operand2;
result = AESShiftRows(result);
V[d, 128] = AESSubBytes(result);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AES)` |

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
- source: `aese_advsimd.xml`
</details>