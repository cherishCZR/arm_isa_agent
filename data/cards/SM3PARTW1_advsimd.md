## SM3PARTW1
_ARM A64 Instruction_

**Title**: SM3PARTW1 -- A64 | **Class**: `advsimd` | **XML ID**: `SM3PARTW1_advsimd`

**Architecture**: `FEAT_SM3` (ARMv8.2)

**Summary**: SM3PARTW1

**Description**:
This instruction takes three 128-bit vectors from the three source SIMD&FP registers
and returns a 128-bit result in the destination SIMD&FP register. The result is
obtained by a three-way exclusive-OR of the elements within the input vectors
with some fixed rotations, see the Operation pseudocode for more
information.

### Variant: `Advanced SIMD`
- **Assembly**: `SM3PARTW1  <Vd>.4S, <Vn>.4S, <Vm>.4S`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24  22  20  15 14 13  11   9   4  |
|-----------------------------------|
| 1100 111 00  11  Rm  1   1   00  00  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha512_3.SM3PARTW1_VVV4_cryptosha512_3)

```
if !IsFeatureImplemented(FEAT_SM3) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.simd_dp.cryptosha512_3.SM3PARTW1_VVV4_cryptosha512_3)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) Vm = V[m, 128];
constant bits(128) Vn = V[n, 128];
constant bits(128) Vd = V[d, 128];
bits(128) result;

result<95:0> = (Vd EOR Vn)<95:0> EOR (ROL(Vm<127:96>, 15):ROL(Vm<95:64>, 15):ROL(Vm<63:32>, 15));

for i = 0 to 3
    if i == 3 then
        result<127:96> = (Vd EOR Vn)<127:96> EOR (ROL(result<31:0>, 15));
    result<(32*i)+31:(32*i)> = (result<(32*i)+31:(32*i)> EOR ROL(result<(32*i)+31:(32*i)>, 15) EOR
                                ROL(result<(32*i)+31:(32*i)>, 23));
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
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP source and destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the second SIMD&FP source register, encoded in the "Rn" field. |
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
- source: `sm3partw1_advsimd.xml`
</details>