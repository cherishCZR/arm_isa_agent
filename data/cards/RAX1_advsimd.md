## RAX1
_ARM A64 Instruction_

**Title**: RAX1 -- A64 | **Class**: `advsimd` | **XML ID**: `RAX1_advsimd`

**Architecture**: `FEAT_SHA3` (ARMv8.2)

**Summary**: Rotate and exclusive-OR

**Description**:
This instruction rotates each 64-bit element of the 128-bit
vector in a source SIMD&FP register left by 1, performs a bitwise
exclusive-OR of the resulting 128-bit vector and the vector in
another source SIMD&FP register, and writes the result to the
destination SIMD&FP register.

### Variant: `Advanced SIMD`
- **Assembly**: `RAX1  <Vd>.2D, <Vn>.2D, <Vm>.2D`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24  22  20  15 14 13  11   9   4  |
|-----------------------------------|
| 1100 111 00  11  Rm  1   0   00  11  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha512_3.RAX1_VVV2_cryptosha512_3)

```
if !IsFeatureImplemented(FEAT_SHA3) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.simd_dp.cryptosha512_3.RAX1_VVV2_cryptosha512_3)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) Vm = V[m, 128];
constant bits(128) Vn = V[n, 128];
V[d, 128] = Vn EOR (ROL(Vm<127:64>, 1):ROL(Vm<63:0>, 1));
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
- source: `rax1_advsimd.xml`
</details>