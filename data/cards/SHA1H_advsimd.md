## SHA1H
_ARM A64 Instruction_

**Title**: SHA1H -- A64 | **Class**: `advsimd` | **XML ID**: `SHA1H_advsimd`

**Architecture**: `FEAT_SHA1` (ARMv8.0)

**Summary**: SHA1 fixed rotate

**Description**:
SHA1 fixed rotate.

### Variant: `Advanced SIMD`
- **Assembly**: `SHA1H  <Sd>, <Sn>`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24 23  21  16  11   9   4  |
|-----------------------------|
| 0101 111 0   00  10100 00000 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha2.SHA1H_SS_cryptosha2)

```
if !IsFeatureImplemented(FEAT_SHA1) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
```

#### Execute (A64.simd_dp.cryptosha2.SHA1H_SS_cryptosha2)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(32) operand = V[n, 32];        // read element [0] only,  [1-3] zeroed
V[d, 32] = ROL(operand, 30);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SHA1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Sd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the SIMD&FP source register, encoded in the "Rn" field. |

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
- source: `sha1h_advsimd.xml`
</details>