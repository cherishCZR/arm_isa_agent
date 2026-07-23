## XAR
_ARM A64 Instruction_

**Title**: XAR -- A64 | **Class**: `advsimd` | **XML ID**: `XAR_advsimd`

**Architecture**: `FEAT_SHA3` (ARMv8.2)

**Summary**: Exclusive-OR and rotate

**Description**:
This instruction performs a bitwise exclusive-OR of the
128-bit vectors in the two source SIMD&FP registers, rotates each
64-bit element of the resulting 128-bit vector right by the value
specified by a 6-bit immediate value, and writes the result to
the destination SIMD&FP register.

### Variant: `Advanced SIMD`
- **Assembly**: `XAR  <Vd>.2D, <Vn>.2D, <Vm>.2D, #<imm6>`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24  22  20  15   9   4  |
|--------------------------|
| 1100 111 01  00  Rm  imm6 Rn  Rd  |
```

#### Decode (A64.simd_dp.crypto3_imm6.XAR_VVV2_crypto3_imm6)

```
if !IsFeatureImplemented(FEAT_SHA3) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.simd_dp.crypto3_imm6.XAR_VVV2_crypto3_imm6)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) Vm = V[m, 128];
constant bits(128) Vn = V[n, 128];
constant bits(128) tmp = Vn EOR Vm;
V[d, 128] = ROR(tmp<127:64>, UInt(imm6)):ROR(tmp<63:0>, UInt(imm6));
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
| `<imm6>` | `immediate` | `imm6` | Is a rotation right, encoded in "imm6". |

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
- source: `xar_advsimd.xml`
</details>