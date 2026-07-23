## UMMLA
_ARM A64 Instruction_

**Title**: UMMLA (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `UMMLA_advsimd_vec`

**Architecture**: `FEAT_I8MM` (PROFILE_A)

**Summary**: Unsigned 8-bit integer matrix multiply-accumulate (vector)

**Description**:
This instruction multiplies the
2x8 matrix of unsigned 8-bit integer values in the first source vector by the
8x2 matrix of unsigned 8-bit integer values in the second source vector. The
resulting 2x2 32-bit integer matrix product is destructively added to
the 32-bit integer matrix accumulator in the destination vector. This
is equivalent to performing an 8-way dot product per destination element.

From Armv8.2 to Armv8.5, this is an OPTIONAL instruction.
From Armv8.6 it is mandatory for implementations that include Advanced SIMD to support it.
ID_AA64ISAR1_EL1.I8MM indicates whether this instruction is supported.

### Variant: `Vector`
- **Assembly**: `UMMLA  <Vd>.4S, <Vn>.16B, <Vm>.16B`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15 14  11 10  9   4  |
|-----------------------------------------------|
| 0   1   1   0   111 0   10  0   Rm  1   010 0   1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame2.UMMLA_asimdsame2_G)

```
if !IsFeatureImplemented(FEAT_I8MM) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant boolean op1_unsigned = TRUE;
constant boolean op2_unsigned = TRUE;
```

#### Execute (A64.simd_dp.asimdsame2.UMMLA_asimdsame2_G)

```
CheckFPAdvSIMDEnabled64();
constant bits(128) operand1 = V[n, 128];
constant bits(128) operand2 = V[m, 128];
constant bits(128) addend   = V[d, 128];

V[d, 128] = MatMulAdd(addend, operand1, operand2, op1_unsigned, op2_unsigned);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_I8MM)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP third source and destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

### Operational Notes

Arm expects that the UMMLA (vector) instruction will deliver a peak integer multiply throughput that is at least as high as can be achieved using two UDOT (vector) instructions, with a goal that it should have significantly higher throughput.
        If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- advsimd-type: `simd`
- isa: `A64`
- source: `ummla_advsimd_vec.xml`
</details>