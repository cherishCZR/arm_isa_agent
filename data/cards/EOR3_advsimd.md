## EOR3
_ARM A64 Instruction_

**Title**: EOR3 -- A64 | **Class**: `advsimd` | **XML ID**: `EOR3_advsimd`

**Architecture**: `FEAT_SHA3` (ARMv8.2)

**Summary**: Three-way exclusive-OR

**Description**:
This instruction performs a three-way exclusive-OR of the values in the three
source SIMD&FP registers, and writes the result to the destination SIMD&FP register.

### Variant: `Advanced SIMD`
- **Assembly**: `EOR3  <Vd>.16B, <Vn>.16B, <Vm>.16B, <Va>.16B`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24  22  20  15 14   9   4  |
|-----------------------------|
| 1100 111 00  00  Rm  0   Ra  Rn  Rd  |
```

#### Decode (A64.simd_dp.crypto4.EOR3_VVV16_crypto4)

```
if !IsFeatureImplemented(FEAT_SHA3) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer a = UInt(Ra);
```

#### Execute (A64.simd_dp.crypto4.EOR3_VVV16_crypto4)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) operand1 = V[m, 128];
constant bits(128) operand2 = V[n, 128];
constant bits(128) operand3 = V[a, 128];
V[d, 128] = operand2 EOR operand1 EOR operand3;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SHA3)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<Va>` | `register (128-bit)` | `Ra` | Is the name of the third SIMD&FP source register, encoded in the "Ra" field. |

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
- source: `eor3_advsimd.xml`
</details>