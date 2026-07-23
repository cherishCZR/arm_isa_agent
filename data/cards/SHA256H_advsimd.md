## SHA256H
_ARM A64 Instruction_

**Title**: SHA256H -- A64 | **Class**: `advsimd` | **XML ID**: `SHA256H_advsimd`

**Architecture**: `FEAT_SHA256` (ARMv8.0)

**Summary**: SHA256 hash update (part 1)

**Description**:
SHA256 hash update (part 1).

### Variant: `Advanced SIMD`
- **Assembly**: `SHA256H  <Qd>, <Qn>, <Vm>.4S`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24 23  21 20  15 14  12 11   9   4  |
|--------------------------------------|
| 0101 111 0   00  0   Rm  0   10  0   00  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha3.SHA256H_QQV_cryptosha3)

```
if !IsFeatureImplemented(FEAT_SHA256) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.simd_dp.cryptosha3.SHA256H_QQV_cryptosha3)

```
AArch64.CheckFPAdvSIMDEnabled();

constant boolean part1 = TRUE;
V[d, 128] = SHA256hash(V[d, 128], V[n, 128], V[m, 128], part1);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SHA256)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Qd>` | `register (128-bit)` | `Rd` | Is the 128-bit name of the SIMD&FP source and destination, encoded in the "Rd" field. |
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
- source: `sha256h_advsimd.xml`
</details>