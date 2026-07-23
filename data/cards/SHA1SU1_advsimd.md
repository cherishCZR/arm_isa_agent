## SHA1SU1
_ARM A64 Instruction_

**Title**: SHA1SU1 -- A64 | **Class**: `advsimd` | **XML ID**: `SHA1SU1_advsimd`

**Architecture**: `FEAT_SHA1` (ARMv8.0)

**Summary**: SHA1 schedule update 1

**Description**:
SHA1 schedule update 1.

### Variant: `Advanced SIMD`
- **Assembly**: `SHA1SU1  <Vd>.4S, <Vn>.4S`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24 23  21  16  11   9   4  |
|-----------------------------|
| 0101 111 0   00  10100 00001 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha2.SHA1SU1_VV_cryptosha2)

```
if !IsFeatureImplemented(FEAT_SHA1) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
```

#### Execute (A64.simd_dp.cryptosha2.SHA1SU1_VV_cryptosha2)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) operand1 = V[d, 128];
constant bits(128) operand2 = V[n, 128];
constant bits(128) T = operand1 EOR LSR(operand2, 32);

bits(128) result;
result<31:0>   = ROL(T<31:0>,   1);
result<63:32>  = ROL(T<63:32>,  1);
result<95:64>  = ROL(T<95:64>,  1);
result<127:96> = ROL(T<127:96>, 1) EOR ROL(T<31:0>, 2);
V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SHA1)` |

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
- source: `sha1su1_advsimd.xml`
</details>