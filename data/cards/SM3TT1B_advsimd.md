## SM3TT1B
_ARM A64 Instruction_

**Title**: SM3TT1B -- A64 | **Class**: `advsimd` | **XML ID**: `SM3TT1B_advsimd`

**Architecture**: `FEAT_SM3` (ARMv8.2)

**Summary**: SM3TT1B

**Description**:
This instruction takes three 128-bit vectors from three source SIMD&FP
registers and a 2-bit immediate index value, and returns a 128-bit
result in the destination SIMD&FP register. It performs a 32-bit
majority function between the three 32-bit fields held in the upper
three elements of the first source vector, and adds the resulting
32-bit value and the following three other 32-bit values:

The result of this addition is returned as the top element of the
result. The other elements of the result are taken from elements of
the first source vector, with the element returned in bits<63:32>
being rotated left by 9.

### Variant: `Advanced SIMD`
- **Assembly**: `SM3TT1B  <Vd>.4S, <Vn>.4S, <Vm>.S[<imm2>]`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24  22  20  15  13  11   9   4  |
|--------------------------------|
| 1100 111 00  10  Rm  10  imm2 01  Rn  Rd  |
```

#### Decode (A64.simd_dp.crypto3_imm2.SM3TT1B_VVV4_crypto3_imm2)

```
if !IsFeatureImplemented(FEAT_SM3) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer i = UInt(imm2);
```

#### Execute (A64.simd_dp.crypto3_imm2.SM3TT1B_VVV4_crypto3_imm2)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) Vm = V[m, 128];
constant bits(128) Vn = V[n, 128];
constant bits(128) Vd = V[d, 128];

bits(32) WjPrime;
bits(128) result;
bits(32) TT1;
bits(32) SS2;

WjPrime = Elem[Vm, i, 32];
SS2 = Vn<127:96> EOR ROL(Vd<127:96>, 12);
TT1 = (Vd<127:96> AND Vd<63:32>) OR (Vd<127:96> AND Vd<95:64>) OR (Vd<63:32> AND Vd<95:64>);
TT1 = (TT1 + Vd<31:0> + SS2 + WjPrime)<31:0>;
result<31:0> = Vd<63:32>;
result<63:32> = ROL(Vd<95:64>, 9);
result<95:64> = Vd<127:96>;
result<127:96> = TT1;
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
| `<imm2>` | `immediate` | `imm2` | Is a 32-bit element indexed out of <Vm>, encoded in "imm2". |

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
- source: `sm3tt1b_advsimd.xml`
</details>