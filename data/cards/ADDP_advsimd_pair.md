## ADDP
_ARM A64 Instruction_

**Title**: ADDP (scalar) -- A64 | **Class**: `advsimd` | **XML ID**: `ADDP_advsimd_pair`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Add pair of elements (scalar)

**Description**:
This instruction adds two vector elements in the source SIMD&FP register
and writes the scalar result into the destination SIMD&FP register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD`
- **Assembly**: `ADDP  D<d>, <Vn>.2D`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23  21  16  11   9   4  |
|-----------------------------------|
| 01  0   1   111 0   11  11000 11011 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdpair.ADDP_asisdpair_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 64;
constant integer datasize = 128;
```

#### Execute (A64.simd_dp.asisdpair.ADDP_asisdpair_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[n, datasize];
V[d, esize] = IntReduce(ReduceOp_ADD, operand, esize);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<d>` | `register (64-bit)` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
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
- source: `addp_advsimd_pair.xml`
</details>