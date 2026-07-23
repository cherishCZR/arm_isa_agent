## SM3SS1
_ARM A64 Instruction_

**Title**: SM3SS1 -- A64 | **Class**: `advsimd` | **XML ID**: `SM3SS1_advsimd`

**Architecture**: `FEAT_SM3` (ARMv8.2)

**Summary**: SM3SS1

**Description**:
This instruction rotates the top 32 bits of the 128-bit vector in the first source SIMD&FP
register by 12, and adds that 32-bit value to the two other 32-bit values held in
the top 32 bits of each of the 128-bit vectors in the second and third source
SIMD&FP registers, rotating this result left by 7 and writing the final result
into the top 32 bits of the vector in the destination SIMD&FP register, with
the bottom 96 bits of the vector being written to 0.

### Variant: `Advanced SIMD`
- **Assembly**: `SM3SS1  <Vd>.4S, <Vn>.4S, <Vm>.4S, <Va>.4S`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24  22  20  15 14   9   4  |
|-----------------------------|
| 1100 111 00  10  Rm  0   Ra  Rn  Rd  |
```

#### Decode (A64.simd_dp.crypto4.SM3SS1_VVV4_crypto4)

```
if !IsFeatureImplemented(FEAT_SM3) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer a = UInt(Ra);
```

#### Execute (A64.simd_dp.crypto4.SM3SS1_VVV4_crypto4)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) Vm = V[m, 128];
constant bits(128) Vn = V[n, 128];
constant bits(128) Va = V[a, 128];

bits(128) result;
result<127:96> = ROL((ROL(Vn<127:96>, 12) + Vm<127:96> + Va<127:96>), 7);
result<95:0> = Zeros(96);
V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SM3)` |

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
- source: `sm3ss1_advsimd.xml`
</details>